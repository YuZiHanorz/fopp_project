
def calculate_indices(index, degree, n_variables):
    
    res = []
    ind = index
    for n in range (n_variables, 0, -1):
        val = ind // (degree + 1) ^ (n-1)
        res.append(val)
        ind -= val * (degree + 1) ^ (n-1)
    return res


class Polynomial:
    """
    Represents a multivariate polynomial
    """
    
    def __init__(self, n: int, d: int, coefficients):
   
        self.n = n                          #number of variables
        self.d = d                          #individual degree
        self.coefficients = coefficients    #list of coeffiecients

    def eval(self, point):
        """ Evaluate the polynomial on a point of a certain field

        Args:
            point (FieldElement): a FieldElement point object

        Returns:
            int: the evaluation result
        """        
        val = 0
        prod = 1
        mapped_indices = []

        for i in range (self.d +1)^(self.n):
            #we need to map the index of coefficient (list) to the list of indices 
            #representing the monomial on the polynomial (e.g. indices [1, 0, 2] represents (x_1)^1 * (x_2)^0 * (x_3)^2)
            mapped_indices = calculate_indices(i, self.d, self.n)
            
            for k in range (self.n):
                prod *= (point[k] ^ mapped_indices[k])
            val += self.coefficients[i] * prod
        
        return val



class SCVerifier:
    def _init_(self, F, H, n, gamma, d, p):
        self.F = F          # field
        self.H = H          # summation domain
        self.n = n          # num of variables
        self.gamma = gamma  # sum
        self.d = d          # individual degree bound
        self.p = p          # polynomial

        self.w = []
        for i in range(n):
            self.w.append(F.random_element())
    
    #Return all the randomnesses generated during the protocol by the verifier
    def getw(self):
        return self.w
    
    # Verifies the main condition of the sumcheck protocol (i.e. \sum{elem \in H} p_i(elem) =? p_{i-1}(w_{i-1}))
    def verify(self, p_i: list[Polynomial]):
        
        sum = 0
        #receive first polynomial 
        for elem in self.H:
            sum += p_i[0].eval(elem)
        
        if sum != self.gamma:
            return False
        
        for i in range(1, self.n, 1):
            sum = 0
            for elem in self.H:
                sum += eval(self.p_i[i], elem)
            if sum != p_i[i-1].eval(self.w[i-1]):
                return False
        
        if self.p.eval(self.w) != p_i[self.n - 1].eval(self.w[self.n - 1]):
            return False
        
        return True
        
class SCProver:
    def _init_(self, F, H, n, gamma, d, p):
        self.F = F          # field
        self.H = H          # summation domain
        self.n = n          # num of variables
        self.gamma = gamma  # sum
        self.d = d          # individual degree bound
        self.p = p          # polynomial
    
    # Generate the messages p_i[] from w, a list of polynomials
    # w is the randomness sent by verifier, a list of field elements 
    def genPi(self, w):
        # the coeffients of p_i, i \in [n]
        coeffiencients = [[0 for _ in range(self.d + 1)] for _ in range(self.n)]
        
        # iterate over all terms of p, calculate the contribution
        for termIdx in range((self.d + 1) ^ self.n):
            tidx = termIdx
            # the tidx_th term of p is of form c_p[idx]\prod x_k^{e_k}
            for k in range(self.n):
                e_k = tidx // (self.d + 1) ^ (self.n - 1 - k)
                tidx -= e_k * (self.d + 1) ^ (self.n - 1 - k)
                
            # will and only will contribute to the coeffient of x_k^{e_k} of p_k
            # the contribution is \sum_{a_{k+1},\cdots,a_{n-1} \in H} p.eval(w_0, \dots, w_{k-1}, 1, a_{k+1}, \cdots, a_{n-1})
                contribution = 0
                h = len(self.H)
                
                for assignment in range(h ^ (self.n - 1 - k)):
                    aidx = assignment
                    a = []
                    
                    for i in range(self.n - 1 - k):
                        a_i = aidx // h ^ (self.n - 1 - k - 1 - i)
                        aidx -= a_i * h ^ (self.n - 1 - k - 1 - i)
                        a.append(a_i)
                    
                    contribution += self.p.eval(w[:k] + [1] + a)
                
                coeffiencients[k][e_k] += contribution
        
        p_i = []
        for i in range(self.n):
            p_i.append(Polynomial(1, self.d, coeffiencients[i]))
        return p_i


class SumcheckProtocol:
    def __init__(self, F, H, n, gamma, d, p):
        self.F = F          # Field
        self.H = H          # summation domain
        self.n = n          # Num of variables
        self.gamma = gamma  # sum
        self.d = d          # individual degree bound
        self.p = p          # polynomial
        
        self.prover = SCProver(F, H, n, gamma, d, p)
        self.verifier = SCVerifier(F, H, n, gamma, d, p)
        
    def prove(self):
        w = self.verifier.getw()
        p_i = self.prover.genPi(w)
        return self.verifier.verify(p_i)
        