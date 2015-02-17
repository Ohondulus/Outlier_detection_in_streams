import plot
import copy
import threading

# Exact Storm algorithm implementation
class ExactStorm:
    # DS = data stream
    DS = ""

    # W = windows size
    W = 0

    # R = neighborhood range
    R = 0

    # k = number of neighbors required to be inline
    k = 0

    # ISB = datapoints in the window
    ISB = []

    # t = last points time id
    t = 0

    # pivot = pivot point for optimalization of range search
    pivot = ""

    # sample_time = the number of points after the algorithm shows the current outliers
    sample_time = -1

    # ISB_plot = object for visualization
    ISB_plot = plot.ESPlot()

    # rescale = rescaling datapoints to be between 0 and 1
    rescale = False

    # set basic parameters
    def init(self, W, R, k, DS, st, plset, rescale):
        self.W = W
        self.R = R
        self.k = k
        self.DS = DS
        self.sample_time = st
        self.rescale = rescale

        # initialize with settings if they were given
        self.ISB_plot.init(plset)

    # the algorithm for detecting outliers
    def run_exact_storm(self):
        if self.sample_time != -1:
            count_time = 0

        # run until the stream stops
        while self.DS.next():
            # set first point as pivot point
            if len(self.ISB) == 0:
                self.pivot = self.DS.current_data_point()

            if self.rescale:
                (max_x, max_y) = self.DS.current_data_point().rescale(self.ISB, self.pivot)
                

            # remove the expired node
            self.remove_node()

            # get the current point from the stream
            curr_point = self.DS.current_data_point()
            curr_point.set_pivot_distance(self.pivot)
            self.t = curr_point.time_id
            
            # call the range query
            self.range_search(curr_point)

            # add to the window
            self.ISB.append(curr_point)

            # sample the current outliers and save them into the files
            if self.sample_time != -1:
                count_time += 1
                if count_time >= self.sample_time:
                    self.sample_outliers()
                    #threading.Thread(target = self.ISB_plot.plot, args = (copy.deepcopy(self.ISB),self.DS.output, self.t)).run()
                    self.ISB_plot.plot(self.ISB, self.DS.output, self.t)
                    count_time = 0

    # the algorithm for detecting outliers
    def run_once(self, data):
        if self.DS.set_data_point(data):
            # set first point as pivot point
            if len(self.ISB) == 0:
                self.pivot = self.DS.current_data_point()

            if self.rescale:
                (max_x, max_y) = self.DS.current_data_point().rescale(self.ISB, self.pivot)
                

            # remove the expired node
            self.remove_node()

            # get the current point from the stream
            curr_point = self.DS.current_data_point()
            curr_point.set_pivot_distance(self.pivot)
            self.t = curr_point.time_id
            
            # call the range query
            self.range_search(curr_point)

            # add to the window
            self.ISB.append(curr_point)


    # removes the oldest object from the window if its full
    def remove_node(self):
        if len(self.ISB) >= self.W:
            self.ISB.pop(0)

    # search the radius of the point for neighbors
    def range_search(self, curr_point):
        for dp in self.ISB:
            # check for triangular inequality using the pivot point to reduce cost
            pdist = abs(curr_point.pivot_distance - dp.pivot_distance)
            if pdist < self.R:
                if curr_point.point_distance(curr_point, dp) < self.R:
                    dp.count_after += 1
                    curr_point.add_prec_neigh(dp.time_id)

    # determine each points outlierness in the current window
    def sample_outliers(self):
        for dp in self.ISB:
            expire_time = self.t - self.W + 1
            prec_neighs = dp.get_nn_before(expire_time)
            succ_neighs = dp.count_after
            if prec_neighs + succ_neighs >= self.k:
                dp.outlier = False
            else:
                dp.outlier = True

    # determine each points outlierness in the current window
    def sample_outliers_and_plot(self):
        for dp in self.ISB:
            expire_time = self.t - self.W + 1
            prec_neighs = dp.get_nn_before(expire_time)
            succ_neighs = dp.count_after
            if prec_neighs + succ_neighs >= self.k:
                dp.outlier = False
            else:
                dp.outlier = True

        self.ISB_plot.plot(self.ISB, self.DS.output, self.t)
