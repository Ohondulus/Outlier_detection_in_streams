import datapoint as dp
import csv
import os
import datetime
import time

# class for handling the stream
class DataStream:
    output = ""
    blist = ""

    datapoint = ""

    # open the input file and create the output folder if it doesn't exist
    def init(self, outputfolder, bufferlist):
        self.blist = bufferlist

        time = datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")
        self.output = outputfolder + time

        try:
            if not os.path.exists(self.output):
                os.makedirs(self.output)
        except Exception as e:
            print("Can't create folder: %s" %e)

    # returns the last read datapoint
    def current_data_point(self):
        return self.datapoint

    # convert the next datapoint
    def set_data_point(self, data):
        point = dp.DataPoint()
        try:
            x = []
            for dim in data:
                x.append(float(dim))

            point.init(x)
            self.datapoint = point
            return True
        except Exception as ex:
            print("Skipping data: %s" %ex)
            return False
