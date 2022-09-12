# -*- coding: utf-8 -*-
"""A* algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RaKUTivTBo-bA952pHbjH19xic_2ROL4
"""

def Find_Nearest(box,storages,restrictions,method):
    remain_storages = []
    for s in storages:
        if (restrictions is not None):
            if {s} not in restrictions:
                remain_storages.append(s)
        else:
            remain_storages.append(s)
    remain_storages = np.array(remain_storages)
    box = np.array(box)
    if method == 'manhattan_distance':
        best_h = np.sum(np.abs(box-remain_storages[0]))
        for i in range(1,len(remain_storages)):
            h = np.sum(np.abs(box-remain_storages[i]))
            if h<best_h:
                best_h = h
    elif method == 'euclidean_distance':
        best_h = np.sum((box-remain_storages[0])**2)
        for i in range(1,len(remain_storages)):
            h = np.sum((box-remain_storages[i])**2)
            if h<best_h:
                best_h = h
    return best_h

"""In this Problem, We want to use A* algorithm to present a solution for an interesting game that we called it, Push Till Redemption. :) <br/>
First, we introduce you to some major features of this game. <br/>

In this game, we have a map with **M** $\times$ **N** dimensions covered by a one-layer wall. i.e., The **M-2** $\times$ **N-2** rectangle in the middle is our usable map. <br/>
There are some boxes whose primary coordinates are specified at the start point, and also There are some specified cells which we call storage, and the most important thing is that we have an agent in this game that should push the boxes to locate them in the storage cells. In the general format of the game, each box can be placed in each storage, but sometimes our boxes may have restrictions. i.e., A specified box must be placed at specified storage. <br/>
And the last feature of this game is its obstacles; We may have some fixed obstacles in some cells of the map, which our agent can't move to cells grides and obviously can't push the boxes to those cells too..

For better inrtoduction, take a look at these two pictures. <br/>
  <img src="Images/map1.png" alt="example1" style="float: left; margin-left: 120px; width:200px;height:300px;"/>
  <img src="Images/map2.png"  style="float: left; margin-left: 250px; width:200px;height:300px;"/>

First, we should introduce symbols used in maps, In this Game, We use **#** for walls and obstacles, $*$ for boxes, **?** for the location of the agent, **-** for storage cell, and if our map had some restrictions, we highlight both the box and its corresponding storage cell with the same color. <br/>

For more clarification, we give an example for defining the state of the game at the start point. Pay attention that this example corresponds to the left map. <br/>
**An important point about defining state in this game is that we ignore border wall (i.e., two columns and two rows) in our input dimensions or coordinates.** <br/>
Don't worry if you don't understand the meaning of some of these inputs or have some questions about them; They're completely explained if they were needed.

State("START", 0, None, 4, 4,  # dimensions <br/>
&nbsp;&nbsp;&nbsp;                (0, 3),  # agent <br/>
&nbsp;&nbsp;&nbsp;                {(1, 2): 0, (1, 1): 1},  # boxes <br/>
&nbsp;&nbsp;&nbsp;                {(2, 1): 0, (2, 2): 1},  # storage <br/>
&nbsp;&nbsp;&nbsp;                frozenset(((0, 0), (1, 0), (3, 3))),  # obstacles <br/>
&nbsp;&nbsp;&nbsp;                (frozenset(((2, 1),)), frozenset(((2, 2),))),  # restrictions, <br/>
&nbsp;&nbsp;&nbsp;                {0: 'cyan', 1: 'magenta'},  # box colours <br/>
&nbsp;&nbsp;&nbsp;                {0: 'cyan', 1: 'magenta'}  # storage colours <br/>
&nbsp;&nbsp;&nbsp;                )

You should implement an A* algorithm to solve this search problem and win the game in this question.

In this problem, we provide you with some of the files to complete the functionality of the game, which you can check out as you want to know more about this game and its properties. Still, for completing this task properly, It's not necessary to check them out, and this jupyter file contains sufficient description. Besides, We provide you with some of the functions to solve the problem. Some of them are complete, but some are incomplete, and you should complete them.

## Prerequisites
"""

import numpy as np
import math
from Helper_codes.search import *
from Helper_codes.sokoban import PROBLEMS, sokoban_goal_state

"""## Heuristics

In this section, we want to investigate three different heuristics. So we explain all requirements, and you should implement these heuristics. <br/>
These functions should take a game state and Return a numeric value that serves as an estimate of the state's distance to the goal. <br/>
Each state has components like **boxes** and **storage**. <br/>
**boxes:** A dictionary where the keys are the coordinates of each box, and the values are the index of that box which is equal to the index of that box's list of restrictions if it has restrictions. <br/>
**storage:** A dictionary where the keys are the coordinates of each storage point, and the values are the index of that storage point.

### A. Displaced Boxes
"""

def heur_displaced(state):
    storage = state.storage
    storage_keys = list(storage.keys())
    storage_vals = list(storage.values())
    boxes = state.boxes
    boxes_keys = list(boxes.keys())
    boxes_vals = list(boxes.values())
    restrictions = state.restrictions
    h = 0
    if (restrictions is not None):
        for k in storage.keys():
                if ({k} in restrictions):
                    if boxes_keys[storage_keys.index(k)] != k:
                        h += 1 
                else: 
                    if (k in boxes_keys):
                        if {storage_keys[boxes_keys.index(k)]} != restrictions[storage_vals[boxes_keys.index(k)]]:
                            h += 1
                    else:
                        h += 1
    else:
        for k in storage.keys():
            if (k not in boxes_keys):
                h += 1
    return h

"""Each state has a component named **restrictions**, a tuple of frozensets of valid storage coordinates for each box. **None** means that all storage locations are valid for each box. Also we know that index of each frozenset in this tuple (**state.restrictions**), is the value of corresponding **box** in dictionary of **state.boxes** . I recommend taking another look at the sample of states defining above.

Now with these explanations, you should implement Manhattan Distance and Euclidean Distance Heuristics.

### B. Manhattan Distance
"""

def heur_manhattan_distance(state):
    storage = state.storage
    storage_keys = list(storage.keys())
    storage_vals = list(storage.values())
    boxes = state.boxes
    boxes_keys = list(boxes.keys())
    boxes_vals = list(boxes.values())
    restrictions = state.restrictions
    h = 0
    if (restrictions is not None):
         for k in boxes.keys():
                if ({storage_keys[storage_vals.index(boxes_keys.index(k))]} in restrictions):
                    x0 = k 
                    x1 = storage_keys[storage_vals.index(boxes_keys.index(k))]
                    h += np.sum(np.abs(np.array(x0)-np.array(x1)))
                else:
                    x0 = k 
                    h += Find_Nearest(x0,storage_keys,restrictions,'manhattan_distance')
    else:
        for k in boxes.keys():
            x0 = k
            h += Find_Nearest(x0,storage_keys,restrictions,'manhattan_distance')
    return h

"""### C. Euclidean Distance"""

def heur_euclidean_distance(state):  
    storage = state.storage
    storage_keys = list(storage.keys())
    storage_vals = list(storage.values())
    boxes = state.boxes
    boxes_keys = list(boxes.keys())
    boxes_vals = list(boxes.values())
    restrictions = state.restrictions
    h = 0
    if (restrictions is not None):
         for k in boxes.keys():
                if ({storage_keys[storage_vals.index(boxes_keys.index(k))]} in restrictions):
                    x0 = k 
                    x1 = storage_keys[storage_vals.index(boxes_keys.index(k))]
                    h += np.sum(np.abs(np.array(x0)-np.array(x1)))
                else:
                    x0 = k 
                    h += Find_Nearest(x0,storage_keys,restrictions,'euclidean_distance')
    else:
        for k in boxes.keys():
            x0 = k
            h += Find_Nearest(x0,storage_keys,restrictions,'euclidean_distance')
    return h

"""## Testing Heuristics

In the given files, The common version of A* algorithm is available. By running the cells below, you could see the game's result for some different game states, which are ready for you through **PROBLEMS** and actually for different kinds of heuristics.
"""

def common_astar(heur_func, P_flag):    
    solved = 0
    unsolved = []
    counter = 0
    percent = 0
    print_path = P_flag
    timebound = 2  # 2 second time limit for each problem
    print("*************************************")
    print("Running A-star with" + str(heur_func) + "Heuristic")

    for i in range(0, 10):  # note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems will get harder as i gets bigger

        se = SearchEngine('astar', 'full')
        se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_func)
        final = se.search(timebound)
        
        if final:
            solved += 1
            if print_path:
                final.print_path()
            
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")

"""Notice that the **common_astart** function get two inputs, one for determining the heuristic function and another boolean input, determines whether the final path of the solution needs to be drawn or not, So if you want to check the steps of the game, you should change that field to **True**."""

common_astar(heur_displaced, False)

common_astar(heur_manhattan_distance, False)

common_astar(heur_euclidean_distance, False)

"""Now that you have seen how your three heuristics perform in action, Please compare these three different heuristic functions from various aspects like **Search Time, Expanded Nodes, etc.** <br/>
I want you to feel free about this comparison and act as you like. For example, you can just explain your points of view in the below cell or compare the performance of these three heuristic functions with some kind of charts or graphs and explain a little about your deduction. (There's no restriction about the type of charts or graphs).
"""

x_val = ['Displaced','Manhattan','Euclidean']
fig, axs = plt.subplots(1, 3, figsize=(15, 6))
Search_Time = np.zeros(3)
Search_Time[0] = 0.09375 + 0.46875 + 0.390625 + 0.484375 + 0.421875 + 0.375 
Search_Time[1] = 0.15625 + 0.6875 + 0.578125 + 1.28125 + 1.4375 + 1.546875 
Search_Time[2] = 0.140625 + 0.53125 + 0.625 + 1.125 + 1.875 + 1.765625
axs[0].bar(x_val, Search_Time)
axs[0].title.set_text('Search Time')
Expanded_Nodes = np.zeros(3)
Expanded_Nodes[0] = 2630 + 10589 + 12827 + 16990 + 15705 + 15075
Expanded_Nodes[1] = 2358 + 10230 + 10653 + 8876 + 14254 + 14254
Expanded_Nodes[2] = 2358 + 10230 + 10653 + 7370 + 15251 + 15251
axs[1].bar(x_val, Expanded_Nodes)
axs[1].title.set_text('Expanded Nodes')
axs[2].bar(x_val, [60,60,60])
axs[2].title.set_text('Percentage of  solved problems in less than 2 seconds')
axs[2].set_ylim([0, 100])
fig.suptitle('Heuristics Perform')

"""## Anytime weighted A*

In this section, We want you to implement another A* algorithm which is named **anytime weighted A*** in this algorithm, and we take the initial state of the game, heuristic function, weight, and timebound as inputs which **weight** is the factor which determines the impact of heuristic in calculating f_value (g + w\*h) and **timebound** is the number of seconds that we have for running this algorithm. And Output of this function is a **goal state of search** (if a goal is found), else **FALSE**. <br/>
In this version of A*, we aim to find the optimal path and optimal goal. So while there is time, we call the search method of the search engine (**se**) and we look for a path with minimum cost and to save time, We use cost-bounder to prune states which have bigger f_value than the best path cost we found so far. Costbounder is a three tuple that is like (g_val, h_val, g_val + h_val) which each of these 3 are like limit for pruning successor state. Please pay attention that in this version, we prune only when the current final f is larger than best_path_cost<br/>
As you can see in the function below, first we save the f_value function, which is affected by weight, into **wrapped_fval_function** then we make a search engine and call its **init_search**. <br/>
For calculating goal value to compare with best path cost that was found, We use **final.gval + heur_fn(final)** which **final** is the goal state in case is found.
"""

def fval_function(sN, weight):
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    return sN.gval + weight * sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # initialization
    best_path_cost = float("inf")
    time_remain = 8
    iter = 0

    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    while (time_remain > 0) and not se.open.empty():
        ################################################
        # (4 Points)                                   #
        # Complete this loop                           #
        # with information we gave you before.         #
        ################################################
        pass
    try:
        return optimal_final
    except:
        return final

    return False

"""## Running the Game"""

def run_astar(P_flag):
    solved = 0
    unsolved = []
    counter = 0
    percent = 0
    print_path = P_flag
    timebound = 8  # 8 second time limit
    print("Running Anytime Weighted A-star")

    for i in range(0, 10):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        weight = 10
        final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)

        if final:
            solved += 1
            if print_path:
                final.print_path()
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")

"""Notice that the **run_astart** function get one input which is boolean. It determines whether the solution's final path is drawn or not, So if you want to check the steps of the game, you should change that field to **True**."""

run_astar(False)

"""Compare these versions of the A* algorithm with the common version you knew before and mention its advantages."""