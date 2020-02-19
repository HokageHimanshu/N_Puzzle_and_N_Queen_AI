import numpy as np
import math
import timeit
import random
import time
from statistics import mean
# value is row and index is col


class Node:

	def __init__(self,arr,cost):
		self.arr = arr
		self.cost = cost

def compareParameter(n):
	return n.cost


def calcClashes(arr):
	clashes = 0
	for i in range(len(arr)):
		for j in range(i+1,len(arr)):
			if arr[i]-i == arr[j]-j :
				clashes+=1
			if arr[i]+i == (arr[j]+j):
				clashes+=1
	return clashes 

#returns the list of the selected nodes 
def selection(pop_list,required_len):
	selected = []
	for i in range(len(pop_list)):
		cost = calcClashes(pop_list[i])
		node = Node(pop_list[i],cost)
		selected.append(node)
	selected.sort(key=compareParameter)
	list_selected = []
	for i in range(required_len):
		list_selected.append(selected[i].arr)
	return list_selected


def mutation(arr,index):
	mutated = []
	for i in range(len(arr)):
		if i != index:
			temp_arr = np.copy(arr)
			temp = temp_arr[i]
			temp_arr[i] = temp_arr[index]
			temp_arr[index] = temp
			mutated.append(temp_arr)
	return mutated

def mutation1(arr,indices):
	temp = arr[indices[0]]
	arr[indices[0]] = arr[indices[1]]
	arr[indices[1]] = temp
	return arr

def generateChildren(parents,pop_len,regularize):
	parent_len = len(parents)
	children=parents
	n = int(len(parents[0]))
	# mid = int(len(parents[0])/2)
	# end = int(len(parents[0]))
	# for i in range(parent_len):
	# 	for j in range(i+1,parent_len):
	# 		c = np.append(parents[i][:mid],parents[j][mid:end])
	# 		children.append(c) 

	reg_ratio = int(0.3*pop_len)
	# if we have to regularize
	if regularize:
		for i in range(pop_len-reg_ratio-parent_len):
			children.append(mutation1(parents[i%10],random.sample((0,n-1),2)))

		# for i in range(parent_len):
		# 	children.extend(mutation(parents[i],random.randint(0,n-1)))
		temp_arr = np.arange(n)

		for i in range(reg_ratio):
			reg_temp = np.copy(temp_arr)
			np.random.shuffle(reg_temp)
			children.append(reg_temp)
	# if we have to generate children from parents only
	else :
		for i in range(pop_len-parent_len):
			children.append(mutation1(parents[i%10],random.sample((0,n-1),2)))

	# print('Children pop = ',len(children))
	return children


def printboard(arr,n):
	board = np.zeros(n*n)

	for i in range(len(arr)):
		board[arr[i]*n+i]=1

	print(np.reshape(board,(n,n)))
	print('\n')



def genetic_algo(arr,n):
	initial_pop = []
	initial_pop_len = 100
	parents_len =10

	for i in range(initial_pop_len):
		tempa = np.copy(arr)
		np.random.shuffle(tempa)
		initial_pop.append(tempa)

	#selected initial pop is list of arrays while initial pop is list of arrays
	selected_parents = selection(initial_pop,parents_len)

	iterations = 5000
	regularize_interval = 50

	for i in range(iterations):
		if i%regularize_interval==0:
			children = generateChildren(selected_parents,initial_pop_len,True)
		else:
			children = generateChildren(selected_parents,initial_pop_len,False)

		selected_parents = selection(children,parents_len)
		if(calcClashes(selected_parents[0])==0):
			# print('Breaking')
			break

	print(selected_parents[0],' clash ',calcClashes(selected_parents[0]))
	print('\n')
	printboard(selected_parents[0],n)
	return calcClashes(selected_parents[0])

# def stats(n):
# 	SETUP_CODE = '''from __main__ import genetic_algo
# 	import numpy as np
# 	import math
# 	import timeit
# 	import random
# 	import time'''

# 	TEST_CODE = ''' 
# 	arr= np.arange(n)
# 	genetic_algo(arr,n)'''
# 	# timeit.repeat statement
# 	times = timeit.repeat(setup = SETUP_CODE,stmt = TEST_CODE,repeat = 10,number = 1) 
# 	# priniting minimum exec. time
# 	print('stats = ',mean(times))

def stats1(n,iterations):
	arr= np.arange(n)
	time_val = []
	clashes = []
	for i in range(iterations):
		t=time.time()
		clashes.append(genetic_algo(arr,n))
		time_val.append(time.time()-t)
	return mean(time_val),int(mean(clashes))


# n=50
# arr= np.arange(n)
# t = timeit.default_timer()
# t2 = time.time()
# genetic_algo(arr,n)
# print('Time taken by genetic_algo = ',((timeit.default_timer()-t)),' t2 = ',time.time()-t2)

# Single call to the function
# print(stats1(10,5))

# n = input('Enter the value of the n for the n queens problem = ')
# arr = np.arange(n)
# genetic_algo(arr,n)

#  Storing in the file
# fd = open('vals_nqueens.txt','w')
# store =[]
# for i in range(4,15):
# 	store.append(stats1(i,5))
# 	line = 'Time taken for '+ str(i) + ' size = ' +str(store[i-4][0]) +" and clashes = "+str(store[i-4][1])
# 	fd.write(line)
# 	fd.write('\n')
# 	print(i,' = ',store[i-4])
# fd.close()