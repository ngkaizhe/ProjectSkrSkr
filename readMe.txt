input variables:
for vector: $v{number}
for matrix: $m{number}

input format for each function:

vector:
5.Norm(V) -> Norm($v0) or norm($v0)
6.Normal(V)-> Normal($v0) or normal($v0)
7.Cross(a,b) -> cross($v0,$v1) or Cross($v0,$v1)
8.Com(a,b) -> Com($v0,$v1) or com($v0,$v1)
9.Proj(A,B) -> Proj($v0, $v1) or proj($v0,$v1)
10.Area(V1,V2) -> area($v0,$v1) or Area($v0,$v1)
11.isParallel(V1,V2) -> isParallel($v0,$v1) or IsParallel($v0,$v1)
12.isOrthogonal(V1,V2) -> isOrthogonal($v0,$v1) or IsOrthogonal($v0,$v1)
13.angle(a,b) -> angle($v0,$v1) or Angle($v0,$v1)
14.pN(a,b) -> PN($v0,$v1) or pN($v0,$v1)
15.IsLI(a,b,c,...) -> IsLI($v0, $v1, $v2....) or isLI($v0, $v1, $v2....)
16.Ob(a,b,c,...) -> ob($v0,$v1, $v2...) or Ob($v0,$v1, $v2...)

matrix:
3.Rank(M1) -> rank($m0) or Rank($m0)
4.trans(M) -> trans($m0) or Trans($m0)
5.Solve Linear System (ax=b) -> solve_linear($m0, $m1)
6.Determinants of Matrix -> det($m0) or Det($m0)
7.Inverse(M1) -> Inverse($m0) or inverse($m0)
8.Adj(M) -> Adj($m0) or adj($m0)
9.Eigen Vector(v) and Eigen Value(d) -> eigen($m0) or Eigen($m0)
10.PM(M) -> PM($m0) or pM($m0)
11.LeastSquare(A1,b1) -> LeastSquare($m0, $m1)