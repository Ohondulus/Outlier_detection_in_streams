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
    def plot(self, dp_list, outputfolder, t):
        ix = []
        iy = []
        ox = []
        oy = []

        # gather all x and y attributes into different lists
        for dp in dp_list:
            if dp.outlier:
                ox.append(dp.x)
                oy.append(dp.y)
            else:
                ix.append(dp.x)
                iy.append(dp.y)

        # plot with the datapoints / this is like the Matlab plot function
        plt.plot(ix, iy, 'yo', ox, oy, 'ro')
        #plt.legend(["Inl", "Outl"])

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

        if self.radius:
            circles = []
            for dp in dp_list:
                col = 'b'
                if dp.outlier:
                    col = 'r'
                circles.append(plt.Circle((dp.x,dp.y), self.R, color=col, fill=False))

            for c in circles:
                plt.gca().add_artist(c)
  
        # create file if it doesn't exist and save the figure into it
        figfile = outputfolder + "/figure_time_%s" %t      
        try:
            pngfile = open(figfile + ".png", "w+")
        except Exception as e:
            print("Exception opening file: %s" %e)
        plt.gca().set_aspect("equal")
        plt.savefig(figfile)
        plt.close()
