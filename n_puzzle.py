import numpy as np
import math
import queue
import timeit
import heapq
import sys

class Node:
	def __init__(self,arr,cord0,parentnode,depth):
		self.a = arr
		self.pos0 = cord0
		self.parentnode = parentnode
		self.depth = depth

class NodeA:
	def __init__(self,arr,cord0,parentnode,depth,gcost,hcost):
		self.a = arr
		self.pos0 = cord0
		self.parentnode = parentnode
		self.depth = depth
		self.gcost = gcost
		self.hcost = hcost
		self.cost = self.gcost+self.hcost


class PriorityQueue(object): 
    def __init__(self): 
        self.queue = []    

    def isEmpty(self): 
        return len(self.queue) == [] 
    
    def insert(self,data): 
        self.queue.append(data) 

    def delete(self): 
        try: 
            maxindex = 0
            for i in range(len(self.queue)): 
                if self.queue[i].cost < self.queue[maxindex].cost: 
                    maxindex = i 
            item = self.queue[maxindex] 
            del self.queue[maxindex] 
            return item 
        except IndexError:  
            return None


def printpath(n,k):
	if n!=None:
		printpath(n.parentnode,k)
		print(np.reshape(n.a,(k,k)))
		print('\n')

def check(arr1,arr2):
	return np.array_equal(arr1,arr2)

def findneighbours(pos,k):
	n = k*k
	neighbours = []
	if pos+k<n :
		neighbours.append(pos+k)
	if pos-k>=0 :
		neighbours.append(pos-k)
	if((pos+1)%k!=0):
		neighbours.append(pos+1)
	if((pos)%k!=0):	
		neighbours.append(pos-1)
	return neighbours


def isSolvable(arr,k):
	n=k*k-1
	count=0
	spacerow = 0
	for i in range(n+1):
		if arr[i]==0:
			spacerow = k-int(i/k)
		for j in range(i+1,n+1):
			if arr[i]>arr[j] and arr[j]!=0 and arr[i]!=0:
				count +=1
	if k%2==1 :
		return count%2==0 
	else:
		if spacerow%2==0:
			return count%2==1
		return count%2==0


def bfs(arr,k,n,pos0):
	print('BFS Strating')
	tempgoal = np.arange(k*k)
	goalarr = np.append(tempgoal[1:],tempgoal[0])

	goalarr2 = np.arange(n+1)

	q = queue.Queue(maxsize=0)
	startnode = Node(arr,pos0,None,0)
	q.put(startnode)
	finished =[]
	finished.append(arr)
	while q.qsize()!=0:
		parentn =q.get()
		print(parentn.a)
		print('\n')
		if(check(parentn.a,goalarr) or check(parentn.a,goalarr2)):
			print('found the sol in the bfs')
			# print(parentn.parentnode.a)
			printpath(parentn,k)
			return

		space = parentn.pos0

		neighbours = findneighbours(space,k)
		print('neighbours = ',neighbours)

		# if parentn.depth<200:
		for i in neighbours:
			tempa = np.copy(parentn.a)
			temp=tempa[space]
			tempa[space] = tempa[i]
			tempa[i] = temp
			childnode = Node(tempa,i,parentn,parentn.depth+1)
			checkPresent = False
			for x in finished:
				if np.array_equal(tempa,x):
					checkPresent=True
					break
			print('outside for loop',checkPresent)

			if not checkPresent:
				print('Adding the childnode')
				q.put(childnode)
				finished.append(tempa)
			tempa=None	

		# finished.append(parentn)

	print('Finishing BFS')



def dfs(arr,k,n,pos0):
	print('DFS Strating....')
	tempgoal = np.arange(k*k)
	goalarr = np.append(tempgoal[1:],tempgoal[0])
	s = queue.LifoQueue(maxsize=0)
	maxdepth = n*n*(n-1)
	# depth =0
	startnode = Node(arr,pos0,None,0)
	s.put(startnode)
	# sys.setrecursionlimit(3000)
	# count =0
	finished =[]
	finished.append(startnode)
	# visited = []
	# visited.append(startnode.a)
	while s.qsize()!=0:
		# depth+=1
		parentn = s.get()
		if(check(parentn.a,goalarr)):
			print('found the sol in the dfs')
			# print(parentn.parentnode.a)
			printpath(parentn,k)
			return
			
		if parentn.depth<maxdepth:
			space = parentn.pos0

			neighbours = findneighbours(space,k)

			for i in neighbours:
				tempa = np.copy(parentn.a)
				temp=tempa[space]
				tempa[space] = tempa[i]
				tempa[i] = temp
				childnode = Node(tempa,i,parentn,parentn.depth+1)
				# checkPresent = False
				# for x in visited:
				# 	if np.array_equal(childnode.a,x):
				# 		checkPresent=True
				# 		break
				# print('outside for loop',checkPresent)

				if not np.array_equal(parentn.a,childnode.a):
				# if childnode not in finished:	
					s.put(childnode)
					print('DFS child added')
					# visited.append(childnode.a)
					# finished.append(childnode)
				tempa=None
			finished.append(parentn)
		print('outside of DFS')

	print('Finishing DFS')


def mis_placedtiles(arr):
	misplaces =0;
	for i in range(len(arr)):
		if(i!=len(arr)-1):
			if(arr[i]!=i+1):
				misplaces+=1
		else:
			if(arr[i]!=0):
				misplaces+=1
	return misplaces

def heuristics(arr):
	return mis_placedtiles(arr)

def idastar(arr,k,n,pos0):
	print('IDA* Strating')
	sol_found = False
	maxcutoff = 1
	cutoff = 1
	tempgoal = np.arange(k*k)
	goalarr = np.append(tempgoal[1:],tempgoal[0])

	while True:
		# print('before =',cutoff,' ',maxcutoff)
		cutoff = maxcutoff
		# print('after = ',cutoff,' ',maxcutoff)
		
		# a star 
		pq = PriorityQueue()
		
		gcost=0
		hcost = heuristics(arr)
		startnode = NodeA(arr,pos0,None,0,gcost,hcost)
		pq.insert(startnode)
		# count =0
		finished =[]
		while not pq.isEmpty():
			# gcost+=1
			# print('retrieving parent',pq.isEmpty())
			parentn = pq.delete()

			if parentn==None:
				break

			if(check(parentn.a,goalarr)):
				print('found the sol in the IDASTAR')
				# print(parentn.parentnode.a)
				sol_found = True
				printpath(parentn,k)
				return
			space = parentn.pos0

			neighbours = findneighbours(space,k)
			# print('checking neighbours')
			for i in neighbours:
				# print('inside neighbourss',' ',maxcutoff,' ',cutoff)
				tempa = np.copy(parentn.a)
				temp=tempa[space]
				tempa[space] = tempa[i]
				tempa[i] = temp

				hcost = heuristics(tempa)

				childnode = NodeA(tempa,i,parentn,parentn.depth+1,parentn.gcost+1,hcost)
				if childnode.gcost+childnode.hcost>maxcutoff :
					maxcutoff = childnode.gcost+childnode.hcost
				if childnode.gcost+childnode.hcost<=cutoff:
					pq.insert(childnode)
				# if childnode not in finished:
				# 	pq.insert(childnode)
				tempa=None
			finished.append(parentn)
			print('Astar indastar with cutoff ',cutoff)
	
	print('Finishing IDA*')

def astar(arr,k,n,pos0):
	print('Inside Astar')
	tempgoal = np.arange(k*k)
	goalarr = np.append(tempgoal[1:],tempgoal[0])
	
	pq = PriorityQueue()
	
	gcost=0
	hcost = heuristics(arr)
	startnode = NodeA(arr,pos0,None,0,gcost,hcost)
	pq.insert(startnode)
	# count =0
	finished =[]
	while not pq.isEmpty():
		# gcost+=1
		parentn = pq.delete()
		if parentn ==None:
			print('Queue is empty')
			break

		if(check(parentn.a,goalarr)):
			print('FOUND the sol in the ASTAR')
			# print(parentn.parentnode.a)
			printpath(parentn,k)
			return
		space = parentn.pos0

		neighbours = findneighbours(space,k)

		for i in neighbours:
			print('inside neighbourss')
			tempa = np.copy(parentn.a)
			temp=tempa[space]
			tempa[space] = tempa[i]
			tempa[i] = temp

			hcost = heuristics(tempa)

			childnode = NodeA(tempa,i,parentn,parentn.depth+1,parentn.gcost+1,hcost)
			pq.insert(childnode)
			# if childnode not in finished:
			#  	pq.insert(childnode)
			tempa=None
		finished.append(parentn)
	print('Outside Astar')


# arr = np.array([3,4,0,5,8,2,1,7,6])




# arr = np.array([1,2,3,4,5,10,6,8,13,9,7,11,14,15,12,0])
# arr = np.a/rray([1,8,2,0,4,3,7,6,5])
# arr = np.array([4,1,2,3,8,5,6,7,12,9,10,11,0,13,14,15])
# arr = np.array([1,5,2,0,4,6,7,3,8])
# n=15
# k=4
# print(isSolvable(arr,k))

# solve ai 
# k = int(input('Enter the width of the board n_puzzle = '))
# n = k*k-1
# arr=np.arange(n+1)
# np.random.shuffle(arr)
# while not isSolvable(arr,k):
# 	np.random.shuffle(arr)
# 	pass
# pos0 = int(np.where(arr==0)[0])

# print('Initial = \n')
# print(np.reshape(arr,(k,k)),' ',pos0,' ',isSolvable(arr,k))

# t = timeit.default_timer()
# if isSolvable(arr,k):
# 	bfs(arr,k,n,pos0)
# else:
# 	print('Array is not solvable')
# print('Time taken  = ',((timeit.default_timer()-t)))







 # Menu driven program
# print('Welcome to the n puzzle program')
# loop =True
# n=input('Enter the value of n for n-puzzle game = ');
# k=int(math.sqrt(n+1))
# solve = False
# arr=np.arange(n+1)
# while not isSolvable(np.random.shuffle(arr),k):
# 	pass
# pos0 = int(np.where(arr==0)[0])

# while loop:
# 	choice = input('Enter your choice (integer) ( 1->BFS , 2->DFS , 3-> A* , 4->Exit ) =')
# 	if choice==1:
# 		t = timeit.default_timer()
# 		bfs(arr,k,n,pos0)
# 		print('Time taken by BFS = ',((timeit.default_timer()-t)*100))
# 	elif choice==2:
# 		t = timeit.default_timer()
# 		dfs(arr,k,n,pos0)
# 		print('Time taken by DFS = ',((timeit.default_timer()-t)*100))
# 	elif choice==3:
# 		t = timeit.default_timer()
# 		astar(arr,k,n,pos0)
# 		print('Time taken by A* search = ',((timeit.default_timer()-t)*100))
# 	elif choice==4:
# 		loop=False
# 		print('Exiting')
# 	else:
# 		print('Enter a valid option')

		

	


