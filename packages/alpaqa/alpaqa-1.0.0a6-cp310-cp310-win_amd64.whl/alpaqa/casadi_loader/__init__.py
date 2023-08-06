import casadi as cs
import os
from os.path import join, basename
import alpaqa as pa
import shelve
import uuid
import pickle
import base64
import glob
import subprocess
import platform
import sys
import warnings
from ..casadi_generator import generate_casadi_problem, generate_casadi_control_problem, generate_casadi_quadratic_control_problem
from ..cache import get_alpaqa_cache_dir


def _load_casadi_problem(sofile, n, m, p):
    print("-- Loading:", sofile)
    prob = pa.load_casadi_problem(sofile, n=n, m=m, p=p)
    return prob


def generate_and_compile_casadi_problem(
    f: cs.Function,
    g: cs.Function,
    second_order: bool = False,
    name: str = "alpaqa_problem",
) -> pa.CasADiProblem:
    """Compile the objective and constraint functions into a alpaqa Problem.

    :param f:            Objective function.
    :param g:            Constraint function.
    :param second_order: Whether to generate functions for evaluating Hessians.
    :param name: Optional string description of the problem (used for filename).

    :return:   * Problem specification that can be passed to the solvers.
    """

    cachedir = get_alpaqa_cache_dir()
    cachefile = join(cachedir, 'problems')

    key = base64.b64encode(pickle.dumps(
        (f, g, second_order, name))).decode('ascii')

    os.makedirs(cachedir, exist_ok=True)
    with shelve.open(cachefile) as cache:
        if key in cache:
            uid, soname, dim = cache[key]
            probdir = join(cachedir, str(uid))
            sofile = join(probdir, soname)
            try:
                return _load_casadi_problem(sofile, *dim)
            except:
                del cache[key]
                # if os.path.exists(probdir) and os.path.isdir(probdir):
                #     shutil.rmtree(probdir)
                raise
        uid = uuid.uuid1()
        projdir = join(cachedir, "build")
        builddir = join(projdir, "build")
        os.makedirs(builddir, exist_ok=True)
        probdir = join(cachedir, str(uid))
        cgen, n, m, p = generate_casadi_problem(f, g, second_order, name)
        cfile = cgen.generate(join(projdir, ""))
        with open(join(projdir, 'CMakeLists.txt'), 'w') as f:
            f.write(f"""
                cmake_minimum_required(VERSION 3.17)
                project(CasADi-{name} LANGUAGES C)
                set(CMAKE_SHARED_LIBRARY_PREFIX "")
                add_library({name} SHARED {basename(cfile)})
                install(FILES $<TARGET_FILE:{name}>
                        DESTINATION lib)
                install(FILES {basename(cfile)}
                        DESTINATION src)
            """)
        build_type = 'Release'
        configure_cmd = ['cmake', '-B', builddir, '-S', projdir]
        if platform.system() == 'Windows':
            configure_cmd += ['-A', 'x64' if sys.maxsize > 2**32 else 'Win32']
        else:
            configure_cmd += ['-G', 'Ninja Multi-Config']
        build_cmd = ['cmake', '--build', builddir, '--config', build_type]
        install_cmd = [
            'cmake', '--install', builddir, '--config', build_type, '--prefix',
            probdir
        ]
        subprocess.run(configure_cmd, check=True)
        subprocess.run(build_cmd, check=True)
        subprocess.run(install_cmd, check=True)
        sofile = glob.glob(join(probdir, "lib", name + ".*"))
        if len(sofile) == 0:
            raise RuntimeError(
                f"Unable to find compiled CasADi problem '{name}'")
        elif len(sofile) > 1:
            warnings.warn(
                f"Multiple compiled CasADi problem files were found for '{name}'"
            )
        sofile = sofile[0]
        soname = os.path.relpath(sofile, probdir)
        cache[key] = uid, soname, (n, m, p)

        return _load_casadi_problem(sofile, n, m, p)

def _load_casadi_control_problem(sofile, N, nx, nu, p):
    print("-- Loading:", sofile)
    prob = pa.load_casadi_control_problem(sofile, N=N, nx=nx, nu=nu, p=p)
    return prob


def generate_and_compile_casadi_control_problem(
    f: cs.Function,
    l: cs.Function,
    l_N: cs.Function,
    N: int,
    name: str = "alpaqa_control_problem",
) -> pa.CasADiControlProblem:
    """Compile the dynamics and cost functions into an alpaqa ControlProblem.

    :param f:            Dynamics.
    :param l:            Stage cost.
    :param l_N:          Terminal cost.
    :param N:            Horizon length.
    :param name: Optional string description of the problem (used for filename).

    :return:   * Problem specification that can be passed to the solvers.
    """

    cachedir = get_alpaqa_cache_dir()
    cachefile = join(cachedir, 'problems')

    key = base64.b64encode(pickle.dumps(
        (f, l, l_N, name))).decode('ascii')

    os.makedirs(cachedir, exist_ok=True)
    with shelve.open(cachefile) as cache:
        if key in cache:
            uid, soname, dim = cache[key]
            probdir = join(cachedir, str(uid))
            sofile = join(probdir, soname)
            try:
                return _load_casadi_control_problem(sofile, N, *dim)
            except:
                del cache[key]
                # if os.path.exists(probdir) and os.path.isdir(probdir):
                #     shutil.rmtree(probdir)
                raise
        uid = uuid.uuid1()
        projdir = join(cachedir, "build")
        builddir = join(projdir, "build")
        os.makedirs(builddir, exist_ok=True)
        probdir = join(cachedir, str(uid))
        cgen, nx, nu, p = generate_casadi_control_problem(f, l, l_N, name)
        cfile = cgen.generate(join(projdir, ""))
        with open(join(projdir, 'CMakeLists.txt'), 'w') as f:
            f.write(f"""
                cmake_minimum_required(VERSION 3.17)
                project(CasADi-{name} LANGUAGES C)
                set(CMAKE_SHARED_LIBRARY_PREFIX "")
                add_library({name} SHARED {basename(cfile)})
                install(FILES $<TARGET_FILE:{name}>
                        DESTINATION lib)
                install(FILES {basename(cfile)}
                        DESTINATION src)
            """)
        build_type = 'Release'
        configure_cmd = ['cmake', '-B', builddir, '-S', projdir]
        if platform.system() == 'Windows':
            configure_cmd += ['-A', 'x64' if sys.maxsize > 2**32 else 'Win32']
        else:
            configure_cmd += ['-G', 'Ninja Multi-Config']
        build_cmd = ['cmake', '--build', builddir, '--config', build_type]
        install_cmd = [
            'cmake', '--install', builddir, '--config', build_type, '--prefix',
            probdir
        ]
        subprocess.run(configure_cmd, check=True)
        subprocess.run(build_cmd, check=True)
        subprocess.run(install_cmd, check=True)
        sofile = glob.glob(join(probdir, "lib", name + ".*"))
        if len(sofile) == 0:
            raise RuntimeError(
                f"Unable to find compiled CasADi problem '{name}'")
        elif len(sofile) > 1:
            warnings.warn(
                f"Multiple compiled CasADi problem files were found for '{name}'"
            )
        sofile = sofile[0]
        soname = os.path.relpath(sofile, probdir)
        cache[key] = uid, soname, (nx, nu, p)

        return _load_casadi_control_problem(sofile, N, nx, nu, p)


def _load_casadi_quadratic_control_problem(sofile, N, nx, nu, p):
    print("-- Loading:", sofile)
    prob = pa.load_casadi_quadratic_control_problem(sofile, N=N, nx=nx, nu=nu, p=p)
    return prob


def generate_and_compile_casadi_quadratic_control_problem(
    f: cs.Function,
    N: int,
    name: str = "alpaqa_quadratic_control_problem",
) -> pa.CasADiQuadraticControlProblem:
    """Compile the dynamics and cost functions into an alpaqa ControlProblem.

    :param f:            Dynamics.
    :param N:            Horizon length.
    :param name: Optional string description of the problem (used for filename).

    :return:   * Problem specification that can be passed to the solvers.
    """

    cachedir = get_alpaqa_cache_dir()
    cachefile = join(cachedir, 'problems')

    key = base64.b64encode(pickle.dumps(
        (f, name))).decode('ascii')

    os.makedirs(cachedir, exist_ok=True)
    with shelve.open(cachefile) as cache:
        if key in cache:
            uid, soname, dim = cache[key]
            probdir = join(cachedir, str(uid))
            sofile = join(probdir, soname)
            try:
                return _load_casadi_quadratic_control_problem(sofile, N, *dim)
            except:
                del cache[key]
                # if os.path.exists(probdir) and os.path.isdir(probdir):
                #     shutil.rmtree(probdir)
                raise
        uid = uuid.uuid1()
        projdir = join(cachedir, "build")
        builddir = join(projdir, "build")
        os.makedirs(builddir, exist_ok=True)
        probdir = join(cachedir, str(uid))
        cgen, nx, nu, p = generate_casadi_quadratic_control_problem(f, name)
        cfile = cgen.generate(join(projdir, ""))
        with open(join(projdir, 'CMakeLists.txt'), 'w') as f:
            f.write(f"""
                cmake_minimum_required(VERSION 3.17)
                project(CasADi-{name} LANGUAGES C)
                set(CMAKE_SHARED_LIBRARY_PREFIX "")
                add_library({name} SHARED {basename(cfile)})
                install(FILES $<TARGET_FILE:{name}>
                        DESTINATION lib)
                install(FILES {basename(cfile)}
                        DESTINATION src)
            """)
        build_type = 'Release'
        configure_cmd = ['cmake', '-B', builddir, '-S', projdir]
        if platform.system() == 'Windows':
            configure_cmd += ['-A', 'x64' if sys.maxsize > 2**32 else 'Win32']
        else:
            configure_cmd += ['-G', 'Ninja Multi-Config']
        build_cmd = ['cmake', '--build', builddir, '--config', build_type]
        install_cmd = [
            'cmake', '--install', builddir, '--config', build_type, '--prefix',
            probdir
        ]
        subprocess.run(configure_cmd, check=True)
        subprocess.run(build_cmd, check=True)
        subprocess.run(install_cmd, check=True)
        sofile = glob.glob(join(probdir, "lib", name + ".*"))
        if len(sofile) == 0:
            raise RuntimeError(
                f"Unable to find compiled CasADi problem '{name}'")
        elif len(sofile) > 1:
            warnings.warn(
                f"Multiple compiled CasADi problem files were found for '{name}'"
            )
        sofile = sofile[0]
        soname = os.path.relpath(sofile, probdir)
        cache[key] = uid, soname, (nx, nu, p)

        return _load_casadi_quadratic_control_problem(sofile, N, nx, nu, p)
