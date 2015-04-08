import plot
import microcluster
import math

# DenStream algorithm implementation
class DenStream:
    # DS = data stream
    DS = ""
    
    # MClusters = collection of all the micro clusters
    MClusters = []

    # (beta * mu) parameters determine the outlier finding scale
    betaParam = 0
    muParam = 0

    # lambda determines the fading significance of the micro clusters
    lambdaParam = 0

    # epszilon determines the maximum radius of micro clusters
    epsilonParam = 0
    
    # Tp = the time interval of checking clusters
    Tp = 0

    # current_t = the current time_id
    current_t = 0

    # elapsed_t = the current time
    elapsed_t = 0

    # class for visualization
    DSPlot = ""
    do_plot = False

    # some debug in code
    debug = False
    deleted_safe = []
    deleted_out = []
    st = 0

    errnum = 0
    pnum = 0

    def init(self, DS, betaParam, muParam, lambdaParam, epsilonParam, do_plot, st, plset):
        self.DS = DS
        self.betaParam = betaParam
        self.muParam = muParam
        self.lambdaParam = lambdaParam
        self.epsilonParam = epsilonParam

        self.st = st

        self.DSPlot = plot.DSPlot()
        self.do_plot = do_plot
        self.DSPlot.init(plset)

        p = self.betaParam * self.muParam
        self.Tp = math.ceil((1 / self.lambdaParam) * math.log(p / (p - 1),10))

    # step the algorithm with the new data point
    def run_once(self, data, data_time_id):
        if self.DS.set_data_point(data):
            point = self.DS.current_data_point()
            self.current_t = self.current_t + 1
            self.elapsed_t = self.elapsed_t + data_time_id
            # merge into a cluster or create a new one, and elapse time for all other clusters
            merged_cluster = self.merge(point)
            if self.debug:
                print(self.current_t ,merged_cluster.getCenter(), merged_cluster.getRadius(), merged_cluster.w)

            for cluster in self.MClusters:
                if cluster != merged_cluster:
                    if self.debug:
                        print(self.current_t ,cluster.getCenter(), cluster.getRadius(), cluster.w)
                    cluster.noneMerged(self.lambdaParam, data_time_id)
                    if self.debug:
                        print(self.current_t ,cluster.getCenter(), cluster.getRadius(), cluster.w)

            del_safe_clusters = []
            del_out_clusters = []

            # if Tp time has elapsed check for outliers and fading clusters
            if self.current_t % self.Tp == 0 or self.Tp == 1 or self.debug:
                for cluster in self.MClusters:
                    # if the cluster is fading, delete it from memory
                    if not cluster.outlier:
                        if cluster.checkOutlierness(self.betaParam * self.muParam):
                            del_safe_clusters.append(cluster)
                    else:
                        if cluster.checkRealOutlierness(self.lambdaParam, self.elapsed_t, self.Tp):
                            del_out_clusters.append(cluster)


                for cluster in del_safe_clusters:
                    self.MClusters.remove(cluster)
                    self.pnum = self.pnum + cluster.pnum

                    if self.debug:
                        self.deleted_safe.append(cluster)

                for cluster in del_out_clusters:
                    self.MClusters.remove(cluster)
                    self.errnum = self.errnum + cluster.pnum
                    self.pnum = self.pnum + cluster.pnum

                    if self.debug:
                        self.deleted_out.append(cluster)

                if(self.do_plot and self.current_t % self.st == 0):
                    if self.debug:
                        self.DSPlot.plot(self.MClusters, self.deleted_safe, self.deleted_out, self.DS.output, 
                            self.current_t, point, merged_cluster)
                    else:
                        self.DSPlot.plot(self.MClusters, del_safe_clusters, del_out_clusters, self.DS.output, 
                            self.current_t, point, merged_cluster)

    # merge point into closest micro cluster or make a new cluster
    def merge(self, point):
        (PMC, OMC) = self.findClosestCluster(point)
        
        # try to merge into potential micro cluster first
        if not PMC == "" and PMC.tryMerge(point, self.epsilonParam):
            return PMC
        else:
            # try to merge into outlier micro cluster and check if it is no longer outlier
            if not OMC == "" and OMC.tryMerge(point, self.epsilonParam):
                OMC.checkOutlierness(self.betaParam * self.muParam)
                return OMC
            # if could not merge, create new outlier micro cluster
            else:
                new_cluster = microcluster.MicroCluster()
                new_cluster.addPoint(point)
                new_cluster.setOutlier(self.elapsed_t)
                self.MClusters.append(new_cluster)
                return new_cluster

    # find closest potential and outlier micro clusters
    def findClosestCluster(self, point):
        # reference to clusters
        PMC = ""
        OMC = ""
        # distance to PMC and OMC
        pdist = ""
        odist = ""

        for cluster in self.MClusters:
            dist = cluster.distance(point)

            if not cluster.outlier:
                if dist < pdist or pdist == "":
                    pdist = dist
                    PMC = cluster
            else:
                if dist < odist or odist == "":
                    odist = dist
                    OMC = cluster

        return (PMC, OMC)
