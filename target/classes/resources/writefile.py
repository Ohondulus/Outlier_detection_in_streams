import storm

class writefile(storm.BasicBolt):
    x = 0
    def process(self, tup):
        self.x += 1

        with open("/home/ohondulus/Downloads/test.txt", "a") as test:
            test.write("X: %s\n" %(self.x))

writefile().run()
