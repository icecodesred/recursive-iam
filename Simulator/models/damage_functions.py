class DamageFunction:
    def damage_fraction(self, temperature):
        raise NotImplementedError

class NordhausQuadratic(DamageFunction):
    def __init__(self, coefficient=0.00267):	#base level 
        self.coefficient = coefficient

    def damage_fraction(self, temperature):
        return self.coefficient * temperature**2
