import math


class Queue:

    current = 0
    isInterrupted = False

    def __init__(self, quantum):
        self.quantum = quantum
        self.queue = []
        self.isRunning = False
        self.isFinished = False


class Process:

    counter = 0
    t = 0
    nextArrival = None
    hasNext = False

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
        print("process " + str(self.id) + " \t(" + str(self.arrival) + ") " + '\t\t\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.finish - self.arrival) +'\t\t\t' + str(self.finish)+str(self.isFinished))

    def wait(self):
        self.waiting = self.finish - self.arrival - self.burst

    def assign(self):
        for q in queues:
            if q.queue.__contains__(self) and not queues.index(q) == self.level:
                q.queue.remove(self)
        if not queues[self.level].queue.__contains__(self):
            queues[self.level].queue.append(self)
        if self.checkFinished():
            queues[self.level].queue.remove(self)

    def demote(self):
        if not self.checkFinished():
            if self.level + 1 < len(queues):
                self.level += 1
        self.assign()

    def checkFinished(self):
        if self.remB <= 0:
            self.isFinished = True
        return self.isFinished


level0 = Queue(8)
level1 = Queue(16)
FCFS = Queue(math.inf)
processes = []
queues = [level0, level1, FCFS]


def start():
    processes.sort(key=lambda x: x.arrival)
    Process.t = processes[0].arrival
    nonpreemtiveexecute()
    Queue.current += 1
    while Queue.current < len(queues):
        if not queues[Queue.current].isFinished:
            queues[Queue.current].isRunning = True
            preemptiveexecute(Queue.current)
            queues[Queue.current].isRunning = False
        elif queues[Queue.current].isFinished:
            Queue.current += 1


def getNextArrival():
    for index in range(0, len(processes)):
        if processes[index].arrival > Process.t and not processes[index].arrival == 0:
            Process.nextArrival = index
            return
    Process.nextArrival = None


def nonpreemtiveexecute():
    update()
    tempQueue = queues[0].queue.copy()
    for p in tempQueue:
        if p.remB < queues[0].quantum - p.q:
            executeProcess(p, p.remB, True)
        else:
            executeProcess(p, queues[0].quantum - p.q, True)
    if Process.nextArrival is not None and processes[Process.nextArrival].arrival <= Process.t:
        nonpreemtiveexecute()


def preemptiveexecute(level):
    update()
    tempQueue = queues[level].queue.copy()
    for p in tempQueue:
        if Process.nextArrival is None or processes[Process.nextArrival].arrival >= Process.t + queues[level].quantum - p.q:
            executeProcess(p, queues[level].quantum - p.q, True)
        else:
            while Process.nextArrival is not None and processes[Process.nextArrival].arrival < Process.t + queues[level].quantum - p.q:
                delta = processes[Process.nextArrival].arrival - Process.t
                executeProcess(p, delta, False)
                p.q += delta
                interrupt(processes[Process.nextArrival])
            executeProcess(p, queues[level].quantum - p.q, True)
    queues[level].isRunning = False
    for p in queues[level].queue:
        if p.checkFinished or not p.level == level:
            p.assign()
    if not len(queues[level].queue) == 0:
        Queue.isInterrupted = True
        preemptiveexecute(level)
    if level == Queue.current:
        queues[level].isFinished = True


def executeProcess(p, t, demoted):
    if t <= p.remB:
        Process.t += t
        p.remB -= t
    else:
        Process.t += p.remB
        p.remB = 0
    if p.checkFinished():
        p.finish = Process.t
    if demoted:
        p.q = 0
        p.demote()


def interrupt(p):
    getNextArrival()
    Queue.isInterrupted = True
    p.assign()
    nonpreemtiveexecute()
    while p.level < Queue.current:
        preemptiveexecute(p.level)


def update():
    getNextArrival()
    for p in processes:
        if p.arrival <= Process.t and not p.checkFinished():
            p.assign()


def printAll():
    processes.sort(key=lambda x: x.id)
    print("\n"+"Process no" + " (Arrival time) " + '\t\t' + "Burst " + " Wait " + "Turnaround")
    for p in processes:
        p.wait()
        p.print()


def test():
    Process(30, 12)
    Process(0, 30)
    Process(16, 5)
    Process(6, 10)
    Process(9, 25)
    Process(30, 4)

    start()
    printAll()


test()
