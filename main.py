from UserGeneration import UserGeneration as ug
from MappingLoader import *
from UserMatcher import *
from GraphManipulation import *
import pprint
from GenericMethods import * 


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(width=41, compact=True)
    amount_of_users = 75
    graph_data = GenericMethods.GetGraphsStructure(amount_of_users)
    users_dict = graph_data[1]
    personal_preference_mapping = MappingLoader.LoadPersonalPreferenceMapping()
    Full_Graph = GraphManipulation.GenerateFullDirectedGraph(personal_preference_mapping,users_dict)
    reduces_dimention_outcome = graph_data[0]
    reduced_dict = reduces_dimention_outcome[2]
    reduces_dimention_outcome_2 = GenericMethods.WriteMappingsToexcelAndReturnDfFromDict(reduces_dimention_outcome,"mapping_of_graph_structure.xlsx")
    Reduced_Graph = GraphManipulation.GenerateFullDirectedGraph(personal_preference_mapping,reduced_dict)
    Undirected_Reduced_Graph = GraphManipulation.GenerateFullUnDirectedGraph(personal_preference_mapping,reduced_dict)
    GraphManipulation.Plot3Graphs(Full_Graph,Reduced_Graph,Undirected_Reduced_Graph,"AllGrahpsForComparison.png")

    cliques = GraphManipulation.ReturnCliques(Undirected_Reduced_Graph)
    cliques_per_node = GraphManipulation.ReturnCliquesPerNode(Undirected_Reduced_Graph)
    #print(cliques)
    #print("Total Number of reduced Users: ", len(reduced_dict))
    print("Preliminary groups...")
    preliminary_group = GraphManipulation.PreliminaryGroupsCliqueSizeOne(Undirected_Reduced_Graph,cliques)
    #users_from_preliminary_groups = Group.GetUsersFromGroups(preliminary_group)
    optimized_groups = GraphManipulation.OptimizeGroups(preliminary_group,Undirected_Reduced_Graph,reduced_dict)






