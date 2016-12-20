// Copyright 2016, tanakat01
#include <iostream>
#include <cassert>
#include <vector>

enum class P : int16_t { };

constexpr P newP(int x, int y) {
  return static_cast<P>(x * 256 + y);
}

constexpr int I(P p) { return static_cast<int>(p); }

P operator+(P p1, P p2) { return static_cast<P>(I(p1) + I(p2)); }
constexpr int Y(P p) { return (I(p) + 128 + 256 * 128) % 256 - 128; }
constexpr int X(P p) { return (I(p) + 128 + 256 * 128) / 256 - 128; }
bool operator==(P p1, P p2) { return I(p1) == I(p2); }
bool operator<(P p1, P p2) { return I(p1) < I(p2); }
P& operator+=(P& p1, P p2) { p1 = p1 + p2; return p1; }
P rotate(P p, int d) {
  switch (d) {
  case 0: return p;
  case 1: return newP(Y(p), -X(p));
  case 2: return static_cast<P>(-I(p));
  case 3: return newP(-Y(p), X(p));
  }
  assert(0);
}

std::ostream& operator<<(std::ostream& os, P p) {
  return os << "(" << X(p) << "," << Y(p) << ")";
}

namespace std {
template<>
struct hash<P> {
  size_t operator()(P p) const {
    return static_cast<size_t>(p);
  }
};
}

typedef std::vector<P> vP;
typedef vP vvP;

vP WEAPONS[3] = {
  vP({{newP(0, 1), newP(0, 2), newP(0, 3), newP(0, 4)}}),
  vP({{newP(1, 0), newP(2, 0), newP(0, 1), newP(1, 1), newP(0, 2)}}),
  vP({{newP(-1, -1), newP(1, -1), newP(-1, 0), newP(1, 0), newP(-1, 1), newP(0, 1), newP(1, 1)}})};



