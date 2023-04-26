from standard_chase import *
from oblivious_skolem_chase import *

R1 = [('a', 'b'), ('b', 'c')]
R2 = [('a', 'c')]
database = Database({'R1': R1, 'R2': R2})

T1 = TGD('R1(x,y) -> R2(x,y)')
sigma = [T1]

oblivious_skolem_chase(database, sigma)

print(database.relations)