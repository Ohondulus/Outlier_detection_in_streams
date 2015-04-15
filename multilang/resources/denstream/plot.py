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
    def plot(self, clusters, safe_fading, out_fading, outputfolder, t, point, merged_cluster, all_p):
        plt.figure(figsize=(6,6))

        for p in all_p:
            plt.plot(p.x[0], p.x[1], 'o', color = "#377eb8", alpha = 0.5)

        #plt.plot(point.x[0], point.x[1], 'x', color = "#ffff33")
        #plt.plot([point.x[0], merged_cluster.getCenter()[0]], [point.x[1], merged_cluster.getCenter()[1]])
        circles = []

        for c in clusters:
            point = c.getCenter()
            if c.outlier:
                plt.plot(point[0], point[1], 'o', color = "#ff7f00")
                if self.radius:
                    circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color="#ff7f00", fill=False))
            else:
                plt.plot(point[0], point[1], 'o', color = "#4daf4a")
                if self.radius:
                    circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color="#4daf4a", fill=False))

        for c in safe_fading:
            point = c.getCenter()
            plt.plot(point[0], point[1], 'o', color = "#984ea3")
            if self.radius:
                circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color="#377eb8", fill=False))

        for c in out_fading:
            point = c.getCenter()
            plt.plot(point[0], point[1], 'o', color = "#e41a1c")
            if self.radius:
                circles.append(plt.Circle((point[0], point[1]), c.getRadius(), color="#e41a1c", fill=False))

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
        plt.gca().grid(which = "both", alpha = 0.7)
        plt.savefig(figfile, dpi= 100)
        plt.close()
