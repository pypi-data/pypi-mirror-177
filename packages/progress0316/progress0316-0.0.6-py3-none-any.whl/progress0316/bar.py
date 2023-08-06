from time import time as ltime1234567

class ProgressBar():
    __fill = '█'

    def __init__(self, iterations, barLength = 40):
        self.__iterations = iterations
        self.__counter = 0
        self.__start = ltime1234567()
        self.__end = False
        self.__total_time = 0
        self.__frequency = 1
        self.__freq10 = 1
        self.__bar_length = barLength-1
    
    def __fill_fun(self, val):
        if val<0.001: return '█'
        if val<0.125: return '▏'
        if val<0.25: return '▎'
        if val<0.375: return '▍'
        if val<0.5: return '▌'
        if val<0.625: return '▋'
        if val<0.75: return '▊'
        if val<0.875: return '▉'
        return '█'

    def __update(self):
        percent = 100*(self.__counter / float(self.__iterations))
        self.__total_time = ltime1234567() - self.__start
        self.__frequency = self.__counter / self.__total_time
        self.__freq10 = int(self.__frequency / 10)
        if self.__freq10 == 0: self.__freq10 = 1
        eta = int((100.0/percent)*self.__total_time) - int(self.__total_time)
        mins = ""
        if eta >= 60:
            mins = eta//60
            mins = str(mins) + "mins "
            eta = eta%60
        eta = mins + str(eta)
        frequency = "{:.2f}".format(self.__frequency)
        spercent = "{:.2f}".format(percent)
        filledLength = self.__bar_length * self.__counter // self.__iterations
        factor = (self.__bar_length * self.__counter / self.__iterations) - (self.__bar_length * self.__counter // self.__iterations)
        # bar = '|' + (self.__fill * filledLength) + '-' * (self.__bar_length - filledLength) + '|'
        
        bar = '|' + (self.__fill * (filledLength)) + self.__fill_fun(factor) + ' ' * (self.__bar_length - filledLength) + '|'       
        if not self.__end:
            print(f'\r{bar} [{spercent}]% (eta: {eta}s, frequency: {frequency}/s)'+7*" ", end = '', flush = True)
        else:
            if self.__total_time >= 60:
                mins = self.__total_time//60
                secs = int(self.__total_time%60)
                totalTime = str(mins) +" mins " + str(secs) + " seconds"
            else:
                totalTime = str(int(self.__total_time)) + " seconds"
            print(f'\r{bar} [100.00]% (total time: {totalTime})'+(20)*" ")

    def next(self):
        self.__counter += 1
        if not self.__end:
            if self.__counter == self.__iterations:
                self.__end = True
                self.__update()
                return
            if self.__frequency > 100000:
                if self.__counter % 100000 == 0:
                    self.__update()
            elif self.__frequency<self.__iterations:
                if self.__counter % self.__freq10 == 0:
                    self.__update()
            elif self.__counter <= 10:
                self.__update()

def bar(iterations): return ProgressBar(iterations)
