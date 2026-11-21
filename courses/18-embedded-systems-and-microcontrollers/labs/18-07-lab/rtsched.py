"""Lab 18-07: a discrete-time simulator of a single-core real-time kernel, and the classical schedulability tests.

Simulator: integer time steps (think of one step as a millisecond or a microsecond). Periodic tasks release jobs at
offset + k * period with a deadline one period later (implicit deadlines unless given). Each job runs a script of
segments, each (duration, mutex or None); a segment with a mutex must acquire it first and releases it at its end.
Policies:
- "fp": preemptive fixed priority (higher number = higher priority);
- "edf": preemptive earliest deadline first (ties: lower task index first).
Mutex protocols (fixed priority only): "none", "inherit" (a holder runs at the highest priority of the jobs it
blocks) and "ceiling" (immediate priority ceiling: a holder runs at the highest base priority of any task that uses
the mutex).

Analysis: utilization, the Liu & Layland bound n(2^(1/n) - 1), hyperbolic bound, exact response-time analysis with
blocking, and the rate-monotonic priority assignment.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    period: int
    script: list            # [(duration, mutex_name_or_None), ...]
    priority: int = 0
    offset: int = 0
    deadline: int | None = None
    max_jobs: int | None = None   # release at most this many jobs (None: periodic forever)

    @property
    def wcet(self) -> int:
        return sum(d for d, _ in self.script)

    @property
    def rel_deadline(self) -> int:
        return self.period if self.deadline is None else self.deadline


@dataclass
class Job:
    task: int
    release: int
    deadline: int
    segs: list
    seg: int = 0
    left: int = 0
    holding: str | None = None
    finish: int | None = None

    def __post_init__(self):
        self.left = self.segs[0][0] if self.segs else 0


@dataclass
class Result:
    response: dict = field(default_factory=dict)      # task name -> list of response times
    misses: dict = field(default_factory=dict)        # task name -> number of deadline misses
    trace: list = field(default_factory=list)         # per time step: task name or None (idle)
    blocked: dict = field(default_factory=dict)       # task name -> steps spent ready but blocked on a mutex

    def worst(self, name: str) -> int:
        return max(self.response[name]) if self.response[name] else 0


def simulate(tasks: list[Task], horizon: int, policy: str = "fp", protocol: str = "none") -> Result:
    ceilings = {}
    for t in tasks:
        for _, m in t.script:
            if m is not None:
                ceilings[m] = max(ceilings.get(m, -math.inf), t.priority)
    owner: dict[str, Job] = {}
    jobs: list[Job] = []
    res = Result(response={t.name: [] for t in tasks}, misses={t.name: 0 for t in tasks},
                 blocked={t.name: 0 for t in tasks})
    released = [0] * len(tasks)

    def eff_prio(j: Job) -> float:
        if policy == "edf":
            return -j.deadline - j.task * 1e-6
        p = tasks[j.task].priority
        if j.holding is not None:
            if protocol == "ceiling":
                p = max(p, ceilings[j.holding])
            elif protocol == "inherit":
                for o in jobs:
                    if o is not j and o.finish is None and o.release <= now and _wants(o) == j.holding:
                        p = max(p, tasks[o.task].priority)
        return p

    def _wants(j: Job):
        if j.seg < len(j.segs) and j.holding is None:
            m = j.segs[j.seg][1]
            return m
        return None

    now = 0
    for now in range(horizon):
        for i, t in enumerate(tasks):
            if now >= t.offset and (now - t.offset) % t.period == 0 and (t.max_jobs is None or released[i] < t.max_jobs):
                jobs.append(Job(i, now, now + t.rel_deadline, list(t.script)))
                released[i] += 1
        active = [j for j in jobs if j.finish is None]
        for j in active:
            if now == j.deadline:
                res.misses[tasks[j.task].name] += 1
        # a job can run if its next segment needs no mutex, or the mutex is free or its own
        runnable = []
        for j in active:
            m = _wants(j)
            if m is not None and m in owner and owner[m] is not j:
                res.blocked[tasks[j.task].name] += 1
                continue
            runnable.append(j)
        if not runnable:
            res.trace.append(None)
            continue
        if protocol == "ceiling" and policy == "fp":
            # immediate ceiling: a job may only lock if its priority beats every ceiling held by others
            def can_start(j):
                m = _wants(j)
                if m is None:
                    return True
                others = [ceilings[h.holding] for h in active if h is not j and h.holding is not None]
                return not others or tasks[j.task].priority > max(others)
            runnable = [j for j in runnable if j.holding is not None or can_start(j)] or runnable
        run = max(runnable, key=lambda j: (eff_prio(j), -j.release))
        m = _wants(run)
        if m is not None:
            owner[m] = run
            run.holding = m
        res.trace.append(tasks[run.task].name)
        run.left -= 1
        while run.left == 0 and run.finish is None:
            if run.holding is not None:
                del owner[run.holding]
                run.holding = None
            run.seg += 1
            if run.seg >= len(run.segs):
                run.finish = now + 1
                res.response[tasks[run.task].name].append(run.finish - run.release)
            else:
                run.left = run.segs[run.seg][0]
    return res


# ------------------------------------------------------------------ analysis
def utilization(tasks: list[Task]) -> float:
    return sum(t.wcet / t.period for t in tasks)


def ll_bound(n: int) -> float:
    """Liu & Layland: n tasks with implicit deadlines are RM-schedulable if U <= n (2^(1/n) - 1)."""
    return n * (2 ** (1 / n) - 1)


def hyperbolic_ok(tasks: list[Task]) -> bool:
    """Bini, Buttazzo & Buttazzo: RM-schedulable if prod(U_i + 1) <= 2."""
    return math.prod(t.wcet / t.period + 1 for t in tasks) <= 2 + 1e-12


def rm_priorities(tasks: list[Task]) -> list[Task]:
    """Assign rate-monotonic priorities: shorter period, higher priority."""
    order = sorted(range(len(tasks)), key=lambda i: tasks[i].period)
    for rank, i in enumerate(order):
        tasks[i].priority = len(tasks) - rank
    return tasks


def response_time(tasks: list[Task], i: int, blocking: float = 0.0, jitter_free: bool = True) -> float | None:
    """Exact worst-case response time of task i under preemptive fixed priority:
    R = C_i + B_i + sum_{j in hp(i)} ceil(R / T_j) C_j, iterated from R = C_i + B_i. None if it exceeds the deadline."""
    t = tasks[i]
    hp = [o for o in tasks if o.priority > t.priority]
    r = t.wcet + blocking
    while True:
        r_new = t.wcet + blocking + sum(math.ceil(r / o.period) * o.wcet for o in hp)
        if r_new == r:
            return r
        if r_new > t.rel_deadline:
            return None
        r = r_new


def blocking_ceiling(tasks: list[Task], i: int) -> int:
    """Worst blocking of task i under a ceiling protocol: the longest critical section of a lower-priority task on a
    mutex whose ceiling is at least task i's priority (one such section at most)."""
    t = tasks[i]
    ceil = {}
    for o in tasks:
        for _, m in o.script:
            if m is not None:
                ceil[m] = max(ceil.get(m, -math.inf), o.priority)
    worst = 0
    for o in tasks:
        if o.priority < t.priority:
            for d, m in o.script:
                if m is not None and ceil[m] >= t.priority:
                    worst = max(worst, d)
    return worst


# ------------------------------------------------------------------ queues
def queue_max_occupancy(period: int, horizon: int, stalls: list[tuple[int, int]], offset: int = 0) -> int:
    """A producer adds one item at offset + k * period; a consumer removes everything at once whenever it is not
    stalled (stalls are (start, length) intervals in which it cannot run). Returns the largest number of items
    waiting at any time."""
    blocked = set()
    for s, n in stalls:
        blocked.update(range(s, s + n))
    q = best = 0
    for t in range(horizon):
        if t >= offset and (t - offset) % period == 0:
            q += 1
            best = max(best, q)
        if t not in blocked:
            q = 0
    return best


def two_task_min_utilization(t1: int = 1000, ratios=None):
    """Numerically find the smallest utilization of a just-schedulable two-task RM set with T1 = t1: for each T2
    (T1 < T2 < 2 T1) and each C1, take the largest C2 meeting task 2's deadline, and minimize C1/T1 + C2/T2.
    Returns (U_min, T2/T1 at the minimum)."""
    best = (2.0, None)
    for t2 in (ratios if ratios is not None else range(t1 + 1, 2 * t1)):
        for c1 in range(1, t1):
            # task 2 meets its deadline iff C2 + ceil(t / T1) C1 <= t for some t <= T2; the candidate points are
            # t = T1 and t = T2 (with T1 < T2 < 2 T1, ceil(T2 / T1) = 2)
            c2 = max(t1 - c1, t2 - 2 * c1)
            if c2 <= 0:
                continue
            u = c1 / t1 + c2 / t2
            if u < best[0]:
                best = (u, t2 / t1)
    return best


def random_task_sets(n_sets: int, n_tasks: int, utilization: float, t_min: int = 10, t_max: int = 100,
                     seed: int = 1807):
    """Random task sets with exact total utilization (UUniFast split, uniform integer periods, real-valued WCETs),
    with RM priorities assigned. For analysis only (the simulator needs integer WCETs)."""
    import random
    rng = random.Random(seed)
    sets = []
    for _ in range(n_sets):
        us, s = [], utilization
        for i in range(n_tasks - 1, 0, -1):
            nxt = s * rng.random() ** (1 / i)
            us.append(s - nxt)
            s = nxt
        us.append(s)
        ts = [rng.randint(t_min, t_max) for _ in range(n_tasks)]
        sets.append(rm_priorities([Task(f"t{i}", ts[i], [(us[i] * ts[i], None)]) for i in range(n_tasks)]))
    return sets


def acceptance(sets: list[list[Task]]) -> tuple[float, float, float]:
    """Fractions accepted by the Liu & Layland bound, the hyperbolic bound and exact response-time analysis."""
    n = len(sets)
    ll = sum(utilization(s) <= ll_bound(len(s)) + 1e-12 for s in sets)
    hy = sum(hyperbolic_ok(s) for s in sets)
    ex = sum(all(response_time(s, i) is not None for i in range(len(s))) for s in sets)
    return ll / n, hy / n, ex / n
