import networkx as nx
import os
import random
from networkx.algorithms.connectivity import minimum_st_edge_cut

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)
        return graph, num_buses, size_bus, constraints

def weight_graph(graph):
    WGraph = nx.Graph()
    WGraph.add_nodes_from(graph.nodes)
    for edge in graph.edges:
        WGraph.add_edge(edge[0],edge[1],capacity=random.randint(1,101))
    return WGraph

def get_min_cuts(graph,rowdy_list):
    for rowdys in rowdy_list:
        i = random.randint(1,len(rowdys)-1)
        s = rowdys[random.randint(0,i-1)]
        t = rowdys[random.randint(i,len(rowdys)-1)]
        min_cut = nx.Graph()
        min_cut.add_nodes_from(graph.nodes)
        min_cut.add_edges_from(minimum_st_edge_cut(graph,s,t))
        
        graph.remove_edges_from(min_cut.edges)
    a = 0
    b = 0
    max_len = 0
    for kid in graph.nodes:
        kids = nx.node_connected_component(graph,kid)
        if len(kids) > max_len:
            max_len = len(kids)
        if len(kids) == 1:
            a = kids.pop()
        elif len(kids) < max_len:
            b = kids.pop()
    if a != 0: 
        graph.add_edge(a,b)
    return graph


def solve(graph, num_buses, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    graph = weight_graph(graph)
    graph = get_min_cuts(graph,constraints)
    Set_Sol = set()
    Sol = []
    bus = []
    for node in graph.nodes:
        if node in Set_Sol:
           continue
        Set_Sol.add(node)
        kids = nx.node_connected_component(graph,node)
        #print(kids)
        #if node != 0:
            #print(" : added " + node + "       \n")
        #print("\n")    
        bus += [node]
        if len(bus) == size_bus:
            Sol += [bus]
            bus = []
            #print(Set_Sol)
        for kid in kids:
            if kid in Set_Sol:
                #print(kid)
                #print(" Kid was already seen \n")
                continue
            bus += [kid]
        #    print(bus)
        #    if kid != 0:
                #print(" : added " + kid + "       \n")
            
            Set_Sol.add(kid)
            if len(bus) == size_bus:
                Sol += [bus]
         #       print("Bus:")
          #      print( bus)
           #     print("\n Solution")
            #    print(Sol)
             #   print("\n\n\n")
                bus = []
                 
    #Set_Sol.remove(0)
    #print(sorted(Set_Sol))
    Orphans = Set_Sol.copy()
    Partials = []
    Sol2 = Sol.copy()
    for bus in Sol:
        if len(bus) != size_bus:
            Partials += [bus]
            Sol2.remove(bus)
        for node in Set_Sol:
            if node in bus:
                Orphans.remove(node)
    n_bus = []
    for node in Orphans:
        #print(node)
        #print("\n")
        n_bus += [node]
        #print(n_bus)
        if len(n_bus) == size_bus:
            Sol2 += [n_bus]
            print("added new bus\n")
            if len(Sol) == num_buses - len(Partials):
                n_bus = Partials.pop(0)
                print("Partial list added\n")
            else:
                n_bus = []
    
    Str_Sol = ""
    for bus in Sol2:
        Str_Sol += str(bus) + "\n"
    
    return Str_Sol
        
def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["all_large","all_large","small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        if size != "all_large":
            continue
        temp = size
        for i in range(11,20):
            size = temp + "/" + str(i)
            category_path = path_to_inputs + "/" + size
            output_category_path = path_to_outputs + "/" + size
            category_dir = os.fsencode(category_path)
        
            if not os.path.isdir(output_category_path):
                os.mkdir(output_category_path)

            for input_folder in os.listdir(category_dir):
                input_name = os.fsdecode(input_folder)
                if input_name == ".DS_Store":
                    continue
            #print(input_name)
            
                graph, num_buses, size_bus, constraints = parse_input(category_path + "/") # + input_name)
                solution = solve(graph, num_buses, size_bus, constraints)
                output_file = open(output_category_path + "/" + ".out", "w")
                print(output_category_path + "/" + ".out")
            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file
                output_file.write(solution)

                output_file.close()
           
if __name__ == '__main__':
    main()


