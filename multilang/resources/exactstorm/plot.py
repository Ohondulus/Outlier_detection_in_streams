import matplotlib.pyplot as plt

# class to visualize the results
class ESPlot:
    use_axis = False
    lx = 0
    tx = 0
    ly = 0
    ty = 0
    radius = False
    R = 0

    # if min and max axis are in use
    def init(self, plset):
        self.use_axis = plset.pop(0)
        self.lx = plset.pop(0)
        self.tx = plset.pop(0)
        self.ly = plset.pop(0)
        self.ty = plset.pop(0)
        self.radius = plset.pop(0)
        self.R = plset.pop(0)

    # plot the figure into the files
    def plot(self, dp_list, outputfolder, t, all_p, exactstorm):
        plt.figure(figsize=(6,6))

        ix = []
        iy = []
        ox = []
        oy = []
        ax = []
        ay = []
        aox = []
        aoy = []

        for a in all_p:
            if a.count_after + len(a.nn_before) < exactstorm.k:
                aox.append(a.x[0])
                aoy.append(a.x[1])
            else:
                ax.append(a.x[0])
                ay.append(a.x[1])

        # gather all x and y attributes into different lists
        for dp in dp_list:
            if dp.outlier:
                ox.append(dp.x[0])
                oy.append(dp.x[1])
            else:
                ix.append(dp.x[0])
                iy.append(dp.x[1])

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(ax, ay, 'o', color = "#377eb8", alpha = 0.5)
        plt.plot(aox, aoy, 'o', color = "#e41a1c", alpha = 0.5)
        plt.plot(ix, iy, 'o', color = "#377eb8")
        plt.plot(ox, oy, 'o', color = "#e41a1c")
        #plt.legend(["Inl", "Outl"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        if self.radius:
            circles = []
            for dp in dp_list:
                col = "#4daf4a"
                if dp.outlier:
                    col = "#e41a1c"
                circles.append(plt.Circle((dp.x[0],dp.x[1]), self.R, color=col, fill=False))

            for c in circles:
                plt.gca().add_artist(c)
  
        # create file if it doesn't exist and save the figure into it
        figfile = outputfolder + "/figure_time_%s" %t      
        try:
            pngfile = open(figfile + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.gca().set_aspect("equal")
        plt.gca().grid(which = "both", alpha = 0.7)
        plt.savefig(figfile, dpi= 100)
        plt.close()
