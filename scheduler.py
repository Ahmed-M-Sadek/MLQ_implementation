import math


class Queue:

    currentLive = 0

    def __init__(self, quantum):
        self.quantum = quantum
        self.queue = []


class Process:

    counter = 0
    t = 0
    nextArrival = 0
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
        print("process " + str(self.id) + " \t(" + str(self.arrival) + ") " + '\t\t\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.finish - self.arrival) +'\t' + str(self.remB))

    def wait(self):
        self.waiting = self.finish - self.arrival - self.burst

    def assign(self):
        queues[self.level].queue.append(self)

    def demote(self):
        if not self.isFinished:
            if self.level + 1 < len(queues):
                self.level += 1
                self.assign()


level0 = Queue(8)
level1 = Queue(16)
FCFS = Queue(math.inf)
processes = []
queues = [level0, level1, FCFS]
isInterrupted = False


def start():
    processes.sort(key=lambda x: x.arrival)
    execute(0)


def getNextArrival():

    if Process.nextArrival + 1 < len(processes) and processes[Process.nextArrival + 1].arrival > processes[Process.nextArrival].arrival:
        Process.nextArrival += 1
        Process.hasNext = True
    else:
        Process.hasNext = False


def execute(level):
    isInterrupted = False
    update()
    print("fml "+str(Process.hasNext))
    if len(queues[level].queue) > 0:
        for p in queues[level].queue:
            if not Process.hasNext:
                if p.remB > queues[level].quantum - p.q:
                    Process.t += queues[level].quantum - p.q
                    p.remB -= (queues[level].quantum - p.q)
                    p.demote()
                    print(str(p.id) + ' kill moi 1 ' + str(Process.t))
                elif p.remB <= queues[level].quantum - p.q:
                    Process.t += p.remB
                    p.remB = 0
                    p.isFinished = True
                    p.finish = Process.t
                    p.q = 0
                    print(str(p.id) + ' kill moi 2 ' + str(Process.t))
            elif not level == 0:
                delta = processes[Process.nextArrival].arrival - Process.t
                p.remB -= delta
                Process.t += delta
                p.q = delta
                isInterrupted = True
                print(str(p.id) + ' kill moi 3 ' + str(p.remB))
                break
            else:
                Process.t += queues[level].quantum - p.q
                p.remB = max(0, p.remB -( queues[level].quantum - p.q))
                p.demote()
                isInterrupted = False
                p.isFinished = True
                print(str(p.id) + ' kill moi 4 ' + str(p.remB))

        print(isInterrupted)
        if isInterrupted:
            processes[Process.nextArrival].assign()
            interrupt()
    if level + 1 < len(queues):
        Queue.currentLive += 1
        execute(level + 1)


def interrupt():
    level = 0
    while level < Queue.currentLive:
        for p in queues[level].queue:
            if not Process.hasNext:
                if p.remB > queues[level].quantum - p.q:
                    Process.t += queues[level].quantum - p.q
                    p.remB -= p.remB - (queues[level].quantum - p.q)
                    p.demote()
                    print('kill moi 1')
                elif p.remB <= queues[level].quantum - p.q:
                    Process.t += p.remB
                    p.remB = 0
                    p.isFinished = True
                    p.finish = Process.t
                    p.q = 0
                    print('kill moi 2')
            elif not level == 0:
                delta = processes[Process.nextArrival].arrival - Process.t
                p.remB -= delta
                Process.t += delta
                p.q = delta
                print('kill moi 3')
                break
            else:
                Process.t += queues[level].quantum - p.q
                p.remB -= p.remB - (queues[level].quantum - p.q)
                p.demote()
                print('kill moi 4')
                p.isFinished = True
                break
        level += 1


def update():
    getNextArrival()
    remove = []
    for q in queues:
        for p in q.queue:
            if p.isFinished:
                remove.append((q, p))
    for item in remove:
        item[0].queue.remove(item[1])
    for p in processes:
        if not (queues[p.level].queue.__contains__(p) or (p.remB <= 0)) and p.arrival <= Process.t:
            queues[p.level].queue.append(p)
            p.isFinished = False


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
