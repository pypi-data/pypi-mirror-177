def search_theory():
    print('''


Search:

Agent:
An entity that perceives its environment and acts upon that environment. In a navigator app, for example, the agent would be a representation of a car that needs to decide on which actions to take to arrive at the destination.
State:
A configuration of an agent in its environment. For example, in a 15 puzzle a state is any one way that all the numbers are arranged on the board.
Initial State: 
The state from which the search algorithm starts. In a navigator app, that would be the current location.
Actions:
choices that can be made in a state.
Transition Model:
A description of what state results from performing any applicable action in any state. More precisely, the transition model can be defined as a function.
State Space:
The set of all states reachable from the initial state by any sequence of actions.
Goal Test:
The condition that determines whether a given state is a goal state. 
Path Cost: 
A numerical cost associated with a given path. 

Information In a Node
In a search process, data is often stored in a node, a data structure that contains the following data:
1.	A state
2.	Its parent node, through which the current node was generated
3.	The action that was applied to the state of the parent to get to the current node
4.	The path cost from the initial state to this node

Uninformed Search:

DFS :- 
A Depth-first search algorithm exhausts all existing options Prior to pursuing a new approach. In such situations, the frontier is controlled by a stack data structure. Here, "last-in, first-out" is the term you follow in DFS. The first node to remove and take into account is the final node put to the frontier after nodes have been added. This leads to a search algorithm that prioritises the first direction that gets in its way and travels as far as it can in that direction, leaving all other directions for later.
Stack: Here we use stack for the implementation of the Search Where the LIFO is Performed and which helps in DFS. 
Advantages:
1. Less time and space complexity rather than BFS.
2. The solution can be found out without much more search.

Cons:
Not Guaranteed that it will give you a solution

Example:
The time complexity of the DFS algorithm is O(V+E), where V is the number of vertices and E is the number of edges in the graph. The space complexity of the DFS algorithm is O(V).
1.	For finding the path
2.	To test if the graph is bipartite
3.	For finding the strongly connected components of a graph
4.	For detecting cycles in a graph

Psuedo:
# Define the function that removes a node from the frontier and returns it.
    def remove(self):
    	  # Terminate the search if the frontier is empty, because this means that there is no solution.
        if self.empty():
            raise Exception("empty frontier")
        else:
        	  # Save the last item in the list (which is the newest node added)
            node = self.frontier[-1]
            # Save all the items on the list besides the last node (i.e. removing the last node)
            self.frontier = self.frontier[:-1]
            return node

BFS
A breadth-first search algorithm will follow multiple directions at the same time , one in each direction that is possible, before taking a second step in each direction. The frontier is controlled in this instance as a queue data structure. First-in, first-out is the term you need to keep in mind in this situation. The order in which the new nodes are examined in this situation is determined by which one was added first (first come, first served!). Due to this, the search algorithm first moves in every direction before moving in any one direction again.

•	                     Pros:
o	This algorithm is guaranteed to find the optimal solution.
o	This algorithm is guaranteed to find the optimal solution.
•	Cons:
o	This algorithm is almost guaranteed to take longer than the minimal time to run.
o	At worst, this algorithm takes the longest possible time to run.

Example:
(An example from outside lecture: suppose you are in a situation where you are looking for your keys. In this case, if you start with your pants, you will look in your right pocket. After this, instead of looking at your left pocket, you will take a look in one drawer. Then on the table. And so on, in every location you can think of. Only after you will have exhausted all the locations will you go back to your pants and search in the next pocket. Define the function that removes a node from the frontier and returns it.
    def remove(self):
    	  # Terminate the search if the frontier is empty, because this means that there is no solution.
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Save the oldest item on the list (which was the first one to be added)
            node = self.frontier[0]
            # Save all the items on the list besides the first one (i.e. removing the first node)
            self.frontier = self.frontier[1:]
            return node




Rational agent:
A rational agent is one that does the right thing—conceptually speaking, every entry in the table for the agent function is filled out correctly

Environment Sensors:
An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators.  

Percept:
We use the term percept to refer to the agent’s perceptual inputs at any given instant. An agent’s percept sequence is the complete history of everything the agent has ever perceived.

Informed  search:

Greedy Best First Search:
Greedy best-first search expands the node that is the closest to the goal, as determined by a heuristic function h(n). As its name suggests, the function estimates how close to the goal the next node is, but it can be mistaken. The efficiency of the greedy best-first algorithm depends on how good the heuristic function is. For example, in a maze, an algorithm can use a heuristic function that relies on the Manhattan distance between the possible nodes and the end of the maze. The Manhattan distance ignores walls and counts how many steps up, down, or to the sides it would take to get from one location to the goal location. This is an easy estimation that can be derived based on the (x, y) coordinates of the current location and the goal location.

A* Search :
A development of the greedy best-first algorithm, A* search considers not only h(n), the estimated cost from the current location to the goal, but also g(n), the cost that was accrued until the current location. By combining both these values, the algorithm has a more accurate way of determining the cost of the solution and optimizing its choices on the go. The algorithm keeps track of (cost of path until now + estimated cost to the goal), and once it exceeds the estimated cost of some previous option, the algorithm will ditch the current path and go back to the previous option, thus preventing itself from going down a long, inefficient path that h(n) erroneously marked as best.

For A* search to be optimal, the heuristic function, h(n), should be:
1.	Admissible, or never overestimating the true cost, and
2.	Consistent, which means that the estimated path cost to the goal of a new node in addition to the cost of transitioning to it from the previous node is greater or equal to the estimated path cost to the goal of the previous node. To put it in an equation form, h(n) is consistent if for every node n and successor node n’ with step cost c, h(n) ≤ h(n’) + c.

A* Search Algorithm
1.  Initialize the open list
2.  Initialize the closed list
    put the starting node on the open 
    list (you can leave its f at zero)
3.  while the open list is not empty
    a) find the node with the least f on 
       the open list, call it "q"
     b) pop q off the open list
     c) generate q's 8 successors and set their 
       parents to q
     d) for each successor
        i) if successor is the goal, stop search
        
        ii) else, compute both g and h for successor
          successor.g = q.g + distance between 
                              successor and q
          successor.h = distance from goal to 
          successor (This can be done using many 
          ways, we will discuss three heuristics- 
          Manhattan, Diagonal and Euclidean 
          Heuristics)
          
          successor.f = successor.g + successor.h

        iii) if a node with the same position as 
            successor is in the OPEN list which has a 
           lower f than successor, skip this successor

        iV) if a node with the same position as 
            successor  is in the CLOSED list which has
            a lower f than successor, skip this successor
            otherwise, add  the node to the open list
     end (for loop)
  
    e) push q on the closed list
    end (while loop)


Adverserial Search:
 
Minimax 
A type of algorithm in adversarial search, Minimax represents winning conditions as (-1) for one side and (+1) for the other side. Further actions will be driven by these conditions, with the minimizing side trying to get the lowest score, and the maximizer trying to get the highest score.

o	Mini-max algorithm is a recursive or backtracking algorithm which is used in decision-making and game theory. It provides an optimal move for the player assuming that opponent is also playing optimally.
o	Mini-Max algorithm uses recursion to search through the game-tree.
o	Min-Max algorithm is mostly used for game playing in AI. Such as Chess, Checkers, tic-tac-toe, go, and various tow-players game. This Algorithm computes the minimax decision for the current state.
o	In this algorithm two players play the game, one is called MAX and other is called MIN.
o	Both the players fight it as the opponent player gets the minimum benefit while they get the maximum benefit.
o	Both Players of the game are opponent of each other, where MAX will select the maximized value and MIN will select the minimized value.
o	The minimax algorithm performs a depth-first search algorithm for the exploration of the complete game tree.
o	The minimax algorithm proceeds all the way down to the terminal node of the tree, then backtrack the tree as the recursion.
Properties
o	Complete- Min-Max algorithm is Complete. It will definitely find a solution (if exist), in the finite search tree.
o	Optimal- Min-Max algorithm is optimal if both opponents are playing optimally.
o	Time complexity- As it performs DFS for the game-tree, so the time complexity of Min-Max algorithm is O(bm), where b is branching factor of the game-tree, and m is the maximum depth of the tree.
o	Space Complexity- Space complexity of Mini-max algorithm is also similar to DFS which is O(bm).

Limitation of the minimax Algorithm:
The main drawback of the minimax algorithm is that it gets really slow for complex games such as Chess, go, etc. This type of games has a huge branching factor, and the player has lots of choices to decide. This limitation of the minimax algorithm can be improved from alpha-beta pruning which we have discussed in the next topic.

Pseudo code 
Function Max-Value(state): 
   If terminal(state): 
      Return utility(state)
   v = -infinity 
   For action in Actions(state): 
      v = Max(v,Min-Value (Result(state,action)))
   Return v 


Function Min-Value(state): 
   If terminal(state): 
      Return utility(state)
   v = infinity 
   For action in Actions(state): 
      v = Min(v,Max-Value (Result(state,action)))
   Return v



Alpha-beta pruning:
•	It skips some unfavorable recursive computations.
•	After establishing one action, if it is seen that it can be a better score for the opponent than the previously established action.
•	Then there is no need of investigating that action ahead because it will be less favorable than the previous action for us.
Alpha-Beta Pruning
A way to optimize Minimax, Alpha-Beta Pruning skips some of the recursive computations that are decidedly unfavorable. After establishing the value of one action, if there is initial evidence that the following action can bring the opponent to get to a better score than the already established action, there is no need to further investigate this action because it will decidedly be less favorable than the previously established one.
This is most easily shown with an example: a maximizing player knows that, at the next step, the minimizing player will try to achieve the lowest score. Suppose the maximizing player has three possible actions, and the first one is valued at 4. Then the player starts generating the value for the next action. To do this, the player generates the values of the minimizer’s actions if the current player makes this action, knowing that the minimizer will choose the lowest one. However, before finishing the computation for all the possible actions of the minimizer, the player sees that one of the options has a value of three. This means that there is no reason to keep on exploring the other possible actions for the minimizing player. The value of the not-yet-valued action doesn’t matter, be it 10 or (-10). If the value is 10, the minimizer will choose the lowest option, 3, which is already worse than the preestablished 4. If the not-yet-valued action would turn out to be (-10), the minimizer will this option, (-10), which is even more unfavorable to the maximizer. Therefore, computing additional possible actions for the minimizer at this point is irrelevant to the maximizer, because the maximizing player already has an unequivocally better choice whose value is 4.
 


Depth-Limited Minimax
There is a total of 255,168 possible Tic Tac Toe games, and 10²⁹⁰⁰⁰ possible games in Chess. The minimax algorithm, as presented so far, requires generating all hypothetical games from a certain point to the terminal condition. While computing all the Tic-Tac-Toe games doesn’t pose a challenge for a modern computer, doing so with chess is currently impossible.
Depth-limited Minimax considers only a pre-defined number of moves before it stops, without ever getting to a terminal state. However, this doesn’t allow for getting a precise value for each action, since the end of the hypothetical games has not been reached. To deal with this problem, Depth-limited Minimax relies on an evaluation function that estimates the expected utility of the game from a given state, or, in other words, assigns values to states. For example, in a chess game, a utility function would take as input a current configuration of the board, try to assess its expected utility (based on what pieces each player has and their locations on the board), and then return a positive or a negative value that represents how favorable the board is for one player versus the other. These values can be used to decide on the right action, and the better the evaluation function, the better the Minimax algorithm that relies on it.

''')

search_theory()