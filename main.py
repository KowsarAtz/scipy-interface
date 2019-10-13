from scipysolve import solve
from pprint import pprint
import sys

result = None

if len(sys.argv) >= 2:
    result = solve(sys.argv[1])
else:
    result = solve()

pprint(result)