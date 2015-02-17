import math

# 2D point class for incoming datas
class DataPoint:
    x = 0
    y = 0

    # the number of phases this facility was a temporal outlier
    outlierscore = 0

    # the number of points assigned to this facility including self and in the last phase
    weight = 1
    lastweight = 0

    # who this point is assigned to and its distance
    assignedto = "not_assigned"
    dist = -1

    # initialize data point
    def init(self, x, y):
        self.x = x
        self.y = y

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
        # c^2 = a^2 + b^2
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        xdiff = x2 - x1
        ydiff = y2 - y1
        dist = math.sqrt((xdiff*xdiff)+(ydiff*ydiff))
        return dist
