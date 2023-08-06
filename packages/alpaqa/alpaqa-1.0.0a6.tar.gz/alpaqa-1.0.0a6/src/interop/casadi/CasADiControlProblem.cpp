#include <alpaqa/config/config.hpp>
#include <alpaqa/interop/casadi/src/CasADiControlProblem.tpp>

namespace alpaqa {
CASADI_LOADER_EXPORT_TEMPLATE(class, CasADiControlProblem, EigenConfigd);
CASADI_LOADER_EXPORT_TEMPLATE(class, CasADiControlProblem, DefaultConfig);
} // namespace alpaqa