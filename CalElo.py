import math

class CalElo():
    
    def __init__(self, Ra, Rb, K, d):
        self.Ra = Ra
        self.Rb = Rb
        self.K = K
        self.d = d
 
    def Probability(self, rating1, rating2):
        return 1.0 * 1.0 / (1 + 1.0 * math.pow(10,1.0*(rating1-rating2)/400))
    
    def EloRating(self):
        self.Pb = self.Probability(self.Ra, self.Rb)
        self.Pa = self.Probability(self.Rb, self.Ra)

        # Case -1 When Player A wins
        if (self.d == 1):
            self.Ra = self.Ra + self.K * (1 - self.Pa)
            self.Rb = self.Rb + self.K * (0 - self.Pb)
        # Case -2 When Player B wins
        else:
            self.Ra = self.Ra + self.K * (0 - self.Pa)
            self.Rb = self.Rb + self.K * (1 - self.Pb)
        print("Updated Ratings:-")
        print("Ra =", round(self.Ra, 6), " Rb =", round(self.Rb, 6))
new = CalElo(1000, 1000, 30, 1)
new.EloRating()



