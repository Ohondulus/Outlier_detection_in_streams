import math

# 2D point class for incoming datas
class DataPoint:
    x = 0
    y = 0
    original_x = 0
    original_y = 0

    time_id = 0

    nn_before = []
    count_after = 0

    outlier = False

    #optimalization
    pivot_distance = -1

    # set basic attributes
    def init(self, x, y, point_id):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.time_id = point_id
        self.nn_before = []

    # set the distance from the pivot point
    def set_pivot_distance(self, pivot):
        self.pivot_distance = self.point_distance(self, pivot)

    # return the number of non expired preceding neighbors
    def get_nn_before(self, expire_time):
        num = 0
        for t_id in self.nn_before:
            if t_id >= expire_time:
                num += 1
        return num

    # add a preceding neighbors time id to the list
    def add_prec_neigh(self, t_id):
        self.nn_before.append(t_id)

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

    # rescaling current point and the given list
    def rescale(self, isb, pivot):
        max_x = self.original_x
        max_y = self.original_y

        for p in isb:
            if abs(p.original_x) > max_x:
                max_x = abs(p.original_x)
            if abs(p.original_y) > max_y:
                max_y = abs(p.original_y)

        if max_x == 0:
            self.x = 0
        else:
            self.x = self.original_x / max_x
        if max_y == 0:
            self.y = 0
        else:
            self.y = self.original_y / max_y

        for p in isb:
            if max_x == 0:
                p.x = 0
            else:
                p.x = p.original_x / max_x
            if max_y == 0:
                p.y = 0
            else:
                p.y = p.original_y / max_y

        if self is not pivot:
            if max_x == 0:
                pivot.x = 0
            else:
                pivot.x = pivot.original_x / max_x
            if max_y == 0:
                pivot.y = 0
            else:
                pivot.y = pivot.original_y / max_y

	return max_x, max_y
