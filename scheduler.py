queue1 = []
queue2 = []
queue3 = []
processes = []


class Process:

    counter = 0
    t = 0

    def __init__(self, burst):
        self.waiting = 0
        self.burst = burst
        self.remB = self.burst
        self.isFinished = False
        Process.counter += 1
        self.id = Process.counter
        self.finish = 0

    def print(self):
        print("process " + str(self.id) + '\t\t' + str(self.burst) + '\t\t' + str(self.waiting) + '\t\t' + str(self.waiting + self.burst))

    def wait(self):
        self.waiting = self.finish - self.burst


def roundRobin(queue, quantum):
    for p in queue:
        Process.t += min(p.remB, quantum)
        p.remB = max(p.remB - quantum, 0)

        if p.remB <= 0:
            p.isFinished = True
            p.finish = Process.t


def promote(queueL, queueH):
    for p in queueL:
        if not p.isFinished:
            queueH.append(p)


def fcfs():
    for p in queue3:
        Process.t += p.remB
        p.remB = 0
        p.isFinished = True
        p.finish = Process.t


def printAll():
    print("Process no" + '\t\t' + "Burst " + " Wait " + "Turnaround" + "\n")
    for p in processes:
        p.wait()
        p.print()


def test():
    p1 = Process(8)
    p2 = Process(26)
    p3 = Process(10)
    p4 = Process(6)

    processes.extend([p1, p2, p3, p4])

    promote(processes, queue1)
    roundRobin(queue1, 8)
    promote(queue1, queue2)
    roundRobin(queue2, 16)
    promote(queue2, queue3)
    fcfs()

    printAll()


test()