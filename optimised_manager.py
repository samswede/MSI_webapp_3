import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from memory_profiler import profile

import pickle
import gzip


class GraphManager:
    #@profile
    def __init__(self):

        self.load_MSI_graph()
        self.load_dicts()
        self.load_mapping_all_labels_to_names()
        self.load_node_types()

    #@profile
    def load_MSI_graph(self):
        self.MSI = nx.read_graphml("MSI_graph.graphml")
        pass
    
    #@profile
    def load_mapping_all_labels_to_names(self):
        with gzip.open('mapping_all_labels_to_names.pkl.gz', 'rb') as f:
            self.mapping_all_labels_to_names = pickle.load(f)
    
    #@profile
    def load_node_types(self):
        with gzip.open('node_types.pkl.gz', 'rb') as f:
            self.node_types = pickle.load(f)

    #@profile
    def load_dicts(self):
        dict_names = ["mapping_label_to_index", "mapping_index_to_label", "mapping_drug_label_to_name", 
                      "mapping_indication_label_to_name", "mapping_drug_name_to_label", "mapping_indication_name_to_label",
                      "drug_names_sorted", "indication_names_sorted"]

        for name in dict_names:
            with gzip.open(f'{name}.pkl.gz', 'rb') as f:
                setattr(self, name, pickle.load(f))

        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        # Subgraph
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    #@profile
    def get_top_k_nodes(self, diffusion_profile, k):
        """
        Get the top k nodes from a diffusion profile.
        Input: 
        - diffusion_profile (numpy array): The diffusion values for each node in the graph.
        The array index corresponds to the node index in the graph.
        - k (int): The number of nodes to return.
        
        Output: 
        - list of str: The labels of the top k nodes.
        """
        # Check if inputs are valid
        #assert isinstance(diffusion_profile, np.ndarray), "diffusion_profile must be a numpy array"
        #assert isinstance(k, int), "k must be an integer"
        #assert k <= len(diffusion_profile), "k cannot be greater than the number of nodes in the graph"
        
        # Get the indices of the top k nodes
        top_k_indices = np.argsort(diffusion_profile)[-k:]
        
        #print(f'Top-K indices: {top_k_indices}')
        #for index in top_k_indices:
        #    print(f'Index: {index}, val: {diffusion_profile[index]}')

        # Convert indices to labels
        top_k_labels = [self.mapping_index_to_label[i] for i in top_k_indices]
        
        return top_k_labels

    #@profile
    def create_subgraph(self, top_k_node_labels):
        """
        Create a subgraph from the top k nodes and draw it.
        
        Input: 
        - top_k_node_labels (list of str): The labels of the nodes to include in the subgraph.

        Output:
        - nx.Graph: The subgraph containing only the top k nodes.
        - dict: A dictionary mapping node labels to colors.
        """
        # Check if input is valid
        assert isinstance(top_k_node_labels, list), "top_k_node_labels must be a list"
        #assert all(isinstance(node, (str, int)) for node in top_k_node_labels), "All elements in top_k_node_labels must be strings or integers"
    
        # Create a subgraph from the top k nodes
        subgraph = self.MSI.subgraph(top_k_node_labels)
        
        # Create a dictionary for node colors
        node_colors, node_shapes = self.get_node_colors_and_shapes(self, subgraph)

        return subgraph, node_colors, node_shapes
    
    def get_node_colors_and_shapes(self, subgraph):

        # Create a dictionary for node colors
        node_colors = {}
        node_shapes = {}
        for node in subgraph.nodes():
            if self.node_types[node] == 'protein':
                node_colors[node] = '#7F8C8D '  # dark grey color for proteins
                node_shapes[node] = 'ellipse'  # circle for proteins
            elif self.node_types[node] == 'bio':
                node_colors[node] = '#2ECC71'  # green, #2ECC71 color for biological functions
                node_shapes[node] = 'box'  # square for biological functions
            elif self.node_types[node] == 'drug':
                node_colors[node] = '#439AD9'  # blue, #03A9F4 color for drugs
                node_shapes[node] = 'triangle'  # triangle for drugs
            elif self.node_types[node] == 'indication':
                node_colors[node] = '#DD614A'  # red, #F44336, #DD614A color for indications
                node_shapes[node] = 'triangleDown'  # triangle for indications


        return node_colors, node_shapes