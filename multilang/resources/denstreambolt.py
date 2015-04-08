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
        st_option = "sample_time"

        try:
            beta = float(config.get(section, beta_option))
            mu = float(config.get(section, mu_option))
            lamb = float(config.get(section, lambda_option))
            epsilon = float(config.get(section, epsilon_option))
            st = float(config.get(section, st_option))
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
        data_stream.init(outfolder, self, do_plot)

        # create, initialize then run the implementation of DenStream
        denstream = dens.DenStream()
        denstream.init(data_stream, beta, mu, lamb, epsilon, do_plot, st, plot_settings)
        self.denstream = denstream

    def process(self, tup):
        data = []
        data = tup.values[0].split(",")

        self.denstream.run_once(data, 0.01)

"""
import random
test = DenStreambolt()
test.initialize("yes","yes")
for i in range(200):
    #x = random.random()
    #y = random.random()
    x = random.randint(0,100)
    y = random.randint(0,100)
    val = ("%s,%s"%(x,y))
    tup = storm.Tuple("yes","yes","yes","yes",val)
    test.process(tup)
"""
"""
import csv
test = DenStreambolt()
test.initialize("yes","yes")
c = "/home/ohondulus/Downloads/ma1.csv"
with open(c, "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for row in reader:
        x = row[0]
        y = row[1]
        val = [("%s,%s" %(x,y))]
        tup = storm.Tuple("yes","yes","yes","yes",val)
        test.process(tup)
num = 0
for clus in test.denstream.MClusters:
    num = num + clus.pnum

print(test.denstream.errnum)
print(test.denstream.pnum + num)
"""
DenStreambolt().run()
