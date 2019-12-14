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
        print("process " + str(self.id) + " \t(" + str(self.arrival) + ") " + '\t\t\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.finish - self.arrival) +'\t' + str(self.finish))

    def wait(self):
        self.waiting = self.finish - self.arrival - self.burst

    def assign(self):
        if not queues[self.level].queue.__contains__(self):
            queues[self.level].queue.append(self)

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
    while Queue.current < len(queues):
        if not queues[Queue.current].isFinished:
            queues[Queue.current].isRunning = True
            execute(Queue.current)
        elif queues[Queue.current].isFinished:
            Queue.current += 1


def getNextArrival():
    for index in range(0, len(processes)):
        if processes[index].arrival > Process.t and not processes[index].arrival == 0:
            Process.nextArrival = index
            return
    Process.nextArrival = None


def execute(level):
    if level > Queue.current:
        return
    update()
    tempQueue = queues[level].queue.copy()
    for p in tempQueue:
        if Process.nextArrival is not None:
            if processes[Process.nextArrival].arrival > Process.t + queues[level].quantum - p.q:
                if p.remB >= queues[level].quantum - p.q:
                    Process.t += queues[level].quantum - p.q
                    p.remB -= queues[level].quantum - p.q
                    p.demote()
                    p.q = 0
                else:
                    Process.t += p.remB
                    p.remB = 0
                    p.q = 0
                    queues[level].queue.remove(p)
                    if p.checkFinished():
                        p.finish = Process.t
                    else:
                        p.demote()

            else:
                if level > 0:
                    delta = processes[Process.nextArrival].arrival - Process.t
                    p.q += delta
                    p.remB -= delta
                    if p.checkFinished():
                        p.finish = Process.t
                    Process.t += delta
                    Queue.isInterrupted = True
                    interrupt(processes[Process.nextArrival], level, p)

                else:
                    Process.t += queues[level].quantum - p.q
                    p.remB -= queues[level].quantum - p.q
                    p.demote()
                    p.q = 0
                    queues[0].queue.append(processes[Process.nextArrival])
                    getNextArrival()
        else:
            if p.remB >= queues[level].quantum - p.q:
                Process.t += queues[level].quantum - p.q
                p.remB -= queues[level].quantum - p.q
                p.demote()
                p.q = 0
                queues[level].queue.remove(p)
            else:
                Process.t += p.remB
                p.remB = 0
                p.q = 0
                queues[level].queue.remove(p)
                if p.checkFinished():
                    p.finish = Process.t
                else:
                    p.demote()

    queues[level].isRunning = False
    for p in queues[level].queue:
        if p.checkFinished or not p.level == level:
            queues[level].queue.remove(p)
    if not len(queues[level].queue) == 0:
        Queue.isInterrupted = True
        execute(level)
    if level == Queue.current:
        queues[level].isFinished = True


def interrupt(p,  level, po):
    Queue.isInterrupted = True
    if level == 0:
        queues[0].queue.append(p)
        getNextArrival()
        return
    else:
        p.assign()
        execute(0)
        if Queue.current > 1:
            execute(1)
    continueProcess(po, queues[level])


def continueProcess(p, q):
    if Process.nextArrival is not None:
        if processes[Process.nextArrival].arrival >= Process.t + q.quantum - p.q:
            if p.remB >= q.quantum - p.q:
                Process.t += q.quantum - p.q
                p.remB -= q.quantum - p.q
                p.demote()
                p.q = 0
            else:
                Process.t += p.remB
                p.remB = 0
                p.q = 0
                if p.checkFinished():
                    p.finish = Process.t
                else:
                    p.demote()
        else:
            Process.t += q.quantum - p.q
            p.remB -= q.quantum - p.q
            p.demote()
            p.q = 0
            queues[0].queue.append(processes[Process.nextArrival])
            getNextArrival()
    else:
        if p.remB >= q.quantum - p.q:
            Process.t += q.quantum - p.q
            p.remB -= q.quantum - p.q
            p.demote()
            p.q = 0
        else:
            Process.t += p.remB
            p.remB = 0
            p.q = 0
            if p.checkFinished():
                p.finish = Process.t
            else:
                p.demote()


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
    Process(25, 9)
    Process(0, 26)
    Process(3, 10)
    Process(9, 6)
    start()
    printAll()


test()
