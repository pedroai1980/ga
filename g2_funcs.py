import numpy as np 

def ind2(ranges, dec=10**1):
	""" Generate an individual based on ranges. """
	ind = {}
	# Sample floats from [low, high]
	for k in ranges.keys():
		low, high = ranges[k]
		ind[k] = np.random.randint(low*dec, high*dec +1) / dec

	return ind 


def pop2(ranges, n=20):
	""" Generate the entire population. """
	return [ind2(ranges) for i in range(n)]


def breed2(a, b, m=0.5):
	""" Breed 2 parents to create 1 children. """
	child = {}
	for k in a.keys():
		if np.random.random() < m:
			# select from either parent with 50% prob
			if np.random.random() < 0.5:
				child[k] = np.random.choice([a[k],b[k]])+(3*(np.random.random()-0.5))
			else:
				child[k] = (a[k]+b[k]) / 2
		else:
			child[k] = np.random.choice([a[k], b[k]])

	return child


def fitness2(g1_func, g1_params, ind):
	""" Measures fitness of an individual. """
	return g1_func(ind, **g1_params)

def log2(g, m):
	print("Generation {0}: {1}".format(g, m[-1]))

def genetic2(ranges, g2_params, g1_func, g1_params, verbose=0):
	""" 
		Fast genetic algorithm.
	"""
	# create the initial population
	pop = pop2(ranges, g2_params["n"])
	# genetic algorithm loop
	eval_history = []

	for i in range(g2_params["gens"]): 
		# Proceed with genetic algorithm
		tupled = [(fitness2(g1_func, g1_params, ind), ind) for ind in pop]
		tupled = sorted(tupled, key=lambda x: x[0])
		pop = tupled[:int(g2_params["n"]*g2_params["retain"])]
		# append evaluation
		eval_history.append(np.mean([x[0] for x in tupled]))
		pop = [x[1] for x in pop]
		

		# Crossover of parents to generate children
		n_children = len(pop) - int(g2_params["n"]*g2_params["retain"])
		children = []
		for i in range(n_children):
			a, b = np.random.choice(pop, size=2, replace=False)
			# Add new child to list of children
			children.append(breed2(a, b, g2_params["mutation"]))

		# Join pareents and children to create next gen and evaluate
		pop.extend(children)
    	
		if verbose: 
			log2(i, eval_history)
		
	return pop, eval_history 