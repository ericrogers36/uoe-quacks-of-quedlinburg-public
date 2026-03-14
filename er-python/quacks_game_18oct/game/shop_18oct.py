#shop_18oct.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

class Shop: # this contains all the shop items we can access. updates to shop between rounds are handled by the state class.
    def __init__(self):
        self.items = {
            (1, "O"): 3,
            (1, "BK"): 10,
            (1, "G"): 6,
            (2, "G"): 8,
            (4, "G"): 14,
            (1, "R"): 6,
            (2, "R"): 10,
            (4, "R"): 16,
            (1, "BL"): 5,
            (2, "BL"): 10,
            (4, "BL"): 19,
        }