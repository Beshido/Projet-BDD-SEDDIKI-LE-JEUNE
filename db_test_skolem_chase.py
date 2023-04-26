from standard_chase import *
from oblivious_skolem_chase import *
from constraints import *


R1 = Relation('R1', [('a', 'b'), ('b', 'c')])
R2 = Relation('R2', [('a', 'c')])

relations = {'R1': R1, 'R2': R2}

T1 = TGD([Attribute('x', 'R1'), Attribute('y', 'R1')], [Attribute('x', 'R2'), Attribute('y', 'R2')])
sigma = [T1]

database = Database(relations=relations, constraints=sigma)

oblivious_skolem_chase(database, sigma)

database.print_database()