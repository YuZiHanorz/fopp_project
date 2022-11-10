class SCVerifier:
    def _init_(self, F, H, n, gamma, p):
        self.F = F          # Field
        self.H = H          # summation domain
        self.n = n          # Num of variables
        self.gamma = gamma  # sum
        self.p = p          # polynomial

        self.w = []
        for i in range(n):
            self.w.append(F.random_element())
    
    def receive(self, p_i):
        self.p_i = p_i
    
    def verify(self):
        for i in range(self.n):
            for a in self.H:
                



class SumcheckProtocol:
    def __init__(self, F, H, n, gamma, d, p):
        self.F = F          # Field
        self.H = H          # summation domain
        self.n = n          # Num of variables
        self.gamma = gamma  # sum
        self.d = d          # individual degree bound
        self.p = p          # polynomial
        