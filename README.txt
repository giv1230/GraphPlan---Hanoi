Course			Introduction to Artificial Intelligence 20551
Mamman #		15
Name			Eli Kesem
ID				
Date			01/06/2017

Question 1:
	I took two actions and checked each delete list, to see if it interferes with a precondition or a positive effect
	of the other one.

Question 2:
	I've looped through a1 and a2 preconditions and searched for a single pair of preconditions that are mutex.

Quetsion 3:
	I've looped through each of prop1 and prop2 action producers, and checked if there is a pair of actions that aren't
	in mutexActions.

Quetsion 4:
	I've looped through the actions that their preconditions are fullfilled in the previous proposition layer, and added
	them to the current action list, if it doesn't already exist.

Quetsion 5:
	I've looped through the actions and checked if they were mutex actions in the previous mutex proposition layer. If they
	did, we added them to the current mutex list, if it doesn't already exist.

Quetsion 6:
	I've looped through the actions and their add list. For every add operation, I've added the added proposition to the list,
	and also updated its producer, if not already exist.

Quetsion 7:
	I've looped through the propositions and checked if they are mutex propositions in the current mutex action layer. If they
	did, we added them to the current mutex list, if it doesn't already exist.

Quetsion 8:
	I've simply called the functions that I've implemented in the last questions: updateActionLayer, updateMutexActions,
	updatePropositionLayer and updateMutexProposition.

Quetsion 9:
	For at least 8 actions (without noOps) I suggested the following state:
		Initial state: r1 q1 a2 b2 ur uq   
		Goal state: a1 b1
	Which it means that both robots are at location 1, empty-handed, and they need to grab the containers from location
	2 and put it back into location 1. This takes 8 mutexActions.

	For the impossible goal state, we can just use:
		Goal state: a1 a2
	Because the robot r cannot be at location 1 and 2 at the same time, there is no solution.

Quetsion 10:
	Implementing getStartState is just returning self.initialState.

	Implementing isGoalState is checking if all goal states are in our current state.

	Implementing getSuccessors means going through all the actions are are not noOps, and that have all preconditions met in
	the current state.
	For each action, we're going to add a successor. We'll compute the new propositions by taking the current state, plus the
	action additions, minus the action deletions.
	The step cost is going to be 1.
	Then we'll return all the new calculated successors.

	While using the null heuristic, 486 search nodes were expanded.

Quetsion 11:
	We first create a new proposition layer and update it.
	Then we create the graph levels, expanding one level in a time.
	In each level expansion, we check two things:
	* If we reach the goal state, we exit and return the level.
	* If the graph is fixed and expansions didn't change in the last level, it means that we can't reach the goal state, and
	we return infinity.
	Otherwise we keep on expanding.

	For this to work, I've implemented the expandWithoutMutex function on planGraphLevel, which works like expand but without
	the mutexes.

	While using the maxLevel heuristic, 64 search nodes were expanded (86.8% less expansions).

Quetsion 12:
	Heuristic is similliar to maxLevel, but now at each level expansion, we're checking if we found any goal state, and it we
	do, we add it to a sum.
	We're returing the sum when we're done expansion.
	We're still returning infinity if we can't reach all the goal states, just like in the maxLevel heuristic.

	While using the levelSum heuristic, 8 search nodes were expanded (87.5% less expansions than maxLevel, 98.3% less expansions than null).

Quetsion 13:
	I've implemented the domain file in the right format.
	I've created the right propositions according to the hanoi problem:
	* clear peg
	* disk on peg
	* disk on top
	* disk on bottom
	* disk on disk

	And the actions:
	* move disk to empty peg
	* move last disk from peg to a non-empty peg
	* move last disk from peg to a empty peg
	* move disk from non-empty peg to a non-empty peg

Quetsion 14:
	I've implemented the problem file in the right format.
	I've created the right problem settings according to the hanoi problem.

	Initial state is:
	* pegs b,c are clear
	* disks are on top each other in the right order on peg a

	Goal state:
	* pegs a,b are clear
	* disks are on top each other in the right order on peg c

