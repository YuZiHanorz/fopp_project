class Polynomial:
    def _init_(self, n, d, coefficients):
        self.n = n          # num of variables
        self.d = d          # individual degree
        self.coefficients = coefficients    # coeffients for 
    
    def eval(self, a):
        return 1


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
    
    
    def getw(self):
        return self.w
    
    def verify(self, p_i):
        check = True
        for i in range(self.n):
            sum = eval(self.p_i[i], )
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
        coeffiencients = [[0 for _ in range(self.d+1)] for _ in range(self.n)]
        
        # iterate over all terms of p, calculate the contribution
        for termIdx in range((self.d+1)^self.n):
            tidx = termIdx
            for k in range(self.n):
            # the idx_th term of p is of form c_p[idx]\prod x_k^{e_k}
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
        