import matplotlib.pyplot as plt

# class to visualize the results
class DSPlot:
    use_axis = False
    lx = 0
    tx = 0
    ly = 0
    ty = 0
    radius = False

    # if min and max axis are in use
    def init(self, plset):
        self.use_axis = plset.pop(0)
        self.lx = plset.pop(0)
        self.tx = plset.pop(0)
        self.ly = plset.pop(0)
        self.ty = plset.pop(0)
        self.radius = plset.pop(0)

    # plot the figure into the files
    def plot(self, clusters, safe_fading, out_fading, outputfolder, t):
        circles = []

        for c in clusters:
            point = c.getCenter()
            if c.outlier:
                plt.plot(point[0], point[1], 'go')
                if self.radius:
                    circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color='g', fill=False))
            else:
                plt.plot(point[0], point[1], 'yo')
                if self.radius:
                    circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color='y', fill=False))

        for c in safe_fading:
            point = c.getCenter()
            plt.plot(point[0], point[1], 'bo')
            if self.radius:
                circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color='b', fill=False))

        for c in out_fading:
            point = c.getCenter()
            plt.plot(point[0], point[1], 'ro')
            if self.radius:
                circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color='r', fill=False))

        if self.use_axis:
            plt.axis([self.lx,self.tx,self.ly,self.ty])

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
