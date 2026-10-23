#!/usr/bin/env python3

from dataclasses import dataclass
from math import lcm
import csv

@dataclass(frozen=True)
class Task:
    name: str
    C: int
    T: int
    D: int

@dataclass
class Job:
    task: Task
    jid: int
    release: int
    deadline: int
    remaining: int
    first_start: int | None = None
    completion: int | None = None
    executed: int = 0
    monitor_requested: bool = False
    monitor_acquired: bool = False
    wait_start: int | None = None
    resource_wait: int = 0
    blocked_ticks: int = 0
    in_cs: bool = False
    cs_remaining: int = 0
    @property
    def label(self): return f"{self.task.name}{self.jid}"

def simulate(tasks, policy, horizon=None):
    H = lcm(*(t.T for t in tasks)); horizon = H if horizon is None else horizon
    jobs, ready, condition_waiters, gantt = [], [], [], []
    running = None; monitor_owner = None
    ids = {t.name: 0 for t in tasks}
    for now in range(horizon):
        # Release new jobs at this time boundary.
        for t in tasks:
            if now % t.T == 0:
                ids[t.name] += 1
                j = Job(t, ids[t.name], now, now+t.D, t.C)
                jobs.append(j); ready.append(j)

        # Choose the CPU job. FIFO only dispatches when CPU becomes free;
        # RM/EDF reconsider priorities at every tick.
        if policy == 'FIFO':
            if running is None:
                if ready:
                    running = min(ready, key=lambda j:(j.release, j.task.name, j.jid)); ready.remove(running)
        else:
            if policy == 'RM':
                key = lambda j:(j.task.T, j.release, j.task.name, j.jid)
            elif policy == 'EDF':
                key = lambda j:(j.deadline, j.release, j.task.name, j.jid)
            else: raise ValueError(f'Unknown policy: {policy}')
            candidates = list(ready)
            if running is not None: candidates.append(running)
            if candidates:
                chosen = min(candidates, key=key)
                if chosen is not running:
                    if running is not None: ready.append(running)
                    if chosen in ready: ready.remove(chosen)
                    running = chosen

        # A job must enter the monitor immediately before its final critical section.
        if running is not None:
            cs_len = min(2, running.task.C)
            non_cs = running.task.C - cs_len
            if not running.monitor_requested and running.executed >= non_cs:
                running.monitor_requested = True
                if monitor_owner is None:
                    monitor_owner = running; running.monitor_acquired = True
                    running.in_cs = True; running.cs_remaining = cs_len
                else:
                    running.wait_start = now
                    condition_waiters.append(running)
                    running = None

        if running is None:
            gantt.append((now, now+1, 'IDLE'))
            # Any jobs already on condition wait queue accrue blocking time.
            # A newly blocked job was counted above for this tick.
            continue

        if running.first_start is None: running.first_start = now
        running.remaining -= 1; running.executed += 1
        gantt.append((now, now+1, running.label))

        if running.in_cs:
            running.cs_remaining -= 1
            if running.cs_remaining == 0:
                # monitor.exit(): release or signal-and-handoff to FIFO waiter.
                running.in_cs = False
                if condition_waiters:
                    nxt = condition_waiters.pop(0)
                    if nxt.wait_start is not None:
                        elapsed = now + 1 - nxt.wait_start
                        nxt.resource_wait += elapsed
                        nxt.blocked_ticks += elapsed
                        nxt.wait_start = None
                    nxt.monitor_acquired = True; nxt.in_cs = True
                    nxt.cs_remaining = min(2, nxt.task.C)
                    monitor_owner = nxt
                    ready.append(nxt)
                else:
                    monitor_owner = None
        if running.remaining == 0:
            running.completion = now+1
            # Critical section is at the end of the job; ownership should be released above.
            running = None


    completed = [j for j in jobs if j.completion is not None]
    def avg(xs): return round(sum(xs)/len(xs), 3) if xs else None
    detail=[]
    for j in jobs:
        ta = j.completion-j.release if j.completion is not None else None
        detail.append({'policy':policy,'job':j.label,'task':j.task.name,'release':j.release,
          'deadline':j.deadline,'execution_time':j.task.C,'first_start':j.first_start,
          'completion':j.completion,'waiting_time':ta-j.task.C if ta is not None else None,
          'turnaround_time':ta,'response_time':j.first_start-j.release if j.first_start is not None else None,
          'resource_waiting_time':j.resource_wait,'block_time':j.blocked_ticks,
          'deadline_missed':bool(j.completion is not None and j.completion>j.deadline)})
    summary={'policy':policy,'hyperperiod':H,'jobs_released':len(jobs),'jobs_completed':len(completed),
      'avg_waiting_time':avg([j.completion-j.release-j.task.C for j in completed]),
      'avg_turnaround_time':avg([j.completion-j.release for j in completed]),
      'avg_response_time':avg([j.first_start-j.release for j in completed if j.first_start is not None]),
      'avg_resource_waiting_time':avg([j.resource_wait for j in completed]),
      'avg_block_time':avg([j.blocked_ticks for j in completed]),
      'deadline_misses':sum(1 for j in completed if j.completion>j.deadline),
      'idle_time':sum(1 for a,b,l in gantt if l=='IDLE')}
    compressed=[]
    for a,b,label in gantt:
        if compressed and compressed[-1][2]==label and compressed[-1][1]==a:
            compressed[-1]=(compressed[-1][0],b,label)
        else: compressed.append((a,b,label))
    return summary, detail, compressed

CASES={'A':[Task('A',1,4,4),Task('B',2,5,5),Task('C',3,10,10)],
       'B':[Task('X',2,5,5),Task('Y',4,7,7)]}

def main():
    summaries=[]; details=[]; gantts=[]
    for case,tasks in CASES.items():
        for policy in ('FIFO','RM','EDF'):
            s, rows, gs=simulate(tasks,policy); s['case']=case; summaries.append(s)
            for r in rows: r['case']=case; details.append(r)
            for a,b,label in gs: gantts.append({'case':case,'policy':policy,'start':a,'end':b,'slot':label})
    for name, rows in [('monitor_summary.csv',summaries),('monitor_job_details.csv',details),('monitor_gantt.csv',gantts)]:
        with open(name,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('case,policy,avg_wait,avg_turnaround,avg_resource_wait,avg_block,misses,idle')
    for s in summaries:
        print(f"{s['case']},{s['policy']},{s['avg_waiting_time']},{s['avg_turnaround_time']},{s['avg_resource_waiting_time']},{s['avg_block_time']},{s['deadline_misses']},{s['idle_time']}")
if __name__=='__main__': main()
