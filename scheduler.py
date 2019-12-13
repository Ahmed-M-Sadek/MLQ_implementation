from collections import deque
import math

level0 = deque()
level1 = deque()
FCFS = deque()
processes = []
queues = [level0, level1, FCFS]


class Process:

    counter = 0
    t = 0

    def __init__(self, arrival, burst):
        self.waiting = 0
        self.arrival = arrival
        self.burst = burst
        self.remB = self.burst
        self.isFinished = False
        Process.counter += 1
        self.id = Process.counter
        self.finish = 0
        self.level = 0
        processes.append(self)

    def print(self):
        print("process " + str(self.id) + " \t(" + str(self.arrival) + ") " + '\t\t\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.finish - self.arrival))

    def wait(self):
        self.waiting = self.finish - self.arrival - self.burst

    def assign(self):
        queues[self.level].append(self)

    def promote(self):
        if not self.isFinished:
            if self.level + 1 < len(queues):
                self.level += 1
                self.assign()


def roundRobin(level, quantum):
    ar = checkNextArrival()
    checkProcessesLevels()
    for p in (queues[level]):
        if p.level == level:
            if Process.t + p.remB > ar and not level == 0:
                p.remB -= (ar - Process.t)
                execute(0)
                break
            Process.t += min(p.remB, quantum)
            p.remB = max(p.remB - quantum, 0)
            if p.remB <= 0:
                p.isFinished = True
                p.finish = Process.t
            p.promote()
    queues[level].clear()
    execute(level + 1)


def checkProcessesLevels():
    for p in processes:
        if p.arrival <= Process.t and not queues[p.level].__contains__(p):
            queues[p.level].append(p)


def fcfs():
    ar = checkNextArrival()
    for p in queues[len(queues) - 1]:
        if Process.t + p.burst > ar:
            p.remB -= (ar - Process.t)
            execute(0)
            break
        Process.t += p.remB
        p.remB = 0
        p.isFinished = True
        p.finish = Process.t


def execute(level):
    level = max(0, level)
    if level < len(queues) - 1:
        roundRobin(level, 8 + level * 8)
    else:
        fcfs()


def printAll():
    print("\n"+"Process no" + " (Arrival time) " + '\t\t' + "Burst " + " Wait " + "Turnaround")
    for p in processes:
        p.wait()
        p.print()


def checkNextArrival():
    for p in processes:
        if p.arrival > Process.t:
            return p.arrival
    return math.inf


def test():
    Process(25, 9)
    Process(0, 26)
    Process(3, 10)
    Process(9, 6)

    execute(0)

    printAll()


test()
