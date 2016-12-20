// Copyright 2016, tanakat01@gmail.com
#include <vector>
#include <unordered_map>
#include <map>
#include <algorithm>
#include <tuple>
#include "./game.h"

typedef std::vector<int> vI;
typedef std::vector<vI> vvI;
typedef std::tuple<P, vP> State;
typedef std::tuple<State, vvI> EState;
typedef std::vector<EState> vEState;

namespace std {
template <typename T>
struct hash<std::vector<T>> {
  const size_t z = 0x64b6055a;
  size_t operator()(std::vector<T> const& vs) const {
    size_t r = 0;
    for (size_t i = 0; i < vs.size(); i++) {
      r = r * z + std::hash<T>()(vs[i]);
    }
    return r;
  }
};

template <typename S, typename T>
struct hash<tuple<S, T>> {
  const size_t z = 0x64b6055a;
  size_t operator()(std::tuple<S, T> const& t) const {
    return z * std::hash<S>()(get<0>(t)) + std::hash<T>()(get<1>(t));
  }
};
}  // namespace std

typedef std::unordered_map<State, vvI> mState;

template<typename T>
std::ostream& operator<<(std::ostream& os, std::vector<T> const& vs) {
  os << "{";
  for (size_t i = 0; i < vs.size(); i++) os << (i == 0 ? "" : ",") << vs[i];
  return os << "}";
}

template<typename S, typename T>
std::ostream& operator<<(std::ostream& os, std::tuple<S, T> const& t) {
  return os << "(" << std::get<0>(t) << "," << std::get<1>(t) << ")";
}

int si = 1;
vvI initial_cmds = {vI(1,1), vI({{1, 5}}), vI({{1, 7}})};
double rate = 4.5000001;

vvI all_cmds;

void init_all_cmds() {
  for (int i = 0; i < 4; i++) {
    all_cmds.push_back(vI(1, i + 1));
    all_cmds.push_back(vI(1, i + 5));
    for (int j = 0; j < 4; j ++) {
      all_cmds.push_back(vI({{i + 1, j + 5}}));
      all_cmds.push_back(vI({{j + 5, i + 1}}));
      if (i <= j && j - i != 2) {
        all_cmds.push_back(vI({{i + 5, j + 5}}));
        for (int k = j; k < 4; k++) {
          if (k - j != 2 && k - i != 2)
            all_cmds.push_back(vI({{i + 5, j + 5, k + 5}}));
        }
      }
    }
  }
  std::sort(all_cmds.begin(), all_cmds.end());
}

State apply_cmds(State const& state, vI const& cmds) {
#if 0
  std::cerr << "apply_cmds(cmds=" << cmds << ")" << std::endl;
#endif
  P p = std::get<0>(state);
  vP ocs = std::get<1>(state);
  for (int cmd : cmds) {
    if (cmd < 5) {
      for (auto dp : WEAPONS[si]) {
        P p1 = p + rotate(dp, cmd - 1);
        if (std::find(ocs.begin(), ocs.end(), p1) == ocs.end())
          ocs.push_back(p1);
      }
    } else {
      p += rotate(newP(0, 1), cmd - 5);
    }
  }
  std::sort(ocs.begin(), ocs.end());
  return State(p, ocs);
}

bool is_opt(int l, State const& state, double rate) {
  return l * rate <= std::get<1>(state).size();
}
void show_max_repeat(int l, vEState const& opt_states) {
  std::cout << l << " " << opt_states.size() << std::endl;
  if (opt_states.size() > 0) {
    size_t s = std::get<1>(std::get<0>(opt_states[0])).size();
    std::cout <<  s /  static_cast<double>(l)<< " " << s << "/" << l << " " << opt_states[0] << std::endl;
  }
}

int main() {
  init_all_cmds();
  std::cout << all_cmds.size() << std::endl;
  vEState opt_states(1, EState(State(newP(0, 0), vvP()), vvI()));
  for (int l = 1; l <= 100; l++) {
    mState new_opt_states;
    for (auto& st : opt_states) {
      for (auto& cmds : (l > 1 ? all_cmds : initial_cmds)) {
        State new_st = apply_cmds(std::get<0>(st), cmds);
#if 0
        std::cerr << "new_st = " << new_st << std::endl;
#endif
        if (!is_opt(l, new_st, rate)) continue;
#if 0
        std::cerr << "opt" << std::endl;
#endif
        if (new_opt_states.count(new_st) > 0) continue;
#if 0
        std::cerr << "new" << std::endl;
#endif
        vvI all_cmds = std::get<1>(st);
        all_cmds.push_back(cmds);
        new_opt_states[new_st] = all_cmds;
      }
    }
    if(new_opt_states.empty()) {
#if 0
      for (auto& st : opt_states) {
        std::cout << st << std::endl;
      }
#endif
      break;
    }
    opt_states = vEState(new_opt_states.begin(), new_opt_states.end());
    std::sort(opt_states.begin(), opt_states.end(), [&](EState const& a, EState const& b) {
        size_t la = std::get<1>(std::get<0>(a)).size();
        size_t lb = std::get<1>(std::get<0>(b)).size();
        if (la != lb) return la > lb;
        return std::get<1>(a) < std::get<1>(b);
      });
    show_max_repeat(l, opt_states);
    if (opt_states.size() == 0) break;
  }
}

