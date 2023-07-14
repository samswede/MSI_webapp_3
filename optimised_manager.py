import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from memory_profiler import profile

import pickle
import gzip


class GraphManager:
    #@profile
    def __init__(self, data_path):

        """ Memory Inefficient Loading:
        #=====================
        # Load and transform data
        #=====================
        self.drug_to_protein, self.indication_to_protein, self.protein_to_protein, self.protein_to_bio, self.bio_to_bio = self.load_data(data_path)

        #=====================
        # Label Graph
        #=====================
        # Create the self.MSI graph
        self.MSI = self.create_MSI_graph()

        self.MSI_node_labels = np.array(self.MSI.nodes()).tolist()
        self.MSI_size_graph = len(self.MSI_node_labels)

        # Create node mappings and sort names
        self.create_node_dictionaries_and_sort_names()
        
        """

        """ Memory Efficient Loading
        """
        #self.load_MSI_graph()
        self.load_dicts()
        self.load_mapping_all_labels_to_names()
        self.load_node_types()

        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        # Build MSI Graph
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def save_mapping_all_labels_to_names(self):
        with gzip.open('mapping_all_labels_to_names.pkl.gz', 'wb') as f:
            pickle.dump(self.mapping_all_labels_to_names, f)
    #@profile
    def load_mapping_all_labels_to_names(self):
        with gzip.open('mapping_all_labels_to_names.pkl.gz', 'rb') as f:
            self.mapping_all_labels_to_names = pickle.load(f)
    
    def save_node_types(self):
        with gzip.open('node_types.pkl.gz', 'wb') as f:
            pickle.dump(self.node_types, f)
    #@profile
    def load_node_types(self):
        with gzip.open('node_types.pkl.gz', 'rb') as f:
            self.node_types = pickle.load(f)

    def save_dicts(self):
        dict_names = ["mapping_label_to_index", "mapping_index_to_label", "mapping_drug_label_to_name", 
                      "mapping_indication_label_to_name", "mapping_drug_name_to_label", "mapping_indication_name_to_label",
                      "drug_names_sorted", "indication_names_sorted"]

        for name in dict_names:
            with gzip.open(f'{name}.pkl.gz', 'wb') as f:
                pickle.dump(getattr(self, name), f)
    #@profile
    def load_dicts(self):
        dict_names = ["mapping_label_to_index", "mapping_index_to_label", "mapping_drug_label_to_name", 
                      "mapping_indication_label_to_name", "mapping_drug_name_to_label", "mapping_indication_name_to_label",
                      "drug_names_sorted", "indication_names_sorted"]

        for name in dict_names:
            with gzip.open(f'{name}.pkl.gz', 'rb') as f:
                setattr(self, name, pickle.load(f))

    def save_MSI_graph(self, file_name):
        nx.write_graphml(self.MSI, f"{file_name}.graphml")

    #@profile
    def load_MSI_graph(self):
        self.MSI = nx.read_graphml("MSI_graph.graphml")
        pass

    #@profile
    def load_data(self, data_path):
        drug_to_protein = pd.read_csv(data_path + '1_drug_to_protein.tsv', sep='\t')
        indication_to_protein = pd.read_csv(data_path + '2_indication_to_protein.tsv', sep='\t')
        protein_to_protein = pd.read_csv(data_path + '3_protein_to_protein.tsv', sep='\t')
        protein_to_bio = pd.read_csv(data_path + '4_protein_to_biological_function.tsv', sep='\t')
        bio_to_bio = pd.read_csv(data_path + '5_biological_function_to_biological_function.tsv', sep='\t')
        
        return drug_to_protein, indication_to_protein, protein_to_protein, protein_to_bio, bio_to_bio
    
    #@profile
    def create_MSI_graph(self):
        'The optimal weights for the multiscale interactome are '
        'wdrug = 3.21, wdisease = 3.54, wprotein = 4.40,'
        ' whigher-level biological function = 2.10, wlower-level biological function = 4.49, wbiological function = 6.58'
        'α = 0.860'
        'use the correlation distance to compare r(c) and r(d) (Fig. 2b, c).'
        
        
        MSI = nx.DiGraph()
        self.node_types = {}
        self.add_nodes_to_graph(self.drug_to_protein, 'drug', 'protein', 3.2, MSI)
        self.add_nodes_to_graph(self.indication_to_protein, 'indication', 'protein', 3.5, MSI)
        self.add_nodes_to_graph(self.protein_to_protein, 'protein', 'protein', 4.4, MSI)
        self.add_nodes_to_graph(self.protein_to_bio, 'protein', 'bio', 4.5, MSI)
        self.add_nodes_to_graph(self.bio_to_bio, 'bio', 'bio', 6.5, MSI)
        return MSI
    

    #@profile
    def add_nodes_to_graph(self, data_frame, node_type_1, node_type_2, weight, MSI):
        for node_1, node_2 in zip(data_frame['node_1'], data_frame['node_2']):
            MSI.add_edge(node_1, node_2, weight= weight)
            self.node_types[node_1] = node_type_1
            self.node_types[node_2] = node_type_2


        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        # Create Dictionaries and Mappings
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    #@profile
    def create_node_dictionaries_and_sort_names(self):
        mapping_label_to_name, mapping_name_to_label, self.mapping_label_to_index, self.mapping_index_to_label, names_sorted = self.create_node_dictionaries(self.drug_to_protein, self.indication_to_protein)

        # Unpack
        self.mapping_drug_label_to_name, self.mapping_indication_label_to_name = mapping_label_to_name 
        self.mapping_drug_name_to_label, self.mapping_indication_name_to_label = mapping_name_to_label
        self.drug_names_sorted, self.indication_names_sorted = names_sorted

    #@profile
    def create_node_dictionaries(self, drug_to_protein, indication_to_protein):
        # Get unique combinations of node_1 and node_1_name
        unique_drug_label_and_name = drug_to_protein[['node_1', 'node_1_name']].drop_duplicates()
        unique_indication_label_and_name = indication_to_protein[['node_1', 'node_1_name']].drop_duplicates()

        # Convert to dictionaries
        mapping_drug_label_to_name = unique_drug_label_and_name.set_index('node_1')['node_1_name'].to_dict()
        mapping_indication_label_to_name = unique_indication_label_and_name.set_index('node_1')['node_1_name'].to_dict()

        # Make flipped dictionaries
        mapping_drug_name_to_label = {v: k for k, v in mapping_drug_label_to_name.items()}
        mapping_indication_name_to_label = {v: k for k, v in mapping_indication_label_to_name.items()}

        # Create dictionary mapping old label to new labels
        mapping_label_to_index = {old_label:new_label for new_label, old_label in enumerate(self.MSI.nodes())}
        mapping_index_to_label = {v: k for k, v in mapping_label_to_index.items()}

        # Get all unique drug names sorted alphabetically
        drug_names_sorted = sorted(unique_drug_label_and_name.astype(str)['node_1_name'].unique())
        indication_names_sorted = sorted(unique_indication_label_and_name.astype(str)['node_1_name'].unique())

        mapping_label_to_name = [mapping_drug_label_to_name, mapping_indication_label_to_name]
        mapping_name_to_label = [mapping_drug_name_to_label, mapping_indication_name_to_label]
        
        names_sorted = [drug_names_sorted, indication_names_sorted]

        return mapping_label_to_name, mapping_name_to_label, mapping_label_to_index, mapping_index_to_label, names_sorted

    #@profile
    def create_label_to_name_dictionaries(self):
        combined_dict_all_labels_to_names = {}

        # Get unique combinations of node_1 and node_1_name
        unique_drug_label_and_name = self.drug_to_protein[['node_1', 'node_1_name']].drop_duplicates()
        unique_indication_label_and_name = self.indication_to_protein[['node_1', 'node_1_name']].drop_duplicates()
        unique_protein_label_and_name_1 = self.protein_to_protein[['node_1', 'node_1_name']].drop_duplicates()
        unique_protein_label_and_name_2 = self.protein_to_protein[['node_2', 'node_2_name']].drop_duplicates()
        unique_bio_label_and_name_1 = self.bio_to_bio[['node_1', 'node_1_name']].drop_duplicates()
        unique_bio_label_and_name_2 = self.bio_to_bio[['node_2', 'node_2_name']].drop_duplicates()

        # Convert to dictionaries
        mapping_drug_label_to_name = unique_drug_label_and_name.set_index('node_1')['node_1_name'].to_dict()
        mapping_indication_label_to_name = unique_indication_label_and_name.set_index('node_1')['node_1_name'].to_dict()
        mapping_protein_label_to_name_1 = unique_protein_label_and_name_1.set_index('node_1')['node_1_name'].to_dict()
        mapping_protein_label_to_name_2 = unique_protein_label_and_name_2.set_index('node_2')['node_2_name'].to_dict()
        mapping_bio_label_to_name_1 = unique_bio_label_and_name_1.set_index('node_1')['node_1_name'].to_dict()
        mapping_bio_label_to_name_2 = unique_bio_label_and_name_2.set_index('node_2')['node_2_name'].to_dict()

        # Combining dictionaries
        combined_dict_all_labels_to_names.update(mapping_drug_label_to_name)
        combined_dict_all_labels_to_names.update(mapping_indication_label_to_name)
        combined_dict_all_labels_to_names.update(mapping_protein_label_to_name_1)
        combined_dict_all_labels_to_names.update(mapping_protein_label_to_name_2)
        combined_dict_all_labels_to_names.update(mapping_bio_label_to_name_1)
        combined_dict_all_labels_to_names.update(mapping_bio_label_to_name_2)

        return combined_dict_all_labels_to_names


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