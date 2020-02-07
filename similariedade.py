import math

class similariedade:
    
    def __init__(self):
        pass

    def dist_euclidiana(self, px, py):
        lengx, lengy = len(px), len(py)
        if lengx != lengy:
            return None
        dim, soma = lengx, 0
        for i in range(dim):
            soma += math.pow(px[i] - py[i], 2)
        return math.sqrt(soma)

    def dist_cosseno(self, px, py):
        lengx, lengy = len(px), len(py)
        if lengx != lengy:
            return None

        dividendo, divisor1, divisor2 = 0,0,0
        for i in range(lengx):
            dividendo += px[i] * py[i]
            divisor1 += math.pow(px[i], 2)
            divisor2 += math.pow(py[i], 2)
        return dividendo / (math.sqrt(divisor1) * math.sqrt(divisor2))


