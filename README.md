# Profit Maximization Simulation

## Problem Description
You are running a service, and cannot leave a job partially done or work on 2 jobs at once. Additionally, not all jobs are equally profitable. The goal is to strategically complete jobs in an order that would maximize total profit. The customer list dictates job deadlines, expected time required, and profit. Additionally, if any job is finished past the deadline, profit decays exponentially according to the following function: $p_{i} \cdot e^{-0.017 \cdot s_{i}}$, where $p_{i}$ = profit for completing job i by the deadline, and $s_{i}$ = # of minutes late after deadline job i was completed. Given a list of n jobs with id i, deadline $t_{i}$ in minutes, duration $d_{i}$ in minutes, and profit $p_{i}$, provide a schedule of jobs in one day (1440 minutes) that would maximize the total profit.

## Constraints
• Start scheduling at the 0th minute of the day.
• Start the next job the same minute we finish the previous job.
• The entire profit is received for tasks that are completed any time before or on their deadline.
• The last task must be completed by minute 1440.

## Approach
Constructed a greedy-based, graph algorithm, using edge removal, and implemented a heuristic for optimization.
- find the shortest path: iteratively remove nodes and edges from the graph, and determine which change or removal would have the most impact on the potential paths in the graph.
- shortest_path(): shortest path to the target vertex, identify potential minimum edges to change/remove + filter.
- has_path(): identify edge removals that maintain a connected graph.
- heuristic: compute k shortest paths, compare nodes' and edges' contribution to alternative paths.

## Testing
- Run the solver using python3 solver.py test.in
- retrieve outputs in submission.json using python3 prepare_submission.py outputs/ submission.json







(Problem Source: CS170: Efficient Algorithms and Intractable Problems)
