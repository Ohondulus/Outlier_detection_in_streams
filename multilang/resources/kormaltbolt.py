import storm
import korm.datastream as ds
import korm.kormalt as kr
import ConfigParser as cp

class Kormbolt(storm.BasicBolt):
    korm = ""

    chunk = []
    Num = 0
    
    def initialize(self, stormconf, context):
        config = cp.ConfigParser()

        configfile = "/home/ohondulus/Downloads/korm_config.ini"

        outfolder = "/home/ohondulus/Downloads/pngs"
        
        # read the config file
        try:
            config.read(configfile)
        except Exception as e:
            print("Can't read the configfile: %s" %e)

        # extract korm settings from config file
        section = "KormSettings"
        n_option = "Total_number_of_points"
        k_option = "Minimum_median_count"
        P_option = "Phases"
        O_option = "Temp_outlier_tests"
        gamma_option = "Gamma"
        beta_option = "Beta"
        Num_option = "Num_points_in_chunk"
        st_option = "Sample_phase"

        try:
            n = int(config.get(section, n_option))
            k = int(config.get(section, k_option))
            P = int(config.get(section, P_option))
            O = int(config.get(section, O_option))
            gamma = int(config.get(section, gamma_option))
            beta = int(config.get(section, beta_option))
            Num = int(config.get(section, Num_option))
            st = float(config.get(section, st_option))
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        # extract plot settings from the config file
        section = "PlotSettings"
        use_option = "Use_axis"
        sample_ofl_option = "Sample_online_fl"
        sample_clu_option = "Sample_cluster"
        lx_option = "Lower_axis_x"
        tx_option = "Top_axis_x"
        ly_option = "Lower_axis_y"
        ty_option = "Top_axis_y"

        try:
            use_axis = config.get(section, use_option)
            sample_ofl = config.get(section, sample_ofl_option)
            sample_clu = config.get(section, sample_clu_option)
            lx = int(config.get(section, lx_option))
            tx = int(config.get(section, tx_option))
            ly = int(config.get(section, ly_option))
            ty = int(config.get(section, ty_option))
        except Exception as e:
            print("Exception in the configfile options: %s" %e)

        if use_axis == "True":
            use_axis = True
        else:
            use_axis = False

        if sample_ofl == "True":
            sample_ofl = True
        else:
            sample_ofl = False

        if sample_clu == "True":
            sample_clu = True
        else:
            sample_clu = False

        plot_settings = [use_axis, sample_ofl, sample_clu, lx, tx, ly, ty]

        # create DataStream object for reading the input file
        data_stream = ds.DataStream()
        data_stream.init(outfolder, n, Num, st)

        # create, initialize then run the implementation of Korm
        self.korm = kr.Korm()
        self.korm.init(data_stream, n, k, P, O, gamma, beta, Num, st, plot_settings)

        self.Num = Num
        #self.korm.run_korm()

    def process(self, tup):
        data = []
        val = tup.values[0].split(",")
        data.append(float(val[0]))
        data.append(float(val[1]))

        self.chunk.append(data)

        if len(self.chunk) >= self.Num:
            self.korm.run_once(self.chunk)
            self.chunk = []

"""
test = Kormbolt()
test.initialize("yes","yes")
while(True):
    tup = storm.Tuple("yes","yes","yes","yes",(1,1))
    test.process(tup)
"""

import csv
test = Kormbolt()
test.initialize("yes","yes")
c = "/home/ohondulus/Downloads/ma1.csv"
first = True
with open(c, "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for row in reader:
        if first:
            first = False
            test.korm.kp.lx = float(row[2])
            test.korm.kp.tx = float(row[3])
            test.korm.kp.ly = float(row[4])
            test.korm.kp.ty = float(row[5])
        x = row[0]
        y = row[1]
        val = [("%s,%s" %(x,y))]
        tup = storm.Tuple("yes","yes","yes","yes",val)
        test.process(tup)

errnum = 0
pnum = 0
for c in test.korm.real_out:
    errnum = errnum + c.weight
    pnum = pnum + c.weight

for c in test.korm.facils:
    pnum = pnum + c.weight

for c in test.korm.safe_out:
    pnum = pnum + c.weight

print(errnum)
print(pnum)

#Kormbolt().run()
