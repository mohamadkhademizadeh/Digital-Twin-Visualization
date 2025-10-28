import simpy, random, math

class Item:
    _id = 0
    def __init__(self, t0):
        self.id = Item._id; Item._id += 1
        self.t0 = t0
        self.t_finish = None
        self.failed_qc = False

class Cell:
    def __init__(self, env, arrival_rate, process_time_mean, qc_fail_prob, breakdown_mtf, repair_time_mean, rng=None):
        self.env = env
        self.rng = rng or random.Random(7)
        self.arrival_rate = arrival_rate
        self.process_time_mean = process_time_mean
        self.qc_fail_prob = qc_fail_prob
        self.breakdown_mtf = breakdown_mtf
        self.repair_time_mean = repair_time_mean

        self.queue = simpy.Store(env)
        self.busy = False
        self.up = True
        self.timeline = []  # (t, state)
        self.throughput = 0
        self.scrap = 0
        self.util_time = 0.0
        self.last_state_change = 0.0

        env.process(self.source())
        env.process(self.machine())
        env.process(self.breakdowns())

    def set_state(self, state):
        self.timeline.append((self.env.now, state))

    def source(self):
        while True:
            # exponential inter-arrival
            dt = self.rng.expovariate(self.arrival_rate) if self.arrival_rate>0 else 1e9
            yield self.env.timeout(dt)
            yield self.queue.put(Item(self.env.now))

    def machine(self):
        self.set_state('IDLE')
        while True:
            itm = yield self.queue.get()
            # wait until machine is up
            while not self.up:
                yield self.env.timeout(0.1)
            self.busy = True; st = self.env.now; self.set_state('BUSY')
            # process
            pt = max(0.1, self.rng.expovariate(1.0/self.process_time_mean))
            yield self.env.timeout(pt)
            # qc
            if self.rng.random() < self.qc_fail_prob:
                self.scrap += 1
                itm.failed_qc = True
            else:
                self.throughput += 1
                itm.t_finish = self.env.now
            self.busy = False; self.set_state('IDLE')

    def breakdowns(self):
        while True:
            ttf = max(1.0, self.rng.expovariate(1.0/self.breakdown_mtf))
            yield self.env.timeout(ttf)
            self.up = False; self.set_state('DOWN')
            r = max(0.5, self.rng.expovariate(1.0/self.repair_time_mean))
            yield self.env.timeout(r)
            self.up = True; self.set_state('IDLE' if not self.busy else 'BUSY')

def run_once(cfg, seed=7):
    rng = random.Random(seed)
    env = simpy.Environment()
    cell = Cell(env, cfg['arrival_rate'], cfg['process_time_mean'], cfg['qc_fail_prob'], cfg['breakdown_mtf'], cfg['repair_time_mean'], rng)
    env.run(until=cfg['duration_min'])
    return dict(throughput=cell.throughput, scrap=cell.scrap, timeline=cell.timeline)
