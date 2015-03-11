import storm
import denstream.datastream as ds
import denstream.denstream as dens
import ConfigParser as cp

class DenStreambolt(storm.BasicBolt):
    denstream = ""

    sample = 0
    t = 0
    
    def initialize(self, stormconf, context):
        config = cp.ConfigParser()

        configfile = "/home/ohondulus/Downloads/ds_config.ini"

        outfolder = "/home/ohondulus/Downloads/pngs"
        
        # read the config file
        try:
            config.read(configfile)
        except Exception as e:
            print("Can't read the configfile: %s" %e)

        # extract exact storm settings from config file
        section = "DenStreamSettings"
        beta_option = "beta"
        mu_option = "mu"
        lambda_option = "lambda"
        epsilon_option = "epsilon"

        try:
            beta = float(config.get(section, beta_option))
            mu = float(config.get(section, mu_option))
            lamb = float(config.get(section, lambda_option))
            epsilon = float(config.get(section, epsilon_option))
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        # exact plot settings from the config file
        section = "PlotSettings"
        do_plot_option = "Do_plot"
        use_option = "Use_axis"
        radius_option = "Show_radius"
        lx_option = "Lower_axis_x"
        tx_option = "Top_axis_x"
        ly_option = "Lower_axis_y"
        ty_option = "Top_axis_y"

        try:
            do_plot = config.get(section, do_plot_option)
            use_axis = config.get(section, use_option)
            radius = config.get(section, radius_option)
            lx = float(config.get(section, lx_option))
            tx = float(config.get(section, tx_option))
            ly = float(config.get(section, ly_option))
            ty = float(config.get(section, ty_option))
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        if do_plot == "True":
            do_plot = True
        else:
            do_plot = False

        if use_axis == "True":
            use_axis = True
        else:
            use_axis = False

        if radius == "True":
            radius = True
        else:
            radius = False

        plot_settings = [use_axis, lx, tx, ly, ty, radius]

        # create DataStream object for reading the input file
        data_stream = ds.DataStream()
        data_stream.init(outfolder, self)

        # create, initialize then run the implementation of DenStream
        denstream = dens.DenStream()
        denstream.init(data_stream, beta, mu, lamb, epsilon, do_plot, plot_settings)
        self.denstream = denstream

    def process(self, tup):
        data = []
        data = tup.values[0].split(",")

        self.denstream.run_once(data)


'''
test = DenStreambolt()
test.initialize("yes","yes")
while(True):
    val = ("1,1,1,1,1")
    tup = storm.Tuple("yes","yes","yes","yes",val)
    test.process(tup)
'''
DenStreambolt().run()
