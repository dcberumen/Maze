#!/usr/bin/python3.5
# CPSC 481 Artificial Intelligence
# Assignment 1: Maze
import math
import random
import sys
import re

def heuristic_cost_estimate(agentx,agenty,endx,endy):
	#manhattan distance
	dx = abs(agentx - endx)
	dy = abs(agenty - endy)
	return 1 * (dx + dy)


def vision(agentx,agenty, unsafe, quicksand, spider):
	#see up to two spaces ahead
	#check to see any spaces that are 1 or 2 spaces ahead, behind, left, and right
	#if any spaces can capture the agent mark them as unsafe
	for x in range(1,3):
		if [agentx+x, agenty] in quicksand and [agentx+x, agenty] not in unsafe:
			unsafe.append([agentx+x,agenty])
		if [agentx-x, agenty] in quicksand and [agentx-x, agenty] not in unsafe:
			unsafe.append([agentx-x, agenty])
		if [agentx, agenty+x] in quicksand and [agentx, agenty+x] not in unsafe:
			unsafe.append([agentx, agenty+x])
		if [agentx, agenty-x] in quicksand and [agentx, agenty-x] not in unsafe:
			unsafe.append([agentx, agenty-x])

		if [agentx+x, agenty] in spider:
			if [agentx+x, agenty] not in unsafe:
				unsafe.append([agentx+x, agenty])
			if [agentx+x+1,agenty] not in unsafe:
				unsafe.append([agentx+x+1,agenty])
			if [agentx+x-1,agenty] not in unsafe:
				unsafe.append([agentx+x-1, agenty])
			if [agentx+x,agenty+1] not in unsafe:
				unsafe.append([agentx+x, agenty+1])
			if [agentx+x, agenty-1] not in unsafe:
				unsafe.append([agentx+x, agenty-1])

		if [agentx-x, agenty] in spider:
			if [agentx-x, agenty] not in unsafe:
				unsafe.append([agentx-x, agenty])
			if [agentx-x+1,agenty] not in unsafe:
				unsafe.append([agentx-x+1,agenty])
			if [agentx-x-1,agenty] not in unsafe:
				unsafe.append([agentx-x-1, agenty])
			if [agentx-x,agenty+1] not in unsafe:
				unsafe.append([agentx-x, agenty+1])
			if [agentx-x, agenty-1] not in unsafe:
				unsafe.append([agentx-x, agenty-1])
		
		if [agentx, agenty+x] in spider:
			if [agentx, agenty+x] not in unsafe:
				unsafe.append([agentx, agenty+x])
			if [agentx+1,agenty+x] not in unsafe:
				unsafe.append([agentx+1,agenty+x])
			if [agentx-1,agenty+x] not in unsafe:
				unsafe.append([agentx-1, agenty+x])
			if [agentx,agenty+x+1] not in unsafe:
				unsafe.append([agentx, agenty+x+1])
			if [agentx, agenty+x-1] not in unsafe:
				unsafe.append([agentx, agenty+x-1])

		if [agentx, agenty-x] in spider:
			if [agentx, agenty-x] not in unsafe:
				unsafe.append([agentx, agenty-x])
			if [agentx+1,agenty-x] not in unsafe:
				unsafe.append([agentx+1,agenty-x])
			if [agentx-1,agenty-x] not in unsafe:
				unsafe.append([agentx-1, agenty-x])
			if [agentx,agenty+1-x] not in unsafe:
				unsafe.append([agentx, agenty+1-x])
			if [agentx, agenty-1-x] not in unsafe:
				unsafe.append([agentx, agenty-1-x])
	
	#check the diagnal from agent position (can only view 1,1 ahead)
	#important for spider traps so agent doesnt trigger them
	if [agentx+1,agenty+1] in spider:
		if [agentx+2,agenty+1] not in unsafe:
			unsafe.append([agentx+2, agenty+1])
		if [agentx, agenty+1] not in unsafe:
			unsafe.append([agentx,agenty+1])
		if [agentx+1, agenty] not in unsafe:
			unsafe.append([agentx+1, agenty])
		if [agentx+1,agenty+2] not in unsafe:
			unsafe.append([agentx+1,agenty+2])

	if [agentx+1, agenty-1] in spider:
		if [agentx+2,agenty-1] not in unsafe:
			unsafe.append([agentx+2, agenty+1])
		if [agentx, agenty-1] not in unsafe:
			unsafe.append([agentx,agenty+1])
		if [agentx+1, agenty] not in unsafe:
			unsafe.append([agentx+1, agenty])
		if [agentx+1,agenty-2] not in unsafe:
			unsafe.append([agentx+1,agenty-2])

	if [agentx-1, agenty-1] in spider:
		if [agentx,agenty-1] not in unsafe:
			unsafe.append([agentx, agenty-1])
		if [agentx-2, agenty-1] not in unsafe:
			unsafe.append([agentx-2,agenty-1])
		if [agentx-1, agenty] not in unsafe:
			unsafe.append([agentx-1, agenty])
		if [agentx-1,agenty-2] not in unsafe:
			unsafe.append([agentx-1,agenty-2])

	if [agentx-1, agenty+1] in spider:
		if [agentx, agenty+1] not in unsafe:
			unsafe.append([agentx, agenty+1])
		if [agentx-2, agenty+1] not in unsafe:
			unsafe.append([agentx-2, agenty+1])
		if [agentx-1, agenty+2] not in unsafe:
			unsafe.append([agentx-1, agenty+2])
		if [agentx-1, agenty] not in unsafe:
			unsafe.append([agentx-1, agenty])



	return(unsafe)

def A(ax, ay, endx, endy, quicksand, spider, c, expense):
	#set of nodes already evaluated will be erased if a dead end has been hit
	closedSet = []
	#possible moves for agent starts as starting point
	openSet = [[ax,ay]]
	#the locations of traps
	unsafe = []
	#will mainly be used to suggest new paths over the same path in case of backtracking
	cameFrom = []

	gScore = [[math.inf]*20 for x in range(20)]
	gScore[ax][ay] = 0

	fScore = [[math.inf]*20 for x in range(20)]
	fScore[ax][ay] = heuristic_cost_estimate(ax,ay,endx,endy)
	currentX = ax
	currentY = ay
	#contains the entire path
	PathTakenL = []

	while len(openSet) != 0:
		#let the agent move to the space with lowest fscor value
        #because didnt create new list of equal values leads to agent always taking same path
		mFscore = 100
		for x in openSet:
			y = x[0]
			z = x[1]
			if fScore[y][z] <= mFscore:
				mFscore = fScore[y][z]
				currentX = x[0]
				currentY = x[1]

        #also causes agent to take same path should have chosen random path instead
		#if the agent forgot to move
		if [currentX,currentY] not in openSet:
			openSet = sorted(openSet)
			currentX = openSet[0][0]
			currentY = openSet[0][1]

		#add the new space to path
		PathTakenL.append([currentX,currentY])
		
		#if the exit has been found
		if currentX == endx and currentY == endy:
			o = open('output.txt', 'w')
			
			totalcost = 0
			
			for x in range(len(PathTakenL)):
				if PathTakenL[x] in c:
					for y in c:
						if PathTakenL[x] == y:
							totalcost += expense[c.index(y)]
				totalcost += 1
			o.write("Total cost: ${} \n".format(totalcost))
			o.write('Total number of steps taken: {}\n'.format(len(PathTakenL)))
			o.write('Traveled rout: {}'.format(PathTakenL))
			o.close()
			return PathTaken (cameFrom, currentX, currentY)

		#prevent agent from staying in same place
		openSet.remove([currentX,currentY])
		#dont let the agent go back and forth
		closedSet.append([currentX,currentY])

		neighbor = []
		unsafe = vision(currentX,currentY, unsafe, quicksand, spider)

		#potential next moves
		if currentX + 1 < 20 and [currentX+1,currentY] not in closedSet and [currentX+1,currentY] not in unsafe:
			neighbor.append([currentX + 1,currentY])

		if currentX - 1 >= 0 and [currentX-1,currentY] not in closedSet and [currentX-1,currentY] not in unsafe:
			neighbor.append([currentX - 1,currentY])

		if currentY + 1 < 20 and [currentX,currentY+1] not in closedSet and [currentX,currentY+1] not in unsafe:
			neighbor.append([currentX, currentY + 1])

		if currentY - 1 >= 0 and [currentX,currentY-1] not in closedSet and [currentX,currentY-1] not in unsafe:
			neighbor.append([currentX, currentY - 1])

		openSet= []
		for x in range(len(neighbor)):

			temp_gScore = gScore[currentX][currentY] + abs(currentX - neighbor[x][0]) + abs(currentY - neighbor[x][1])
			#prepare possible moves
			if neighbor[x] not in openSet:
				openSet.append(neighbor[x])

			elif temp_gScore >= gScore[currentX][currentY]:
				continue
			#favor unexplored spaces
			if neighbor[x] in PathTakenL:
				cameFrom.append([currentX,currentY])
				nx = neighbor[x][0]
				ny = neighbor[x][1]
				gScore[nx][ny] = temp_gScore
				fScore[nx][ny] += gScore[nx][ny] + heuristic_cost_estimate(neighbor[x][0],neighbor[x][1],endx,endy) + 2
				
			else:	
				cameFrom.append([currentX,currentY])
				nx = neighbor[x][0]
				ny = neighbor[x][1]
				gScore[nx][ny] = temp_gScore
				fScore[nx][ny] = gScore[nx][ny] + heuristic_cost_estimate(neighbor[x][0],neighbor[x][1],endx,endy)
		#in case of dead end
		if len(openSet) == 0:
			openSet.append(closedSet[len(closedSet)-2])
			closedSet = []
			closedSet.append([currentX,currentY])

	
	return ("Failure")

def PathTaken(cameFrom,currentX,currentY):
	total_path = [[currentX,currentY]]
	while [currentX,currentY] in cameFrom:
		currentX = cameFrom[currentX][0]
		currentY = cameFrom[currentX][1]
		total_path.append([currentX,currentY])
	return (total_path)

def main():
	f = open('input.txt')

	start = f.readline()
	start = re.sub('[(),]', ' ', start)
	start = list(map(int,start.split()))

	end = f.readline()
	end = re.sub('[(),]', ' ', end)
	end = list(map(int, end.split()))

	qs = f.readline()
	qs = re.sub('[(),]', ' ', qs)
	qs = list(map(int,qs.split()))
	quicksand = []
	for x in range(0,len(qs),2):
		quicksand.append([qs[0],qs[1]])
		qs.pop(0)
		qs.pop(0)

	sp = f.readline()
	sp = re.sub('[(),]', ' ', sp)
	sp = list(map(int,sp.split()))
	spider = []
	for x in range(0,len(sp),2):
		spider.append([sp[0],sp[1]])
		sp.pop(0)
		sp.pop(0)

	cost = f.readline()
	cost = re.sub('[(),:]', ' ', cost)
	expense = []
	c = []
	cost = list(map(int, cost.split()))
	for x in range(0,len(cost), 3):
		expense.append(cost[0])
		c.append([cost[1],cost[2]])
		cost.pop(0)
		cost.pop(0)
		cost.pop(0)
	
	A(start[0], start[1], end[0], end[1], quicksand, spider, c, expense)
	f.close()
if __name__ == '__main__':
	main()


