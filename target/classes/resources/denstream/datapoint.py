import math

# point class for incoming datas
class DataPoint:
    x = []

    # set basic attributes
    def init(self, x):
        self.x = list(x)

    # calculates the distance of 2 given points
    def point_distance(self, p1, p2):
        # euclidesian distance
        x1 = p1.x
        x2 = p2.x

        distsquare = 0
        for i,j in zip(x1,x2):
            square = (i-j)*(i-j)
            distsquare += square

        dist = math.sqrt(distsquare)
        return dist

    # the length of the given vector
    def vector_length(self, vector):
        length = 0
        for num in vector:
            length = length + num * num

        return math.sqrt(length)
