from math import comb




"""
       | Group 1 | Group 2 |
-------|--------|--------|
Outcome|   a    |   b    |
-------|--------|--------|
Outcome|   c    |   d    |
"""

class BarnardTest:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.n = a + b + c + d
        
        self.p1 = a / (a + b)
        self.p2 = c / (c + d)
        
        self.min_a = max(0, self.n*self.p1 + self.n*self.p2 - self.n)
        self.max_a = min(self.a+self.b, self.n*self.p1, self.n*self.p2)
        
    def p_value(self):
        """Compute the p-value for the test"""
        p_value = 0
        for i in range(int(self.min_a), int(self.max_a)+1):
            numerator = comb(self.a+self.b, i) * comb(self.c+self.d, self.n-i)
            denominator = comb(self.n, self.a+self.c)
            p_value += numerator / denominator
            
        return p_value