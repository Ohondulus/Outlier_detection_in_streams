import math

# 2D point class for incoming datas
class DataPoint:
    x = []

    # the number of phases this facility was a temporal outlier
    outlierscore = 0

    # the number of points assigned to this facility including self and in the last phase
    weight = 1
    lastweight = 0

    # who this point is assigned to and its distance
    assignedto = "not_assigned"
    dist = -1

    # initialize data point
    def init(self, x):
        self.x = list(x)

    # assign the point to this facility by increaseing its weight
    def assignPoint(self, p):
        self.weight += p.weight

    # unassign the point from this facility by removeing its weight
    def unassign(self):
        if self.assignedto is not "not_assigned":
            self.assignedto.weight -= self.weight

    # prepare this facility for the next phase
    def nextPhase(self):
        self.lastweight = self.weight

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
