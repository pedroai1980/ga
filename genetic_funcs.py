""" Functions used to selve the routing problem via a genetic algorithm. """

import sys
import numpy as np
import matplotlib.pyplot as plt

from utils import *


def common(a,b):
	""" Looks for common points between two different routes. """
	c = set(a).intersection(set(b))
	if len(c) == 0: 
		return None
	else:
		return c 
		

def allow_transition(arc, agent):
	""" Verifies a transition can take place based on restrictions. 
		Defaults to True and we try to false it.
	"""
	for k in arc["conditions"]:
		condition = arc["conditions"][k]
		# call the condition function and act accordingly
		if not condition["compare"](agent[k], condition["k"]):
			return False
	return True


def expand(node, arcs, agent):
	""" Returns an iterable of neighbors for a given node. """
	neighbors = []
	for arc in arcs.keys():
		if node == arc.split("-")[0]:
			if allow_transition(arcs[arc], agent):
				neighbors.append({"origen": arc.split("-")[0], 
								   "destin": arc.split("-")[1],
								   "cost": arcs[arc]["cost"]})
	return neighbors


def cost(node, neighbor, tree):
	""" Returns the cost of travelling from node to neighbor. """
	return arcs[node+"-"+neighbor]["cost"]


def goal_check(goal,  check = "7"):
	""" Returns True if goal found, false else. """
	if goal == check:
		return True
	
	return False
	

def prune_reps(route):
	""" Gets an inefficient route. Prunes loops.
		Check if node appears twice. Then prune loop.
	 """
	while True in [route.count(node)>=2 for node in route]:
		for city in route:
			indexs = [i for i, x in enumerate(route) if x == city]
			if len(indexs) > 1:
				route = route[:indexs[0]] + route[indexs[-1]:]

	return route


def individual(nodes, arcs, root, goal, agent):
	ind           = [root]
	dead_branches = []
	# Expand node while solution is not met: Monte-Carlo DFS
	while not goal_check(ind[-1], goal):
		cands = [cand["destin"] for cand in expand(ind[-1], arcs, agent) 
								if cand not in ind]
		# delete dead branches from candidates
		if len(cands) == 0:
			dead_branches.append(ind[-1])
			ind = ind[:-1]
		else:
			cand = np.random.choice(cands)
			ind.append(cand)

		# Check that the problem is solvable. If not, exit program:
		if len(ind) == 0:  return False

	return ind


def population(nodes, arcs, root, goal, agent, X=5):
	"""
		Initialize population.
	"""
	# np.random.seed(1)
	pop = [individual(nodes, arcs, root, goal, agent)]
	# Check first that problem is solvable
	if False in pop: return False
	# if it is, generate whole pop
	for i in range(X-1): pop.append(individual(nodes, arcs, root, goal, agent))

	return pop


def fitness(ind, arcs):
	""" Measure the fitness of an individual. Lower is better. """
	cost = []
	for i in range(len(ind)-1):
		cost.append(arcs[ind[i]+"-"+ind[i+1]]["cost"])
	return np.sum(cost)


def evaluate(population, arcs, retain):
	""" Measure the fitness of an entire population. Lower is better. """
	# print("pop", population)
	evaluation = [fitness(individual, arcs) 
				  for individual in population[:int(len(population)*retain)]]
	return np.mean(evaluation)


def mutate(ind, arcs, nodes, goal, agent):
	""" Mutate candidate solution. """
	pos = np.random.randint(1, len(ind))
	ind = ind[:pos]    
	while ind[-1] != goal:
		cands = [cand["destin"] for cand in expand(ind[-1], arcs, agent)]
		cand = np.random.choice(cands)
		ind.append(cand)
	return ind


def evolve(pop, arcs, nodes, root, goal, agent, retain=0.5, mutation=0.3):
    # Ensure no bucles during routes
    pop = [prune_reps(ind) for ind in pop]
    # Proceed with genetic algorithm
    tupled = [ (fitness(ind, arcs), ind) for ind in pop ]
    tupled = [ x[1] for x in sorted(tupled) ]
    parents = tupled[:int(len(pop)*retain)]

	# Crossover of parents to generate children
    n_children = len(pop) - int(len(pop)*retain)
    children = []
    while len(children) < n_children:
    	# select two parents
        parents_i = list(range(len(parents)))
        male, female = np.random.choice(parents_i, size=2, replace=False)
        male, female = parents[male], parents[female]
        # define cross point
        cp = common(male, female)
        if cp is None: 
            child = mutate(np.random.choice([male, female]), arcs, nodes, goal, agent)
        else: 
            cp = np.random.choice(list(cp))
            child = male[:male.index(cp)]+female[female.index(cp):]
            # mutate if probability is met
            if np.random.random() < mutation:
                child = mutate(child, arcs, nodes, goal, agent)
        # Add new child to list of children
        children.append(child)
    
    # Join pareents and children to create next gen
    parents.extend(children)
    return parents 


def solve_genetic(agent, root, goal, n, retain, 
				  mutation, gens, vars, no_sol, arcs):
	""" Solve the problem via genetic algorithm. """

	# tarnsform agent to list of values
	agent = list(agent.values())
	# Initialize population
	pop = population(nodes=None, arcs=arcs, root=root, goal=goal, agent=agent, X=n)

	# if problem not solvable
	if pop is False:
		return no_sol
	# no need to evaluate ta the beginning since we only evaluate
	# selected candidates
	eval_history = []
	# Run Genetic Algorithm
	for i in range(gens-1):
		pop = evolve(pop, arcs, nodes=None, root=root, goal=goal, agent=agent, retain=retain, mutation=mutation)
		evaluation = evaluate(pop, arcs, retain) # fitness(pop[0], arcs)
		eval_history.append(evaluation)

	return fitness(pop[0], arcs)# pop, eval_history


def plot_graph(eval_history):
	# Plot the Fitness of each generation. Lower is better
	plt.figure()
	# Define plots.
	plt.plot(eval_history, '-ro')
	plt.grid(True)
	plt.title("Graph visualization")
	plt.xlabel("Number of Generations")
	plt.ylabel("Fitness score")
	# Plot it all
	plt.show()