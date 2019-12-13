from collections import deque
import math


class queue:

    def __init__(self, quantum):
        self.quantum = quantum
        self.queue = deque()


class Process:

    counter = 0
    t = 0
    nextArrival = None

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
        self.q = 0
        processes.append(self)

    def print(self):
        print("process " + str(self.id) + " \t(" + str(self.arrival) + ") " + '\t\t\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.finish - self.arrival))

    def wait(self):
        self.waiting = self.finish - self.arrival - self.burst

    def assign(self):
        queues[self.level].append(self)

    def demote(self):
        if not self.isFinished:
            if self.level + 1 < len(queues):
                self.level += 1
                self.assign()


level0 = queue(8)
level1 = queue(16)
FCFS = queue(math.inf)
processes = []
queues = [level0, level1, FCFS]


def start():
    processes.sort(key=lambda x: x.arrival)
    execute(0)


def getNextArrival(offset):
    for p in processes:
        if p.arrival > Process.t + offset:
            if not p == Process.nextArrival:
                Process.nextArrival = p
            break


def execute(level):
    isInterrupted = False
    for p in processes:
        if p.level == level and not p.isFinished:
            queues[level].append(p)
    for p in queues[level]:
        if p.remB > queues[level].quantum - p.q and Process.nextArrival.arrival > Process.t + queues[level].quantum - p.q:
            Process.t += queues[level].quantum - p.q
            p.remB = max(0, p.remB - queues[level].quantum - p.q)
            p.demote()
        elif p.remB <= queues[level].quantum - p.q and Process.nextArrival.arrival > Process.t + queues[level].quantum - p.q:
            Process.t += p.remB
            p.remB = 0
            p.isFinished = True
            p.q = 0
        elif not level == 0:
            delta = Process.nextArrival.arrival - Process.t
            p.remB -= delta
            Process.t += delta
            p.q = delta
            isInterrupted = True
            break
        else:
            Process.t += queues[level].quantum - p.q
            p.remB = max(0, p.remB - queues[level].quantum - p.q)
            p.demote()
            isInterrupted = True
            break
    if isInterrupted:
        Process.nextArrival.assign()
        interrupt()


def interrupt():
    execute(0)


def printAll():
    for p in processes:
        print(str(p.id) + "\t" + str(p.arrival))


def test():
    Process(25, 9)
    Process(0, 26)
    Process(3, 10)
    Process(9, 6)

    printAll()


test()
