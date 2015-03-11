import storm
import exactstorm.datastream as ds
import exactstorm.exactstorm as es
import ConfigParser as cp
#import threading

class Exactbolt(storm.BasicBolt):
    #bufferlist = []
    #bufflock = threading.Lock()
    exs = ""

    sample = 0
    t = 0
    
    def initialize(self, stormconf, context):
        config = cp.ConfigParser()

        configfile = "/home/ohondulus/Downloads/es_config.ini"

        outfolder = "/home/ohondulus/Downloads/pngs"
        
        # read the config file
        try:
            config.read(configfile)
        except Exception as e:
            print("Can't read the configfile: %s" %e)

        # extract exact storm settings from config file
        section = "ExactStormSettings"
        W_option = "Window_size"
        R_option = "Neighborhood_radius"
        k_option = "Neighbors_of_inliers"
        st_option = "Sample_frequency"
        rescale_option = "Rescale"

        try:
            W = int(config.get(section, W_option))
            R = float(config.get(section, R_option))
            k = int(config.get(section, k_option))
            st = int(config.get(section, st_option))
            rescale = config.get(section, rescale_option)
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        if rescale == "True":
            rescale = True
        else:
            rescale = False

        # exact plot settings from the config file
        section = "PlotSettings"
        use_option = "Use_axis"
        radius_option = "Show_radius"
        lx_option = "Lower_axis_x"
        tx_option = "Top_axis_x"
        ly_option = "Lower_axis_y"
        ty_option = "Top_axis_y"

        try:
            use_axis = config.get(section, use_option)
            radius = config.get(section, radius_option)
            lx = float(config.get(section, lx_option))
            tx = float(config.get(section, tx_option))
            ly = float(config.get(section, ly_option))
            ty = float(config.get(section, ty_option))
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        if use_axis == "True":
            use_axis = True
        else:
            use_axis = False

        if radius == "True":
            radius = True
        else:
            radius = False

        plot_settings = [use_axis, lx, tx, ly, ty, radius, R]

        # create DataStream object for reading the input file
        data_stream = ds.DataStream()
        data_stream.init(outfolder, self)

        # create, initialize then run the implementation of Exact Storm
        exactstorm = es.ExactStorm()
        exactstorm.init(W, R, k, data_stream, st, plot_settings, rescale)
        self.exs = exactstorm
        self.sample = st
        #self.exs = threading.Thread(target = exactstorm.run_exact_storm)
        #self.exs.setDaemon(True)
        #self.exs.start()

    def process(self, tup):
        data = []
        data = tup.values[0].split(",")

        self.exs.run_once(data)

        self.t += 1
        if self.t >= self.sample and self.sample != -1:
            self.exs.sample_outliers_and_plot()
            self.t = 0
        #with self.bufflock:
        #    self.bufferlist.append(data)

"""
test = Exactbolt()
test.initialize("yes","yes")
while(True):
    val = ("1,1,1,1,1")
    tup = storm.Tuple("yes","yes","yes","yes",val)
    test.process(tup)
"""
Exactbolt().run()
