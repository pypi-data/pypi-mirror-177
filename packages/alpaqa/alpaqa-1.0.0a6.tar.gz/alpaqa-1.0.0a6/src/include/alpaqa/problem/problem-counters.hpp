#pragma once

#include <alpaqa/export.h>

#include <chrono>
#include <iosfwd>

namespace alpaqa {

struct EvalCounter {
    unsigned proj_diff_g{};
    unsigned proj_multipliers{};
    unsigned prox_grad_step{};
    unsigned f{};
    unsigned grad_f{};
    unsigned f_grad_f{};
    unsigned f_g{};
    unsigned f_grad_f_g{};
    unsigned grad_f_grad_g_prod{};
    unsigned g{};
    unsigned grad_g_prod{};
    unsigned grad_gi{};
    unsigned grad_L{};
    unsigned hess_L_prod{};
    unsigned hess_L{};
    unsigned ψ{};
    unsigned grad_ψ{};
    unsigned grad_ψ_from_ŷ{};
    unsigned ψ_grad_ψ{};

    struct EvalTimer {
        std::chrono::nanoseconds proj_diff_g{};
        std::chrono::nanoseconds proj_multipliers{};
        std::chrono::nanoseconds prox_grad_step{};
        std::chrono::nanoseconds f{};
        std::chrono::nanoseconds grad_f{};
        std::chrono::nanoseconds f_grad_f{};
        std::chrono::nanoseconds f_g{};
        std::chrono::nanoseconds f_grad_f_g{};
        std::chrono::nanoseconds grad_f_grad_g_prod{};
        std::chrono::nanoseconds g{};
        std::chrono::nanoseconds grad_g_prod{};
        std::chrono::nanoseconds grad_gi{};
        std::chrono::nanoseconds grad_L{};
        std::chrono::nanoseconds hess_L_prod{};
        std::chrono::nanoseconds hess_L{};
        std::chrono::nanoseconds ψ{};
        std::chrono::nanoseconds grad_ψ{};
        std::chrono::nanoseconds grad_ψ_from_ŷ{};
        std::chrono::nanoseconds ψ_grad_ψ{};
    } time;

    void reset() { *this = {}; }
};

ALPAQA_EXPORT std::ostream &operator<<(std::ostream &, const EvalCounter &);

inline EvalCounter::EvalTimer &operator+=(EvalCounter::EvalTimer &a,
                                          const EvalCounter::EvalTimer &b) {
    a.proj_diff_g += b.proj_diff_g;
    a.proj_multipliers += b.proj_multipliers;
    a.prox_grad_step += b.prox_grad_step;
    a.f += b.f;
    a.grad_f += b.grad_f;
    a.f_grad_f += b.f_grad_f;
    a.f_g += b.f_g;
    a.f_grad_f_g += b.f_grad_f_g;
    a.grad_f_grad_g_prod += b.grad_f_grad_g_prod;
    a.g += b.g;
    a.grad_g_prod += b.grad_g_prod;
    a.grad_gi += b.grad_gi;
    a.grad_L += b.grad_L;
    a.hess_L_prod += b.hess_L_prod;
    a.hess_L += b.hess_L;
    a.ψ += b.ψ;
    a.grad_ψ += b.grad_ψ;
    a.grad_ψ_from_ŷ += b.grad_ψ_from_ŷ;
    a.ψ_grad_ψ += b.ψ_grad_ψ;
    return a;
}

inline EvalCounter &operator+=(EvalCounter &a, const EvalCounter &b) {
    a.proj_diff_g += b.proj_diff_g;
    a.proj_multipliers += b.proj_multipliers;
    a.prox_grad_step += b.prox_grad_step;
    a.f += b.f;
    a.grad_f += b.grad_f;
    a.f_grad_f += b.f_grad_f;
    a.f_g += b.f_g;
    a.f_grad_f_g += b.f_grad_f_g;
    a.grad_f_grad_g_prod += b.grad_f_grad_g_prod;
    a.g += b.g;
    a.grad_g_prod += b.grad_g_prod;
    a.grad_gi += b.grad_gi;
    a.grad_L += b.grad_L;
    a.hess_L_prod += b.hess_L_prod;
    a.hess_L += b.hess_L;
    a.ψ += b.ψ;
    a.grad_ψ += b.grad_ψ;
    a.grad_ψ_from_ŷ += b.grad_ψ_from_ŷ;
    a.ψ_grad_ψ += b.ψ_grad_ψ;
    a.time += b.time;
    return a;
}

inline EvalCounter operator+(EvalCounter a, const EvalCounter &b) { return a += b; }

namespace detail {
template <class T>
struct Timed {
    Timed(T &time) : time(time) { time -= std::chrono::steady_clock::now().time_since_epoch(); }
    ~Timed() { time += std::chrono::steady_clock::now().time_since_epoch(); }
    Timed(const Timed &)            = delete;
    Timed(Timed &&)                 = delete;
    Timed &operator=(const Timed &) = delete;
    Timed &operator=(Timed &&)      = delete;
    T &time;
};
#ifndef DOXYGEN
template <class T>
Timed(T &) -> Timed<T>;
#endif
} // namespace detail

} // namespace alpaqa
