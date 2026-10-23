# fifo-monitor-rm-edf-comparison
Research paper and Python simulation comparing FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) scheduling algorithms using monitor-based synchronization in real-time task systems.
# Real-Time Scheduling with Monitor-Based Synchronization

## Overview

This repository contains a research paper and a Python simulation for comparing three CPU scheduling algorithms: First-In, First-Out (FIFO), Rate Monotonic (RM), and Earliest Deadline First (EDF).

The project investigates the behavior of periodic real-time task systems when shared resources are protected using a monitor-based synchronization mechanism.

It focuses on scheduling performance, resource contention, and blocking behavior under the assumptions defined by the simulation.

## Repository Contents

- `FIFO_Monitor_RM_EDF_Comparison_figures_intext.docx` — Research paper in editable Word format, including figures and Gantt charts.
- `fifo_monitor_comparison.py` — Python source code for the scheduling simulation.

A PDF version of the paper may also be included for convenient reading.

## Scheduling Algorithms

### FIFO — First-In, First-Out

A non-preemptive scheduling policy that executes ready jobs in arrival order.

### RM — Rate Monotonic

A fixed-priority preemptive scheduling algorithm that assigns higher priority to tasks with shorter periods.

### EDF — Earliest Deadline First

A dynamic-priority preemptive scheduling algorithm that selects the ready job with the earliest absolute deadline.

## Monitor-Based Synchronization

A monitor is a synchronization construct that encapsulates shared data and operations while providing controlled access to a shared resource.

The project models monitor-based resource access and condition waiting. The simulation examines how resource contention can affect task execution and blocking.

The exact behavior depends on the monitor implementation and the assumptions used in the Python simulation.

## Performance Metrics

The algorithms are evaluated using the following metrics:

- Average waiting time
- Average turnaround time
- Average resource waiting time
- Average blocking time
- Number of deadline misses

## Task Sets

The simulation uses two periodic task sets.

### Task Set A

| Task | Execution Time (C) | Period (T) | Deadline (D) |
|---|---:|---:|---:|
| A | 1 | 4 | 4 |
| B | 2 | 5 | 5 |
| C | 3 | 10 | 10 |

- Hyperperiod: 20 time units
- Total utilization: 0.95

### Task Set B

| Task | Execution Time (C) | Period (T) | Deadline (D) |
|---|---:|---:|---:|
| X | 2 | 5 | 5 |
| Y | 4 | 7 | 7 |

- Hyperperiod: 35 time units
- Total utilization: approximately 0.9714

## How to Run

### Requirements

- Python 3

### Execute the simulation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/real-time-scheduling-monitor-comparison.git
```

Navigate to the project directory:

```bash
cd real-time-scheduling-monitor-comparison
```

Run the simulation:

```bash
python fifo_monitor_comparison.py
```

Replace `YOUR_USERNAME` with your GitHub username.

## Figures and Results

The research paper includes diagrams and Gantt charts to illustrate the simulation workflow, monitor structure, task execution sequence, and scheduling comparisons.

Numerical results depend on the task parameters and synchronization rules implemented in the code. Validate the implementation and its output before using the results as evidence in further research.

## Limitations

This project is an educational simulation rather than a complete implementation of a production real-time operating system.

The results depend on assumptions such as task release times, scheduling policy, critical-section lengths, monitor entry and exit behavior, and condition-queue semantics. The results should not be generalized beyond the modeled scenarios without further testing.

## Future Work

Potential extensions include:

- Evaluating additional periodic task sets.
- Comparing response times and deadline-miss ratios.
- Modeling alternative monitor and condition-variable semantics.
- Adding automated plots and reproducible experiment reports.
- Validating results against established real-time scheduling analyses.

## Author

**Erfan Barati**
