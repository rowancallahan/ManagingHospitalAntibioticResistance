"""
Darwinian Defenders
"""

# Importing libraries
import matplotlib as plt
plt.use('TkAgg')
import matplotlib.pyplot as pyplot
import json
import numpy
import networkx as nx
import sys
import datetime


# Data stripping

# Given header line, parse headers
def get_headers(line):
	headers = {}
	tokens = line.strip().split('\t')
	for i in range(1,len(tokens)):
		headers.update( {i:tokens[i]} )
	return headers

# Given a file of Collateral Sensitivity scores matrix, return drugs, resistant strains, and edge scores
def get_edges(matrix_file):
	headers = {}
	strain_list = []
	edge_list = []
	reader = open(matrix_file,'r')
	for line in reader:
		if line.find('*\t')==0:
			headers = get_headers(line)
			continue

		tokens = line.strip().split('\t')
		strain_res = tokens[0]
		strain_list.append(strain_res)
		for i in range(1,len(tokens)):
			drug = headers[i]
			value = int(tokens[i])
			edge_list.append( (strain_res,drug,value) )

	return headers.keys(), strain_list, edge_list

# Remove all positive scores from edge scores (remove resistant matches)
def remove_positive_vals(edge_list):
	new_edge_list = []
	for e in edge_list:
		if e[2] >= 0:
			continue
		new_edge_list.append(e)
	return new_edge_list


def generate_plot(matrix_file, resistant=None):
	
	# Import data for Graphs
	drug_list, res_list, e_list = get_edges(matrix_file)
	ne_list = remove_positive_vals(e_list)
	
	# Building graph data
	G=nx.DiGraph()
	
	for n in res_list:				# add nodes
		G.add_node(n)

	pos = nx.spring_layout(G)

	for e in ne_list:				# add edges
		G.add_edge(e[0],e[1],weight=e[2])
	
	
	# Calculating total cycles
	total_cycle_list = []
	for possible_cycle in nx.simple_cycles(G):
		total_cycle_list.append(list(possible_cycle))
	
	# Input a single Antibiotic resistance_list and makes list of reachable nodes
	######
	######
	########
	#######
	######
	
	if resistant == None:
		print('yo')
		
	
	else:
		
		# Get all reachable graphs
		reachable = []
		for node in res_list:
			if nx.has_path(G, resistant, node):
				reachable.append(node)
		
		# Selecting best cycle
		high_score = 0
		cycle_list = []
		best_cycle = None
		for cycle in total_cycle_list:
			for element in cycle:
				if(element in reachable):
					cycle_list.append(cycle)
					break
		
		for cycle in cycle_list:
			size = len(cycle)
			sum_of_score = 0
			for spot in range(size):
				addition = G[cycle[spot]][cycle[(spot+1) % size]]['weight']
				sum_of_score += addition
			if size < 6:
				sum_of_score *= size
			else:
				sum_of_score *= 3
			if (sum_of_score/size) <= high_score:
				high_score = sum_of_score/size
				best_cycle = cycle
		
		print(best_cycle)
		
		# Drawing Cycle
		color_map = []
		
		if best_cycle == None:
			print("no cycles")
			subgraph = nx.subgraph(G,resistant)
			nx.draw(subgraph,pos,node_size=2000, with_labels = True,)
			pyplot.show()
		else:
			subgraph = nx.subgraph(G, [resistant] + best_cycle)
			pos = nx.spring_layout(subgraph)
			for node in subgraph:
				if node==resistant:
					color_map.append('red')
				elif node in best_cycle:
					color_map.append('blue')
				else:
					color_map.append('green')
			
			a = nx.draw(subgraph,pos,node_color = color_map,node_size=2000, with_labels = True, arrows=True,arrowstyle='->')
			print(type(a))
			pyplot.show()
generate_plot(sys.argv[1],sys.argv[2])
