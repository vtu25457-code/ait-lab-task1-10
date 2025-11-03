import numpy as np
d = np.array([
    [0, 20, 25, 18, 22],
    [20, 0, 24, 30, 17],
    [25, 24, 0, 21, 26],
    [18, 30, 21, 0, 28],
    [22, 17, 26, 28, 0]
], dtype=float)
iteration = 100
n_ants = 5
n_citys = 5
m = n_ants
n = n_citys
e = 0.5
alpha = 1
beta = 2
visibility = np.zeros_like(d, dtype=float)
with np.errstate(divide="ignore"):
    visibility[d > 0] = 1.0 / d[d > 0]
pheromne = 0.1 * np.ones((n, n))
np.fill_diagonal(pheromne, 0.0)
rute = np.ones((m, n + 1), dtype=int)
global_best_cost = np.inf
global_best_route = None
for ite in range(iteration):
    rute[:, 0] = 1
    for i in range(m):
        visited = {0}
        current = 0
        for step in range(n - 1):
            candidates = [c for c in range(n) if c not in visited]
            tau = pheromne[current, candidates] ** alpha
            eta = visibility[current, candidates] ** beta
            desirability = tau * eta
            total = desirability.sum()
            if total == 0:
                probs = np.ones(len(candidates)) / len(candidates)
            else:
                probs = desirability / total
            next_city = np.random.choice(candidates, p=probs)
            rute[i, step + 1] = next_city + 1
            visited.add(next_city)
            current = next_city
        rute[i, -1] = rute[i, 0]
    rute_opt = np.array(rute, dtype=int)
    dist_cost = np.zeros((m, 1), dtype=float)
    for i in range(m):
        s = 0.0
        for j in range(n):
            a = int(rute_opt[i, j]) - 1
            b = int(rute_opt[i, j + 1]) - 1
            s += d[a, b]
        dist_cost[i] = s
    dist_min_loc = int(np.argmin(dist_cost))
    dist_min_cost = dist_cost[dist_min_loc]
    current_best_route = rute_opt[dist_min_loc, :].astype(int)
    if dist_min_cost < global_best_cost:
        global_best_cost = float(dist_min_cost[0])
        global_best_route = current_best_route.copy()
    pheromne = (1 - e) * pheromne
    for i in range(m):
        tour_length = float(dist_cost[i][0])
        if tour_length <= 0:
            continue
        dt = 1.0 / tour_length
        for j in range(n):
            a = int(rute_opt[i, j]) - 1
            b = int(rute_opt[i, j + 1]) - 1
            pheromne[a, b] += dt
            pheromne[b, a] += dt
    pheromne = np.clip(pheromne, 1e-12, None)
    np.fill_diagonal(pheromne, 0.0)
print("Route of all the ants at the end (last iteration):")
print(rute_opt)
print()
print("Best path found (1-based):", global_best_route.tolist())
print("Cost of the best path:", int(global_best_cost))
