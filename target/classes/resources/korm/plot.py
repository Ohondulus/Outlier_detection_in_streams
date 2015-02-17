import matplotlib.pyplot as plt

# class to visualize the results
class KormPlot:
    use_axis = False
    lx = 0
    tx = 0
    ly = 0
    ty = 0

    count_step = 0
    output = ""

    # if min and max axis are in use
    def init(self, plset):
        self.use_axis = True
        self.lx = plset.pop(0)
        self.tx = plset.pop(0)
        self.ly = plset.pop(0)
        self.ty = plset.pop(0)
        self.output = plset.pop(0)

    # plot the figure into the files
    def plot(self, dp_list, fac_list, tout_list, rout_list):
        dpx = []
        dpy = []
        fx = []
        fy = []
        tox = []
        toy = []
        rox = []
        roy = []

        # gather all x and y attributes into different lists
        for dp in dp_list:
            dpx.append(dp.x)
            dpy.append(dp.y)

        for f in fac_list:
            fx.append(f.x)
            fy.append(f.y)

        for to in tout_list:
            tox.append(to.x)
            toy.append(to.y)

        for ro in rout_list:
            rox.append(ro.x)
            roy.append(ro.y)

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(dpx, dpy, 'yo', fx, fy, 'bo', tox, toy, 'go', rox, roy, 'ro')
        plt.legend(["DP", "Fac", "TeO", "ReO"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        # create file if it doesn't exist and save the figure into it
        self.count_step += 1
        fig = self.output + "/figure_%s" %self.count_step   
        try:
            pngfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.savefig(fig)
        plt.close()

    # plot a step of online_fl
    def plot_step(self, dp_list, fac_list, tout_list, rout_list, curr_point, curr_fac, new_fac):
        dpx = []
        dpy = []
        fx = []
        fy = []
        tox = []
        toy = []
        rox = []
        roy = []
        cx = curr_point.x
        cy = curr_point.y
        cfx = curr_fac.x
        cfy = curr_fac.y

        # gather all x and y attributes into different lists
        for dp in dp_list:
            dpx.append(dp.x)
            dpy.append(dp.y)

        for f in fac_list:
            fx.append(f.x)
            fy.append(f.y)

        for to in tout_list:
            tox.append(to.x)
            toy.append(to.y)

        for ro in rout_list:
            rox.append(ro.x)
            roy.append(ro.y)

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(dpx, dpy, 'yo', fx, fy, 'bo', tox, toy, 'go', rox, roy, 'ro')

        if new_fac:
            plt.plot([cx], [cy], 'bs')
        else:
            plt.plot([cx, cfx], [cy, cfy])

        plt.legend(["DP", "Fac", "TeO", "ReO"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        # create file if it doesn't exist and save the figure into it
        self.count_step += 1
        fig = self.output + "/figure_%s" %self.count_step    
        try:
            pngfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.savefig(fig)
        plt.close()

    # plot a step of clustering
    def plot_cluster(self, dp_list, fac_list, tout_list, rout_list):
        dpx = []
        dpy = []
        fx = []
        fy = []
        tox = []
        toy = []
        rox = []
        roy = []

        # gather all x and y attributes into different lists
        for dp in dp_list:
            dpx.append(dp.x)
            dpy.append(dp.y)

        for f in fac_list:
            fx.append(f.x)
            fy.append(f.y)

        for to in tout_list:
            tox.append(to.x)
            toy.append(to.y)

        for ro in rout_list:
            rox.append(ro.x)
            roy.append(ro.y)

        # plot with the datapoints
        plt.plot(dpx, dpy, 'yo', fx, fy, 'bo', tox, toy, 'go', rox, roy, 'ro')

        plt.legend(["DP", "Fac", "TeO", "ReO"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        for dp in dp_list:
            if dp.assignedto != "not_assigned":
                plt.plot([dp.x, dp.assignedto.x], [dp.y, dp.assignedto.y], 'b')

        # create file if it doesn't exist and save the figure into it
        self.count_step += 1
        fig = self.output + "/figure_%s" %self.count_step    
        try:
            pngfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.savefig(fig)
        plt.close()
