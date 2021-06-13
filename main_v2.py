""" Handler for genetic solver. """

import sys
import numpy as np 
import matplotlib.pyplot as plt

from utils import *
from g2_funcs import *
from genetic_funcs import *


# DESCRIBE NODES AND ARCS
# Condition availability: less, greater, equal, range()
ARCS = {"s1-s2": { "cost": 0.3,
				   "conditions": {0: {"k": 3, "compare": greater},
				   				  1: {"k": 7, "compare": greater},
				   				  2: {"k": 8, "compare": lesser},
				   				 }
				 },
		"s1-s3": { "cost": 0.3,
				   "conditions": {0: {"k": 3, "compare": greater},
				   				  1: {"k": [1,3], "compare": range_exclude},
				   				  2: {"k": 8, "compare": lesser},
				   				 }
						  },
		"s1-s4": { "cost": 0.4,
				   "conditions": {0: {"k": 3, "compare": lesser},
				   				  1: {"k": 4, "compare": greater},
				   				  2: {"k": 8, "compare": greater},
				   				 }
				 },
		"s2-s6": { "cost": 0,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s3-s6": { "cost": 0.4,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": [4.99, 8], "compare": range_exclude},
				   				 }
				 },
		"s3-s7": { "cost": 0.3,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": [2.99, 5], "compare": range_exclude},
				   				 }
				 },
		"s3-s8": { "cost": 0.3,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": [1, 3], "compare": range_exclude},
				   				 }
				 },
		"s4-s7": { "cost": 0.3,
				   "conditions": {0: {"k": [1.99, 3], "compare": range_exclude},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s4-s5": { "cost": 0.3,
				   "conditions": {0: {"k": [0, 2], "compare": range_exclude},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s6-s7": { "cost": 0,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s5-s8": { "cost": 0,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s7-s9": { "cost": 0,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 },
		"s8-s9": { "cost": 0,
				   "conditions": {0: {"k": 0, "compare": allow},
				   				  1: {"k": 0, "compare": allow},
				   				  2: {"k": 0, "compare": allow},
				   				 }
				 }			  
		 }


# GENETIC ALGORITHM PARAMS
G1_FUNC   = solve_genetic
G1_PARAMS = {"root"    : "s1",
			 "goal"    : "s9",
			 "n"       : 10,
			 "retain"  : 0.4,
			 "mutation": 0.7,
			 "gens"    : 2,
			 "vars"    : 3,   # number of variables per agent
			 "no_sol"  : 1e5, # value to return if no solution
			 "arcs"    : ARCS
			}

G2_PARAMS = {"n"       : 50,
			 "retain"  : 0.15,
			 "mutation": 0.8,
			 "gens"    : 50
			}


# DEFINE Conditional variables
RANGES = {"variable_1": [0, 10],
		  "variable_2": [1, 13],
		  "variable_3": [2, 19]
		 }


VERBOSE               = 1 # 3 modes: 0-silent, 1-plot_as_go, 2-plot_final_too
ALTERNATIVE_SOLUTIONS = True


print("START SOLVING")
# Solve problem via Genetic Algorithm
pop, eval_history = genetic2(RANGES, G2_PARAMS, G1_FUNC, G1_PARAMS, verbose=VERBOSE)
best = fitness2(G1_FUNC, G1_PARAMS, pop[0])

# Get results
print("El mejor candidato es:   {0}".format(pop[0]))
print("El coste es:             {0}".format(best))


if ALTERNATIVE_SOLUTIONS:
	# give pop a great format
	unique_pop = set(["-".join([str(x) for x in sol.values()]) for sol in pop])
	sols = []
	for ind in unique_pop:
		sol  = {} 
		vals = ind.split("-")
		for i in range(len(pop[0])):
			sol[list(pop[0].keys())[i]] = float(vals[i])
		sols.append((sol, fitness2(G1_FUNC, G1_PARAMS, sol)))
	# reorder solutions based on cost
	sols = sorted(sols, key=lambda x:x[1])

	# print on screen
	print("\nSoluciones alternativas:")
	for sol in sols:
		print("{0} coste {1}".format(sol[0], sol[1]))


if VERBOSE > 1:
	print("\nEval history: \n{0}".format(eval_history))
