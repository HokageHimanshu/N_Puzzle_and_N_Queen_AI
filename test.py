from nqueues import *
from n_puzzle import *
import time
from statistics import mean
import numpy as np
import sys

print('Stats Generation')
loop = True
while loop:
	ch = input('1) n_puzzle, 2) nquenes, 3)Exit. Enter your choice  =')
	ch = int(ch)
	if ch==1:
		# k = int(input('Enter the width of the board n_puzzle = '))
		k=3
		n = k*k-1
		# arr=np.arange(n+1)
		
		s='4 1 2 8 0 3 7 6 5'
		lstr =s.split()
		templ = []
		for i in lstr:
			# print(i)
			templ.append(int(i))
		# print('templ',templ)

		arr = np.array(templ)
		fd = open('vals_npuzzle.txt','w')
		lbfs = []
		ldfs = []
		lstar = []
		lidastar = []
		# np.random.shuffle(arr)
		while not isSolvable(arr,k):
			np.random.shuffle(arr)
			pass
		pos0 = int(np.where(arr==0)[0])

		t_bfs_start = time.time()
		bfs(arr,k,n,pos0)
		t_bfs_end = time.time()

		t_dfs_start = time.time()
		dfs(arr,k,n,pos0)
		t_dfs_end = time.time()

		t_astar_start = time.time()
		astar(arr,k,n,pos0)
		t_astar_end = time.time()

		t_idastar_start = time.time()
		idastar(arr,k,n,pos0)
		t_idastar_end = time.time()

		lbfs.append(t_bfs_end-t_bfs_start)
		ldfs.append(t_dfs_end-t_dfs_start)
		lstar.append(t_astar_end-t_astar_start)
		lidastar.append(t_idastar_end-t_idastar_start)

		line = str(n)+' => '+str(round(mean(lbfs),4))+' , '+str(round(mean(ldfs),4))+' , '+str(round(mean(lstar),4))+' '+str(round(mean(lidastar),4))
		fd.write(line)
		fd.write('\n')
		fd.close()

	elif ch==2:
		limit = int(input('Enter the upper value of n (>=4) in n quenes ='))
		fd = open('vals_nqueens.txt','w')
		store =[]
		for i in range(4,limit+1):
			store.append(stats1(i,5))
			line = str(i) + ' ' +str(store[i-4][0]) +' '+str(store[i-4][1])
			fd.write(line)
			fd.write('\n')
			print(i,' = ',store[i-4])
		fd.close()

	elif ch==3:
		loop=False
	else :
		print('Enter a valid option')
