import numpy as np
import lib
import time
import random

def gen_params(parameters):
    p = np.zeros(len(parameters), dtype=np.float64)
    for i, par in enumerate(parameters):
        mini = par["min"]
        maxi = par["max"]
        p[i] = np.random.uniform(mini, maxi)
    return p


def a(costf=None, parameters=None, N=100, max_time=-1, debug=False):
    if costf is None:
        raise Exception("costf is a required kwarg")
    if parameters is None:
        raise Exception("parameters is a required kwarg")
    best_params = None
    best_cost = None
    it_best_costs = []
    start_time = time.time()
    times = []
    it = 0
    if max_time > 0:
        N = -1
    current_time = 0
    while (it < N or N < 0) and (current_time < max_time or max_time < 0):
        it += 1
        ps = gen_params(parameters)
        cost = costf(ps)
        if best_cost is None or cost < best_cost:
            best_params = ps
            best_cost = cost
        it_best_costs.append(best_cost)
        current_time = time.time() - start_time
        times.append(current_time)
        if debug:
            print("parameters:", ps, end="\t")
            print("cost:", cost, end="\t")
            print("best cost:", best_cost)
    return {
        "results": {
            "best_params": best_params.tolist(),
            "best_cost": best_cost,
        },
        "stats": {
            "it_best_costs": it_best_costs,
            "time": times,
        }
    }

def best_m(params, costs, M=10, unzip=True):
    best_M = sorted(zip(params, costs), key=lambda x: x[1])[:M]
    if unzip:
        return list(zip(*best_M))
    return best_M

def bests2parameters(bests):
    print("bests: ", bests)
    params = bests[0] 
    p1 = params[0]
    ps = []
    for i in range(len(p1)):
        param_values = list(map(lambda x: x[i], params))
        ps.append({
            "min": min(param_values),
            "max": max(param_values),
            })
    return ps

def b_mod(costf=None, parameters=None, iterations=2, N=100, M=10, max_time=-1, debug=False):
    if costf is None:
        raise Exception("costf is a required kwarg")
    if parameters is None:
        raise Exception("parameters is a required kwarg")
    it_best_costs = []
    start_time = time.time()
    best_cost = None
    best_params = None
    times = []
    current_time = 0
    iterations_results = []
    for i in range(iterations):
        if debug:
            print("iteration: ", i)
        if max_time > 0 and current_time > max_time:
            break
        params = []
        costs = []
        it = 0
        while it < N:
            it += 1
            ps = gen_params(parameters)
            cost = costf(ps)
            params.append(ps)
            costs.append(cost)
            if best_cost is None or cost < best_cost:
                best_params = ps
                best_cost = cost
            it_best_costs.append(best_cost)
            current_time = time.time() - start_time
            times.append(current_time)
            if debug:
                print("parameters:", ps, end="\t")
                print("cost:", cost, end="\t")
                print("best cost:", best_cost)
        bests = best_m(params, costs, M=M)
        parameters = bests2parameters(bests)
        iteration_results = {
                "M": M,
                "best_m_params": list(map(lambda x: x.tolist(), bests[0])),
                "best_m_costs": bests[1],
                "best_params": best_params.tolist(),
                "best_cost": best_cost,
        }
    return {
        "results": {
            "best_params": best_params.tolist(),
            "best_cost": best_cost,
        },
        "stats": {
            "it_best_costs": it_best_costs,
            "time": times,
        },
        "iteration_results": iteration_results,
    }

def perturb(x, alpha=0.1):
    # generate random point in the unit hypersphere
    print(x, type(x))
    ndim = x.shape[0]
    random_point = np.random.normal(size=ndim)
    random_point /= np.linalg.norm(random_point)

    # scale and translate the point to fit the specified center and radius
    perturbed_point = x + alpha * x * random_point

    return perturbed_point

def b(costf=None, parameters=None, alpha=0.1, iterations=2, N=100, M=10, max_time=-1, debug=False):
    if costf is None:
        raise Exception("costf is a required kwarg")
    if parameters is None:
        raise Exception("parameters is a required kwarg")
    it_best_costs = []
    start_time = time.time()
    best_cost = None
    best_params = None
    times = []
    if max_time > 0:
        N = -1
    current_time = 0
    params = []
    costs = []
    it = 0
    while (it < N or N < 0) and (current_time < max_time or max_time < 0):
        it += 1
        ps = gen_params(parameters)
        cost = costf(ps)
        params.append(ps)
        costs.append(cost)
        if best_cost is None or cost < best_cost:
            best_params = ps
            best_cost = cost
        it_best_costs.append(best_cost)
        current_time = time.time() - start_time
        times.append(current_time)
        if debug:
            print("parameters:", ps, end="\t")
            print("cost:", cost, end="\t")
            print("best cost:", best_cost)
    bests = best_m(params, costs, M=M)

    for i in range(iterations):
        params = []
        costs = []
        it = 0
        while it < N and (current_time < max_time or max_time < 0):
            it += 1
            choice = random.choice(bests[0])
            new_params = perturb(choice, alpha=alpha)
            new_cost = costf(choice)
            params.append(new_params)
            costs.append(new_cost)
            if new_cost < best_cost:
                best_cost = new_cost
                best_params = new_params
        bests = best_m(params, costs, M=M)
        alpha /= 2
        
    return {
        "results": {
            "best_params": best_params,
            "best_cost": best_cost,
        },
        "stats": {
            "it_best_costs": it_best_costs,
            "time": times,
        }
    }


if __name__ == "__main__":
    costf = lib.f_real
    parameters=[{"min": 0, "max": 20},{"min": 0, "max": 20}]
    N=1000
    out = b(costf=costf, iterations=30, parameters=parameters, N=N, M=300, debug=False, alpha=5)
    print(out['results']['best_params'])
