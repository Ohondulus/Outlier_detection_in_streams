import datapoint as dp
import csv
import os
import datetime

# class for handling the stream
class DataStream:
    currentChunk = []
    chunkSize = 0
    maxSize = 0
    current = 1

    output = ""

    # open the input file and create the output folder if it doesn't exist
    def init(self, outputfolder, n, Num):
        self.chunkSize = Num
        self.maxSize = n

        time = datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")
        self.output = outputfolder + time

        try:
            if not os.path.exists(self.output):
                os.makedirs(self.output)
        except Exception as e:
            print("Can't create folder: %s" %e)

    # returns true if the next datapoints has been succesfully read
    def process_data(self, chunk):
        self.currentChunk = []
        for data in chunk:
            try:
                point = dp.DataPoint()
                x = float(data[0])
                y = float(data[1])
                point.init(x, y)

                self.currentChunk.append(point)
                self.current += 1

            except Exception as e:
                continue

        return True

    # returns the last read datapoints
    def current_chunk(self):
        return self.currentChunk
