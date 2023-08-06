#pragma once

#include <alpaqa/inner/internal/solverstatus.hpp>
#include <alpaqa/outer/alm.hpp>
#include <alpaqa/outer/src/internal/alm-helpers.tpp>

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <utility>

#include <alpaqa/config/config.hpp>
#include <alpaqa/util/quadmath/quadmath-print.hpp>
#include <alpaqa/util/src/print.tpp>

namespace alpaqa {

template <class InnerSolverT>
typename ALMSolver<InnerSolverT>::Stats
ALMSolver<InnerSolverT>::operator()(const Problem &p, rvec y, rvec x) {
    using std::chrono::duration_cast;
    using std::chrono::nanoseconds;
    auto start_time = std::chrono::steady_clock::now();

    // Check the problem dimensions etc.
    p.check();

    // Lagrange multipliers corresponding to penalty constraints are always 0.
    auto &&y_penalty = y.topRows(params.penalty_alm_split);
    y_penalty.setZero();

    auto m = p.get_m();
    if (m == 0) { // No general constraints, only box constraints
        Stats s;
        vec Σ(0), error(0);
        auto ps = inner_solver(p, Σ, params.ε, true, x, y, error);
        bool inner_converged = ps.status == SolverStatus::Converged;
        auto time_elapsed    = std::chrono::steady_clock::now() - start_time;
        s.inner_convergence_failures = not inner_converged;
        s.inner += ps;
        s.ε                = ps.ε;
        s.δ                = 0;
        s.norm_penalty     = 0;
        s.outer_iterations = 1;
        s.elapsed_time     = duration_cast<nanoseconds>(time_elapsed);
        s.status           = ps.status;
        return s;
    }

    constexpr auto NaN               = alpaqa::NaN<config_t>;
    vec Σ                            = vec::Constant(m, NaN);
    vec Σ_old                        = vec::Constant(m, NaN);
    vec error_1                      = vec::Constant(m, NaN);
    vec error_2                      = vec::Constant(m, NaN);
    [[maybe_unused]] real_t norm_e_1 = NaN;
    [[maybe_unused]] real_t norm_e_2 = NaN;

    std::array<char, 64> printbuf;
    auto print_real = [&](real_t x) {
        return float_to_str_vw(printbuf, x, params.print_precision);
    };

    Stats s;

    // Initialize the penalty weights
    if (params.Σ_0 > 0) {
        Σ.fill(params.Σ_0);
    }
    // Initial penalty weights from problem
    else {
        Helpers::initialize_penalty(p, params, x, Σ);
    }

    real_t ε                      = params.ε_0;
    [[maybe_unused]] real_t ε_old = NaN;
    real_t Δ                      = params.Δ;
    real_t ρ                      = params.ρ;

    unsigned num_successful_iters = 0;

    for (unsigned int i = 0; i < params.max_iter; ++i) {
        // TODO: this is unnecessary when the previous iteration lowered the
        // penalty update factor.
        p.eval_proj_multipliers(y, params.M, params.penalty_alm_split);
        // Check if we're allowed to lower the penalty factor even further.
        bool out_of_penalty_factor_updates =
            (num_successful_iters == 0
                 ? s.initial_penalty_reduced == params.max_num_initial_retries
                 : s.penalty_reduced == params.max_num_retries) ||
            (s.initial_penalty_reduced + s.penalty_reduced ==
             params.max_total_num_retries);
        bool out_of_iter = i + 1 == params.max_iter;
        // If this is the final iteration, or the final chance to reduce the
        // penalty update factor, the inner solver can just return its results,
        // even if it doesn't converge.
        bool overwrite_results = out_of_iter || out_of_penalty_factor_updates;

        // Inner solver
        // ------------

        // Call the inner solver to minimize the augmented lagrangian for fixed
        // Lagrange multipliers y.
        auto ps = inner_solver(p, Σ, ε, overwrite_results, x, y, error_2);
        // Reset the Lagrange multipliers for the penalty constraints to 0 again.
        y_penalty.setZero();
        // Check if the inner solver converged
        bool inner_converged = ps.status == SolverStatus::Converged;
        // Accumulate the inner solver statistics
        s.inner_convergence_failures += not inner_converged;
        s.inner += ps;

        auto time_elapsed = std::chrono::steady_clock::now() - start_time;
        bool out_of_time  = time_elapsed > params.max_time;
        bool backtrack =
            not inner_converged && not overwrite_results && not out_of_time;

        // Print statistics of current iteration
        if (params.print_interval != 0 && i % params.print_interval == 0) {
            real_t δ       = backtrack ? NaN : vec_util::norm_inf(error_2);
            auto color     = inner_converged ? "\x1b[0;32m" : "\x1b[0;31m";
            auto color_end = "\x1b[0m";
            std::cout << "[\x1b[0;34mALM\x1b[0m]   " << std::setw(5) << i
                      << ": ‖Σ‖ = " << print_real(Σ.norm())
                      << ", ‖y‖ = " << print_real(y.norm())
                      << ", δ = " << print_real(δ)
                      << ", ε = " << print_real(ps.ε)
                      << ", Δ = " << print_real(Δ) << ", status = " << color
                      << std::setw(13) << ps.status << color_end
                      << ", iter = " << std::setw(13) << ps.iterations
                      << std::endl; // Flush for Python buffering
        }

        // TODO: check penalty size?
        if (ps.status == SolverStatus::Interrupted) {
            s.ε                = ps.ε;
            s.δ                = vec_util::norm_inf(error_2);
            s.norm_penalty     = Σ.norm();
            s.outer_iterations = i + 1;
            s.elapsed_time     = duration_cast<nanoseconds>(time_elapsed);
            s.status           = ps.status;
            return s;
        }

        // Backtrack and lower penalty if inner solver did not converge
        if (backtrack) {
            // This means the inner solver didn't produce a solution that
            // satisfies the required tolerance.
            // The best thing we can do now is to restore the penalty to its
            // previous value (when the inner solver did converge), then lower
            // the penalty update factor Δ, and update the penalty with this
            // smaller factor.
            // On convergence failure, error_2 is not overwritten by the inner
            // solver, so it still contains the error from the iteration before
            // the previous successful iteration. error_1 contains the error of
            // the last successful iteration. (Unless, of course, there hasn't
            // been a successful iteration yet, which is covered by the second
            // branch of the following if statement.)
            if (num_successful_iters > 0) {
                // We have a previous Σ and error
                // Recompute penalty with smaller Δ
                Δ = std::fmax(params.Δ_min, Δ * params.Δ_lower);
                Helpers::update_penalty_weights(params, Δ, false, error_1,
                                                error_2, norm_e_1, norm_e_2,
                                                Σ_old, Σ, true);
                // Recompute the primal tolerance with larger ρ
                ρ = std::fmin(params.ρ_max, ρ * params.ρ_increase);
                ε = std::fmax(ρ * ε_old, params.ε);
                ++s.penalty_reduced;
            } else {
                // We don't have a previous Σ, simply lower the current Σ and
                // increase ε
                Σ *= params.Σ_0_lower;
                ε *= params.ε_0_increase;
                ++s.initial_penalty_reduced;
            }
        }

        // If the inner solver did converge, increase penalty
        else {
            // After this line, error_1 contains the error of the current
            // (successful) iteration, and error_2 contains the error of the
            // previous successful iteration.
            error_2.swap(error_1);
            norm_e_2 = std::exchange(norm_e_1, vec_util::norm_inf(error_1));

            // Check the termination criteria
            bool alm_converged =
                ps.ε <= params.ε && inner_converged && norm_e_1 <= params.δ;
            bool exit = alm_converged || out_of_iter || out_of_time;
            if (exit) {
                s.ε                = ps.ε;
                s.δ                = norm_e_1;
                s.norm_penalty     = Σ.norm();
                s.outer_iterations = i + 1;
                s.elapsed_time     = duration_cast<nanoseconds>(time_elapsed);
                s.status           = alm_converged ? SolverStatus::Converged
                                     : out_of_time ? SolverStatus::MaxTime
                                     : out_of_iter ? SolverStatus::MaxIter
                                                   : SolverStatus::Busy;
                return s;
            }
            // After this line, Σ_old contains the penalty used in the current
            // (successful) iteration.
            Σ_old.swap(Σ);
            // Update Σ to contain the penalty to use on the next iteration.
            Helpers::update_penalty_weights(
                params, Δ, num_successful_iters == 0, error_1, error_2,
                norm_e_1, norm_e_2, Σ_old, Σ, true);
            // Lower the primal tolerance for the inner solver.
            ε_old = std::exchange(ε, std::fmax(ρ * ε, params.ε));
            ++num_successful_iters;
        }
    }
    throw std::logic_error("[ALM]   loop error");
}

} // namespace alpaqa