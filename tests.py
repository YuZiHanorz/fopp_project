import template
from field import FieldElement
from template import Polynomial

def eval_test():
    coefficients = []
    for i in range(4):
        coefficients.append(FieldElement.random_element())
    p = Polynomial(2,1,coefficients)
    print (p.coefficients)
    print(type(p.eval(point=[3,4])))

eval_test()