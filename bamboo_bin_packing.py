from __future__ import print_function
from ortools.linear_solver import pywraplp
import pandas as pd


def create_data_model():
    """Create the data for the example."""
    raw_data = pd.read_csv(r'C:\Users\Sven.Koenning\Documents\bamboo_code\test.csv', encoding='utf-8')
    raw_data = raw_data.values.tolist()
    raw_data = [item for sublist in raw_data for item in sublist]
    data = {}
    weights = raw_data
    data['weights'] = weights
    data['items'] = list(range(len(weights)))
    data['bins'] = data['items']
    data['bin_capacity'] = 600
    return data


def knapsack(data):

    # Create the mip solver with the SCIP backend.
    #solver = pywraplp.Solver.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # y[j] = 1 if bin j is used.
    y = {}
    for j in data['bins']:
        y[j] = solver.IntVar(0, 1, 'y[%i]' % j)

    # Constraints
    # Each item must be in exactly one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items']) <= y[j] *
            data['bin_capacity'])

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum([y[j] for j in data['bins']]))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        num_bins = 0
        bamboo = []
        for j in data['bins']:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data['items']:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(i)
                        bin_weight += data['weights'][i]
                if bin_weight > 0:
                    num_bins += 1
                bamboo.append([bin_items, bin_weight])

        return bamboo, num_bins

    else:
        print('The problem does not have an optimal solution.')


data_bamboo = create_data_model()

solution = knapsack(data_bamboo)

df_solution = pd.DataFrame(solution[0])
df_solution.to_csv(r'C:\Users\Sven.Koenning\Documents\bamboo_code\solution.csv')

print(solution)

