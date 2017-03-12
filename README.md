# Maze
The algorithm implemented was an A* algorithm using the manhattan distance heuristic.

The program reads the starting and ending locations as well as all the locations of the traps.
The agent then starts moving in the direction of the exit.  
If the agent sees a trap then the location of the traps location, 
as well as the adjacent spaces if the trap is a spider,
and marks those as locations that cannot be traveled through. 
The agent also favors paths that it has not taken over paths that it has already visited.  
The agent avoids the spaces with extra cost unless it see’s that it can get closer to the goal by going through it.


heuristic:
	distance X = abs( agent(x) - finish(x) )
	distance Y = abs( agent(y) - finish(y) )
	return 1 * ( distance x + distance y )


because the agent prefers paths not taken the agent may wander around until it gets to a point where all
available open states are states that have already been visited before heading back in the direction of the exit

#error always goes through same path forgot to make random choice when each path is considered equal
