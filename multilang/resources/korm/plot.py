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
        plt.figure(figsize=(6,6))
        
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
            dpx.append(dp.x[0])
            dpy.append(dp.x[1])

        for f in fac_list:
            fx.append(f.x[0])
            fy.append(f.x[1])

        for to in tout_list:
            tox.append(to.x[0])
            toy.append(to.x[1])

        for ro in rout_list:
            rox.append(ro.x[0])
            roy.append(ro.x[1])

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(dpx, dpy, 'o', color = "#377eb8")
        plt.plot(fx, fy, 'o', color = "#4daf4a") 
        plt.plot(tox, toy, 'o', color = "#ff7f00")
        plt.plot(rox, roy, 'o', color = "#e41a1c")
        #plt.legend(["DP", "Fac", "TeO", "ReO"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        # create file if it doesn't exist and save the figure into it
        fig = self.output + "/figure_%s" %self.count_step
        self.count_step += 1   
        try:
            figfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.gca().grid(which = "both", alpha = 0.7)
        plt.savefig(figfile, dpi= 100)
        plt.close()

    # plot a step of online_fl
    def plot_step(self, dp_list, fac_list, tout_list, rout_list, curr_point, curr_fac, new_fac):
        plt.figure(figsize=(6,6))

        dpx = []
        dpy = []
        fx = []
        fy = []
        tox = []
        toy = []
        rox = []
        roy = []
        cx = curr_point.x[0]
        cy = curr_point.x[1]
        cfx = curr_fac.x[0]
        cfy = curr_fac.x[1]

        # gather all x and y attributes into different lists
        for dp in dp_list:
            dpx.append(dp.x[0])
            dpy.append(dp.x[1])

        for f in fac_list:
            fx.append(f.x[0])
            fy.append(f.x[1])

        for to in tout_list:
            tox.append(to.x[0])
            toy.append(to.x[1])

        for ro in rout_list:
            rox.append(ro.x[0])
            roy.append(ro.x[1])

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(dpx, dpy, 'yo', color = "#377eb8")
        plt.plot(fx, fy, 'bo', color = "#4daf4a") 
        plt.plot(tox, toy, 'o', color = "#ff7f00")
        plt.plot(rox, roy, 'o', color = "#e41a1c")

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
            figfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.gca().grid(which = "both", alpha = 0.7)
        plt.savefig(figfile, dpi= 100)
        plt.close()

    # plot a step of clustering TODO: Out of date
    def plot_cluster(self, dp_list, fac_list, tout_list, rout_list):
        plt.figure(figsize=(6,6))

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
        plt.plot(dpx, dpy, 'yo', color = "#377eb8")
        plt.plot(fx, fy, 'bo', color = "#4daf4a") 
        plt.plot(tox, toy, 'o', color = "#ff7f00")
        plt.plot(rox, roy, 'o', color = "#e41a1c")

        #plt.legend(["DP", "Fac", "TeO", "ReO"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        for dp in dp_list:
            if dp.assignedto != "not_assigned":
                plt.plot([dp.x, dp.assignedto.x], [dp.y, dp.assignedto.y], 'b')

        # create file if it doesn't exist and save the figure into it
        self.count_step += 1
        fig = self.output + "/figure_%s" %self.count_step    
        try:
            figfile = open(fig + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.gca().grid(which = "both", alpha = 0.7)
        plt.savefig(figfile, dpi= 100)
        plt.close()
