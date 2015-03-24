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
        center = list(self.CF1)
        for i in range(len(center)):
            center[i] = center[i] / self.w

        c = dp.DataPoint()
        c.init(center)
        return point.point_distance(c, point)

    # try to merge the point into this cluster, based on its radius
    def tryMerge(self, point, epsilonParam):
        center = list(self.CF1)
        square_center = list(self.CF2)

        max_radius = 0
        new_w = self.w + 1

        for i in range(len(center)):
            center[i] = center[i] + point.x[i]
            square_center[i] = square_center[i] + point.x[i] * point.x[i]

            dim_radius = (square_center[i] / new_w) - ((center[i] / new_w) * (center[i] / new_w))
            if dim_radius < 0:
                dim_radius = 0
            dim_radius = math.sqrt(dim_radius)

            if max_radius < dim_radius:
                max_radius = dim_radius  

        if(max_radius <= epsilonParam):
            self.addPoint(point)
            return True
        else:
            return False

    # incrementally change the cluster with the statistics of the point
    def addPoint(self, point):
        if self.CF1 == []:
            self.CF1 = list(point.x)
        else:
            for i in range(len(self.CF1)):
                self.CF1[i] = self.CF1[i] + point.x[i]

        if self.CF2 == []:
            self.CF2 = list(point.x)
            for i in range(len(self.CF2)):
                self.CF2[i] = self.CF2[i] * self.CF2[i]
        else:
            for i in range(len(self.CF2)):
                self.CF2[i] = self.CF2[i] + point.x[i] * point.x[i]

        self.w = self.w + 1

    # elapse time if none where merged, the cluster is fading out in significance
    def noneMerged(self, lambdaParam, delta_time):
        delta = 1.0 / math.pow(2.0, lambdaParam * delta_time)

        for j in range(len(self.CF1)):
            self.CF1[j] = self.CF1[j] * delta

        for k in range(len(self.CF2)):
            self.CF2[k] = self.CF2[k] * delta

        self.w = self.w * delta

    # check if this outlier has become a real outlier
    def checkRealOutlierness(self, lambdaParam, tc, Tp):
        exp = lambdaParam * (tc - self.time_id + Tp)
        score = 1.0 / math.pow(2.0, exp)

        score = score - 1

        exp2 = lambdaParam * Tp
        divide = 1.0 / math.pow(2.0, exp2)

        divide = divide - 1

        score = score / divide

        if self.w < score:
            return True
        else:
            return False

    # get the center of the cluster
    def getCenter(self):
        center = list(self.CF1)
        for i in range(len(center)):
            center[i] = center[i] / self.w

        return center

    # get the radius of the cluster
    def getRadius(self):
        center = list(self.CF1)
        square_center = list(self.CF2)

        max_radius = 0

        for i in range(len(center)):
            dim_radius = (square_center[i] / self.w) - ((center[i] / self.w) * (center[i] / self.w))
            if dim_radius < 0:
                dim_radius = 0
            dim_radius = math.sqrt(dim_radius)

            if max_radius < dim_radius:
                max_radius = dim_radius
        
        return max_radius
