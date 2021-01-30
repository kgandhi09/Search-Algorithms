from SearchEnum import SearchEnum
import Graph
import sys
from collections import OrderedDict
from Graph import State
# Template for Project 1 of CS 4341 - A2020

def print_queue(queue, node):
    if len(queue) > 0:
        print("      ", end="")
        print(node[0][0].name, end="")
        print("       ", end="")
        print('[', end="")
        for node in queue:
            print("<", end="")
            for state in node[0]:
                print(state.name, end = "")
                if state != node[0][-1]:
                    print(",", end="")
            print(">", end="")
            # print(node[1], end="")        #print this line to get cost and heuristic info
            if node != queue[-1]:
                print(" ", end = "")
        print('] ')
    # print(curr_limit)

def General_Search(problem, searchMethod):
    """
    Return the solution path or failure to reach state G from state S. 
    
    Parameters
    ----------
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """
    initialState = 'S' # name of the initial state
    finalState = 'G' # Name of the final state
    solution = finalState
    # Make_Queue, Make_Queue_Node, Remove_Front, Terminal_State, Expand, and expand_queue are to be implemented by the student. 
    # Implementation of the below pseudocode may vary slightly depending on the data structures used.
    
    queue = Make_Queue(Make_Queue_Node(problem.getState(initialState))) # Initialize the data structures to start the search at initialState
    depth_limit_iterative = 1
    explored = []
    uninformed_search = ["Depth 1st search", "Breadth 1st search", "Depth-limited search (depth-limit = 2)","Iterative deepening search"]
    informed_search = ["Uniform Search (Branch-and-bound)", "Greedy Search", "A*", "Hill climbing without backtracking", "Beam search (w = 2)"]
    search_type = " "

    if searchMethod.value in uninformed_search:
        search_type = "uninformed"
    elif searchMethod.value in informed_search:
        search_type = "informed"

    print("Expanded      Queue")
    if not searchMethod.value == "Iterative deepening search":
        print_queue(queue, queue[0])
    else:
        print("L=0")
        print_queue(queue, queue[0])

    while len(queue) > 0:
        node = Remove_Front(queue) # Remove and return the node to expand from the queue
        if Terminal_State(node) is solution: # solution is not a defined variable, but this statement represents checking whether you have expanded the goal node.
            return node # If this is a solution, return the node containing the path to reach it.
        explored.append(Terminal_State(node))    
        opened_nodes = Expand(problem, node) # Get new nodes to add to the queue based on the expanded node 
        
        if search_type == "uninformed":
            for elem in opened_nodes:
                if elem[0][0].name in explored:
                    opened_nodes.remove(elem)

        elif search_type == "informed": 
            for elem in opened_nodes:
                if elem[0][0].name in explored:
                    opened_nodes.remove(elem)
                for node in queue:
                    if elem[0][0].name == node[0][0].name:
                        if node[1][0] < elem[1][0]:
                            opened_nodes.remove(elem)

        queue = expand_queue(queue,opened_nodes,problem,searchMethod, depth_limit_iterative)

        if searchMethod.value == "Iterative deepening search":
            if len(queue) == 0:
                depth_limit_iterative += 1
                explored = []
                queue = Make_Queue(Make_Queue_Node(problem.getState(initialState)))   
                print()
                print("L=", end="")
                print(depth_limit_iterative) 
                print_queue(queue, queue[0])
    return False

def expand_queue(queue, nodesToAddToQueue, problem, search, depth_limit_iterative):
    """
    Add the new nodes created from the opened nodes to the queue based on the search strategy.

    Parameters
    ----------
    queue 
        The queue containing the possible nodes to expand upon for the search.
    newNodesToAddToQueue : list
        The list of nodes to add to the queue.
    problem : Graph.Graph
        The graph to search from S to G.
    searchMethod : SearchEnum
        The search method to use to search the graph.
    """
    # Fill in the below if and elif bodies to implement how the respective searches add new nodes to the queue.
    if search == SearchEnum.DEPTH_FIRST_SEARCH:
        for i in range(len(nodesToAddToQueue) -1, -1, -1):
            queue.insert(0, nodesToAddToQueue[i])
        print_queue(queue, queue[0])

    elif search == SearchEnum.BREADTH_FIRST_SEARCH:
        queue.extend(nodesToAddToQueue)
        print_queue(queue, queue[0])

    elif search == SearchEnum.DEPTH_LIMITED_SEARCH:
        depth_limit = 2
        to_remove = []
        for i in range(len(nodesToAddToQueue) -1, -1, -1):
            queue.insert(0, nodesToAddToQueue[i])
        print_queue(queue, queue[0])
        for i in range(len(queue)):
            curr_limit_node = len(queue[i][0])-1 
            if curr_limit_node >= depth_limit:
                to_remove.append(queue[i])     
        for elem in to_remove:
            if Terminal_State(elem) != 'G':
                queue.remove(elem)
            if len(queue) != 0:
                print_queue(queue, queue[0])

    elif search == SearchEnum.ITERATIVE_DEEPENING_SEARCH:
        depth_limit = depth_limit_iterative
        to_remove = []
        for i in range(len(nodesToAddToQueue) -1, -1, -1):
            queue.insert(0, nodesToAddToQueue[i])
        print_queue(queue, queue[0])
        for i in range(len(queue)):
            curr_limit_node = len(queue[i][0])-1 
            if curr_limit_node >= depth_limit:
                to_remove.append(queue[i])     
        for elem in to_remove:
            if Terminal_State(elem) != 'G': 
                queue.remove(elem)
            if len(queue) != 0:
                print_queue(queue, queue[0])

    elif search == SearchEnum.UNIFORM_COST_SEARCH:
        for node_from_opened in nodesToAddToQueue:
            pushed = False
            for j in range(len(queue)):
                fn_1 = node_from_opened[1][0]
                fn_2 = queue[j][1][0]

                if fn_1 != fn_2:
                    if fn_1 < fn_2:
                        queue.insert(j, node_from_opened)
                        pushed = True
                        break
                elif fn_1 == fn_2:
                    if node_from_opened[0][0].name != queue[j][0][0].name:
                        if node_from_opened[0][0].name < queue[j][0][0].name:
                            queue.insert(j, node_from_opened)
                            pushed = True
                            break
                    elif node_from_opened[0][0].name == queue[j][0][0].name:
                        if len(node_from_opened[0]) != len(queue[j][0]):
                            if len(node_from_opened[0]) < len(queue[j][0]):
                                queue.insert(j, node_from_opened)
                                pushed = True
                                break
                        elif len(node_from_opened[0]) == len(queue[j][0]):
                            for k in range(len(node_from_opened[0])):
                                if node_from_opened[0][k].name != queue[j][0][k]:
                                    if node_from_opened[0][k].name < queue[j][0][k]:
                                        queue.insert(j, node_from_opened)
                                        pushed = True
                                        break
            if not pushed:
                queue.append(node_from_opened)

        print_queue(queue, queue[0])

    elif search == SearchEnum.GREEDY_SEARCH:
        for node_from_opened in nodesToAddToQueue:
            pushed = False
            for j in range(len(queue)):
                fn_1 = node_from_opened[1][1]
                fn_2 = queue[j][1][1]

                if fn_1 != fn_2:
                    if fn_1 < fn_2:
                        queue.insert(j, node_from_opened)
                        pushed = True
                        break
                elif fn_1 == fn_2:
                    if node_from_opened[0][0].name != queue[j][0][0].name:
                        if node_from_opened[0][0].name < queue[j][0][0].name:
                            queue.insert(j, node_from_opened)
                            pushed = True
                            break
                    elif node_from_opened[0][0].name == queue[j][0][0].name:
                        if len(node_from_opened[0]) != len(queue[j][0]):
                            if len(node_from_opened[0]) < len(queue[j][0]):
                                queue.insert(j, node_from_opened)
                                pushed = True
                                break
                        elif len(node_from_opened[0]) == len(queue[j][0]):
                            for k in range(len(node_from_opened[0])):
                                if node_from_opened[0][k].name != queue[j][0][k]:
                                    if node_from_opened[0][k].name < queue[j][0][k]:
                                        queue.insert(j, node_from_opened)
                                        pushed = True
                                        break
            if not pushed:
                queue.append(node_from_opened)

        print_queue(queue, queue[0])

    elif search == SearchEnum.A_STAR:
        for node_from_opened in nodesToAddToQueue:
            pushed = False
            for j in range(len(queue)):
                fn_1 = node_from_opened[1][0] + node_from_opened[1][1]
                fn_2 = queue[j][1][0] + queue[j][1][1]

                if fn_1 != fn_2:
                    if fn_1 < fn_2:
                        queue.insert(j, node_from_opened)
                        pushed = True
                        break
                elif fn_1 == fn_2:
                    if node_from_opened[0][0].name != queue[j][0][0].name:
                        if node_from_opened[0][0].name < queue[j][0][0].name:
                            queue.insert(j, node_from_opened)
                            pushed = True
                            break
                    elif node_from_opened[0][0].name == queue[j][0][0].name:
                        if len(node_from_opened[0]) != len(queue[j][0]):
                            if len(node_from_opened[0]) < len(queue[j][0]):
                                queue.insert(j, node_from_opened)
                                pushed = True
                                break
                        elif len(node_from_opened[0]) == len(queue[j][0]):
                            for k in range(len(node_from_opened[0])):
                                if node_from_opened[0][k].name != queue[j][0][k]:
                                    if node_from_opened[0][k].name < queue[j][0][k]:
                                        queue.insert(j, node_from_opened)
                                        pushed = True
                                        break
            if not pushed:
                queue.append(node_from_opened)

        print_queue(queue, queue[0])

    elif search == SearchEnum.HILL_CLIMBING:
        min = float('inf')
        min_el = ()
        for node in nodesToAddToQueue:
            if node[1][1] < min:
                min = node[1][1]
                min_el = node
        if len(min_el) != 0:
            queue.append(min_el)
        print_queue(queue, queue[0])

    elif search == SearchEnum.BEAM_SEARCH:
        beam_w = 2
        queue.extend(nodesToAddToQueue)
        to_check = []
        to_remove = []
        min = float('inf')
        min_el = ()
        for elem in queue:
            if len(elem[0]) < min:
                min = len(elem[0])
                min_el = elem
        curr_limit = len(min_el[0])
        for elem in queue:
            if len(elem[0]) == curr_limit:
                to_check.append(elem)
        if len(to_check) > beam_w:
            no_el_to_remove = len(to_check) - beam_w
            #sort
            for i in range(len(to_check)):
                for j in range(len(to_check)-i-1):
                    if to_check[j][1][1] > to_check[j+1][1][1]:
                        temp = to_check[j]
                        to_check[j] = to_check[j+1]
                        to_check[j+1] = temp
            for i in range(no_el_to_remove):
                to_remove.append(to_check.pop(-1))
        for elem in to_remove:
            queue.remove(elem)
        print_queue(queue, queue[0])

    return queue

def Make_Queue_Node(state):
    path = []
    fn_info = [0, state.heuristic]
    path.append(state)
    result = (path, fn_info)
    return result

def Make_Queue(path):
    result = []
    result.append(path)
    return result

def Remove_Front(queue):
    result = queue.pop(0)
    return result

# node in Expand has the format ( [path] ,f_n )
def Expand(problem, node):
    opened_nodes = []
    curr_state = node[0][0]
     
    for child in curr_state.edges:
        temp_path = []
        fn_info = []
        cost = node[1][0] + curr_state.edges[child]
        heur = problem.getState(child).heuristic
        fn_info.append(cost)
        fn_info.append(heur)
        for i in range(len(node[0])):
            temp_path.append(node[0][i])
        if problem.getState(child) not in node[0]:
            temp_path.insert(0, problem.getState(child))
            opened_nodes.append((temp_path, fn_info))
            

    return opened_nodes

def Terminal_State(node):
    return node[0][0].name   


def main(filename):
    """
    Entry point for this program. Parses the input and then runs each search on the parsed graph.

    Parameters
    ----------
    filename : str
        The name of the file with graph input to search
    """ 
    graph = readInput(filename)
    for search in SearchEnum:
        print(search.value)
        node = General_Search(graph, search)
        if (node):
            print("      goal reached!")
            # Print solution path here
            print("      solution found: ", end="")
            for i in range(len(node[0])-1, -1, -1):
                print(node[0][i].name, end= "")
                if i != 0:
                    print(" - ",end= "")
            print()
        elif(not node):
            print("failure to find path between S and G")
            pass
        print()

def readInput(filename):
    """
    Build the graph from the given input file.

    Parameters
    ----------
    filename : str
        The name of the file with input to parse into a graph.
    """

    parsedGraph = Graph.Graph()
    isHeuristicSection = False # True if processing the heuristic values for the graph. False otherwise.
    sectionDivider = "#####"
    minCharsInLine = 3 # Each line with data must have at least 3 characters
    with open(filename, 'r') as input:
        for line in input.readlines():
            if (len(line) > minCharsInLine):
                line = line.strip()
                if(sectionDivider in line):
                    isHeuristicSection = True
                elif(isHeuristicSection):
                    state, heurStr = line.split(' ')
                    heuristic = float(heurStr)
                    parsedGraph.setHeuristic(state, heuristic)
                else:
                    state1, state2, costStr = line.split(' ')
                    cost = float(costStr)
                    parsedGraph.addStatesAndEdge(state1,state2, cost)
    for state_key in parsedGraph.states:
        state = parsedGraph.states[state_key]
        state.edges = OrderedDict(sorted(state.edges.items()))
    return parsedGraph   
if __name__ == "__main__": 
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Must input the filename with the graph input to search.")

