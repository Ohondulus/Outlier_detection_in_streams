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
    time_id = 0

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

    # returns true if the next datapoint has been succesfully read
    def next(self):
        while True:
            data = "nodata"
            with self.blist.bufflock:
                if self.blist.bufferlist:
                    data = self.blist.bufferlist.pop(0)

            if data == "nodata":
                msec = 1 / 1000
                time.sleep(msec)
            else:
                point = dp.DataPoint()
                try:
                    x = float(data[0])
                    y = float(data[1])

                    self.time_id += 1
                    point_id = self.time_id

                    point.init(x,y, point_id)
                    self.datapoint = point
                    return True
                except Exception as ex:
                    print("Skipping data: %s" %ex)

    # returns the last read datapoint
    def current_data_point(self):
        return self.datapoint

    def set_data_point(self, data):
        point = dp.DataPoint()
        try:
            x = float(data[0])
            y = float(data[1])

            self.time_id += 1
            point_id = self.time_id

            point.init(x,y, point_id)
            self.datapoint = point
            return True
        except Exception as ex:
            print("Skipping data: %s" %ex)
            return False
