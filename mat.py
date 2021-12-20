"""
provides math functions for the calulator
"""

def factorial (n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

class Matrix ():
    def __init__ (self, values):
        self.mat = values
    
    def __getitem__ (self, index):
        return self.mat[index]
    
    def __setitem__ (self, index, value):
        self.mat[index] = value
    
    def __len__ (self):
        return len(self.mat)
    
    def __str__ (self):
        return str(self.mat)
    
    def __repr__ (self):
        f = []
        for i in range(len(self)):
            f.append(str(self[i]))
        return "\n".join(f)
    
    def __matmul__ (self, other):
        return Matrix(Matrix._multiply(self, other))
    
    def __rmatmul__ (self, other):
        return Matrix(Matrix._multiply(other, self))
    
    def __imatmul__ (self, other):
        return self.__matmul__(other)
    
    def _multiply (m1, m2):
        f = [[None] for i in range(len(m1))]
        for i in range(len(m1)):
            n = 0
            for j in range(len(m2[0])):
                n += m1[i][0] * m2[i][j]
            f[i][0] = n
        return f