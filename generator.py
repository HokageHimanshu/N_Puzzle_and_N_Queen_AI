import numpy as np
import random

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

def swapsit(arr,iterations,k):
	
	# length = len(arr)
	
	for i in range(iterations):
		pos0 = int(np.where(arr==0)[0])
		neigh = findneighbours(pos0,k)
		index2 = int(neigh[random.randint(0,len(neigh)-1)])
		# print(index2)
		temp = arr[pos0]
		arr[pos0] = arr[index2]
		arr[index2] = temp
	return arr



sizen = int(input('Enter the the value of n  = '))

fd=open('input_npuz.txt','w')

for i in range(2,sizen):
	for j in range(5):
		k = i
		n= k*k-1
		temparr = np.arange(n+1)
		arr = np.append(temparr[1:],temparr[0])
		print(arr)
		# print(arr)
		modified_list = swapsit(arr,random.randint(0,10),k)
		line = str(k) + ' ' + str(modified_list)
		fd.write(line)
		fd.write('\n')

fd.close()





