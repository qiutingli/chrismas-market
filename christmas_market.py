from gurobipy import *

def solve(stands,
          temperature,
          amount,
          alcohol_content,
          sugar,
          calorific_value,
          price,
          cup_type,
          persons,
          budget,
          min_wine_total,
          environment,
          max_wine_per_stand):

    model = Model("Christmas ")
    model.modelSense = GRB.MAXIMIZE

    # variable x
    x = {}
    for p in persons:
        for s in stands:
            x[p, s] = model.addVar(vtype="I",lb=0.0,name="x_%s_%s" % (p, s))


    # TODO: Add potential additional variables.
    model.update()
    model.setObjective(quicksum(alcohol_content[s]/price[s]*quicksum(x[p,s] for p in persons) for s in stands), GRB.MAXIMIZE)


    # TODO: Add all contraints
    # For each person, the total spend on all stands is less than the budget[p].
    for p in persons:
        model.addConstr(quicksum(x[p,s]*price[s] for s in stands) <= budget[p])

    # Each person drinks at most max_wine_per_stand[p,s] cups hot wine at stand s.
    for p in persons:
        for s in stands:
            model.addConstr(x[p,s] <= max_wine_per_stand[p,s])

    # For each person, the total number of cups taken from all stands is greater than min_wine_total[p].
    for p in persons:
        model.addConstr(quicksum(x[p,s] for s in stands) >= min_wine_total[p])

    # Those who drink environmental friendly, only drink at stands whose cup-types are glass or ceramic.
    for p in persons:
        for s in stands:
            if environment[p] and cup_type[s] != 'ceramic' and cup_type[s] != 'glass':
                model.addConstr(x[p,s] <= 0)

    model.optimize()

    # print solution
    if model.status == GRB.OPTIMAL:
        print('\n objective: %g\n' % model.ObjVal)
        for p in persons:
            for s in stands:
                if x[p, s].x >= 1:
                    print('%s drinks %i cups at %s' % (p, x[p, s].x, s))

    return model



