import math
import datapoint as dp
import datastream as ds
import plot
import random

# Korm algorithm implementation
class Korm:
    # list containing current facilities
    facils = []

    # list of temporal outliers
    temp_out = []

    # list of real outliers
    real_out = []
 
    # X = data stream
    X = ""

    # n = number of points in the given data stream
    n = 0
    
    # k = lower bound for the number of facilities (k < n)
    k = 0

    # p = number of phases (p <= n)
    p = 0

    # O = number of phases a temporal Outlier is tested (O = k gives the best results)
    O = 0

    # gamma = beta = 34 -> gamma + 4 * (1 + 4 * (beta + gamma)) <= gamma * beta
    # c aproximate algorithm -> beta >= 2 * c * (1 + gamma) + gamma
    gamma = 0
    beta = 0

    # Num = number of data points in a chunk
    Num = 0
    
    # Lj = lower bound for current chunk of data
    Lj = "not_assigned"

    # Fj = facility cost for current chunk of data
    Fj = "not_assigned"

    # Tc = total cost of solution
    Tc = 0

    # kp = visualization object for the algorithm
    kp = plot.KormPlot()
    sample_ofl = False
    sample_clu = False

    first_run = True
    j = 0

    # initialize the parameters for the run
    def init(self, data_stream, n, k, P, O, gamma, beta, Num, plot_settings):
        self.X = data_stream
        self.n = n
        self.k = k
        self.p = P
        self.O = O
        self.gamma = gamma
        self.beta = beta
        self.Num = Num
        
        if plot_settings.pop(0):
            self.sample_ofl = plot_settings.pop(0)
            self.sample_clu = plot_settings.pop(0)
            plot_settings.append(self.X.output)
            self.kp.init(plot_settings)

    # this function goes trough the incoming chunks of data points to detect outliers
    def run_once(self, chunk):
        self.X.process_data(chunk)
        # get the current chunk of data and the facilities to it
        Xj = self.X.current_chunk()
        for f in self.facils:
            Xj.append(f)

        if self.first_run:
            # calculate Lower bound    
            self.Lj = self.set_lb(Xj) / self.beta
            self.j = 1
            self.first_run = False

            # make a visualization of the starting points
            self.kp.plot(Xj, self.facils, self.temp_out, self.real_out)

        # calculate the facility cost for current window
        self.Fj = self.Lj / (self.k * (1 + math.log10(self.n)))

        # cluster the data
        self.cluster(Xj)

        # check if temporal outlier is a real outlier and reassign it
        real_outs = []
        for f in self.facils:
            if f.outlierscore == self.O:
                real_outs.append(f)

        for ro in real_outs:
                self.facils.remove(ro)
                self.temp_out.remove(ro)
                self.real_out.append(ro)


        # make a visualization of this phase
        self.kp.plot(Xj, self.facils, self.temp_out, self.real_out)

        # increase the lower bound
        self.Lj = self.Lj * self.beta

        self.j += 1

    # set the lower bound of first phase
    # returns D = minimal distance between the first k+1 members of X
    def set_lb(self, X):
        D = "not_assigned"
        # takes first k elements
        Xk = X[0:self.k+1]
        Xk2 = X[0:self.k+1]
        # iterate trough both lists
        for i in Xk:
            for j in Xk2:
                if i is not j:
                    # calculate distance of the 2 points
                    dist = dp.DataPoint().point_distance(i, j)
                    if D is "not_assigned" or dist < D:
                        D = dist
            # take out first in list, as it has already been calculated
            Xk2.pop(0)
        return D

    # A.Meyerson's ONLINE-FL algorithm
    # finding the facilities for a segment of point stream or assigning them to the closest
    def online_fl(self, X, fj):
        change = False
        for p in X:
            cloFacil = "not_assigned"
            theta = "not_assigned"

            if p not in self.facils:
                # find closest facility to the point
                for f in self.facils:
                    dist = dp.DataPoint().point_distance(p, f)
                    if theta is "not_assigned" or dist < theta:
                        theta = dist
                        cloFacil = f

                if not (theta == p.dist):
                    change = True
                    p.dist = theta

                # the probability of opening a new facility is min(theta * weight / facility cost, 1)
                if fj == 0:
                    probability = 1
                else:
                    probability = (theta * p.weight) / (fj)

                # note: the probability is very high at start compared to the random [0.0,1.0)
                rand = random.random()
                p.unassign()

                # make point new facility
                if probability >= rand and len(self.facils) < (self.k * math.log10(self.n)):
                    self.facils.append(p)
                    self.Tc = self.Tc + fj
                    change = True

                    # make a figure of this step
                    if self.sample_ofl:
                        new_fac = True
                        self.kp.plot_step(X, self.facils, self.temp_out, self.real_out, p, cloFacil, new_fac)

                # or assign it to an existing facility
                else:
                    cloFacil.assignPoint(p)
                    p.assignedto = cloFacil
                    self.Tc = self.Tc + (theta * p.weight)

                    # make a figure of this step
                    if self.sample_ofl:
                        new_fac = False
                        self.kp.plot_step(X, self.facils, self.temp_out, self.real_out, p, cloFacil, new_fac)

        # returns if there was a change in the run or not
        return change

    # function to cluster the given data chunk
    def cluster(self, Xj):
        Lj = self.Lj
        k = self.k
        n = self.n
        nochange = 0
        lastTc = -1
        nostop = True
        klogn = (k * math.log10(n))
        change = False

        # set first facility to be the first data point
        if len(self.facils) == 0:
            self.facils.append(Xj[0])

        # runs until one of the stopping criterias is met based on the total cost, median number, and changes
        while nostop:
            change = self.online_fl(Xj, self.Fj)
            if self.sample_clu and change == True:
                self.kp.plot_cluster(Xj, self.facils, self.temp_out, self.real_out)

            # stop if total cost of solution becomes higher than this
            if self.Tc > (4 * Lj * (1 + 4 * (self.gamma + self.beta))) / (2*math.log(n)*100):
                nostop = False

            # stop if the number of facilities exceeds this
            if len(self.facils) > klogn:
                nostop = False

            # stop if there is no change since the last 2 runs
            if self.Tc == lastTc or change == False:
                nochange = nochange + 1
                if nochange >= 2:
                    nostop = False
            else:
                nochange = 0

            lastTc = self.Tc

        # remove temporal outliers if their weight changed
        nottemp = []
        for to in self.temp_out:
            if to.lastweight != to.weight:
                nottemp.append(to)

        for nt in nottemp:
            self.temp_out.remove(nt)
            nt.outlierscore = 0

        # if a facilities weight did not change then it becomes a temporal outlier
        for p in self.facils:
            if p.lastweight == p.weight:
                if p not in self.temp_out:
                    self.temp_out.append(p)
                p.outlierscore = p.outlierscore + 1 
            p.nextPhase()

