import math
import datapoint as dp

# micro cluster class
class MicroCluster:
    CF1 = []
    CF2 = []
    w = 0
    time_id = 0
    outlier = False

    # check if its an outlier cluster
    def checkOutlierness(self, outlier_weight):
        if self.w > outlier_weight:
            self.outlier = False
            return False
        else:
            self.outlier = True
            return True

    # set this cluster to be an outlier cluster
    def setOutlier(self, time):
        self.time_id = time
        self.outlier = True

    # the distance of the point and the clusters center
    def distance(self, point):
        center = self.CF1
        for i in range(len(center)):
            center[i] = center[i] / self.w

        c = dp.DataPoint()
        c.init(center)
        return point.point_distance(c, point)

    # try to merge the point into this cluster, based on its radius
    def tryMerge(self, point, epsilonParam):
        center = self.CF1
        for i in range(len(center)):
            center[i] = center[i] + point.x[i]

        square_center = self.CF2
        for j in range(len(square_center)):
            square_center[i] = square_center[i] + point.x[i] * point.x[i]

        center_length = point.vector_length(center) / (self.w + 1)
        square_center_length = point.vector_length(square_center) / (self.w + 1)

        radius = square_center_length - (center_length * center_length)

        #TODO: workaround for negative numbers
        if(radius < 0):
            radius = radius * (-1)

        radius = math.sqrt(radius)
        

        if(radius <= epsilonParam):
            self.addPoint(point)
            return True
        else:
            return False

    # incrementally change the cluster with the statistics of the point
    def addPoint(self, point):
        if self.CF1 == []:
            self.CF1 = point.x
        else:
            for i in range(len(self.CF1)):
                self.CF1[i] = self.CF1[i] + point.x[i]

        if self.CF2 == []:
            self.CF2 = point.x
            for i in range(len(self.CF2)):
                self.CF2[i] = self.CF2[i] * self.CF2[i]
        else:
            for i in range(len(self.CF2)):
                self.CF2[i] = self.CF2[i] + point.x[i] * point.x[i]

        self.w = self.w + 1

    # elapse time if none where merged, the cluster is fading out in significance
    def noneMerged(self, lambdaParam, delta_time):
        delta = 1.0
        for i in range(int(lambdaParam * delta_time)):
            delta = delta / 2

        for j in range(len(self.CF1)):
            self.CF1[j] = self.CF1[j] * delta

        for k in range(len(self.CF2)):
            self.CF2[k] = self.CF2[k] * delta

        self.w = self.w * delta

    # check if this outlier has become a real outlier
    def checkRealOutlierness(self, lambdaParam, tc, Tp):
        exp = lambdaParam * (tc - self.time_id + Tp)
        score = 1.0
        for i in range(int(exp)):
            score = score / 2

        score = score - 1

        exp2 = lambdaParam * Tp
        divide = 1.0
        for j in range(int(exp2)):
            divide = divide / 2

        divide = divide - 1

        score = score / divide

        if self.w < score:
            return True
        else:
            return False

    # get the center of the cluster
    def getCenter(self):
        center = self.CF1
        for i in range(len(center)):
            center[i] = center[i] / self.w

        return center

    # get the radius of the cluster
    def getRadius(self):
        center = self.CF1
        square_center = self.CF2

        center_length = dp.DataPoint().vector_length(center) / (self.w)
        square_center_length = dp.DataPoint().vector_length(square_center) / (self.w)

        radius = square_center_length - (center_length * center_length)

        #TODO: workaround for negative numbers
        if(radius < 0):
            radius = radius * (-1)

        radius = math.sqrt(radius)
        
        return radius
