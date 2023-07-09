# Import necessary libraries
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# Import personalised modules
from vector_database import *
from utils import *
from manager import *

# Memory optimisation
from memory_profiler import profile

#===================================================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#===================================================================

# Initialize the FastAPI application
app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware setup to allow requests from the specified origins
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "https://primal-hybrid-391911.ew.r.appspot.com", #New for google cloud
    "http://localhost:8080",  # Allow your local frontend to access the server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates with the "templates" directory
templates = Jinja2Templates(directory="templates")

# Instantiate and initialize necessary components for the application
data_path = './data/'
graph_manager = GraphManager(data_path)


def load_diffusion_profiles(data_path):
    # Load diffusion profiles
    with np.load(f'{data_path}compressed_diffusion_profiles.npz') as data:
        drug_diffusion_profiles = data['arr1']
        indication_diffusion_profiles = data['arr2']
    return drug_diffusion_profiles, indication_diffusion_profiles

drug_diffusion_profiles, indication_diffusion_profiles = load_diffusion_profiles(data_path)


def load_dictionaries(data_path):
    map_drug_diffusion_labels_to_indices = load_data_dict(f'{data_path}map_drug_labels_to_indices')
    map_drug_diffusion_indices_to_labels = {v: k for k, v in map_drug_diffusion_labels_to_indices.items()}
    map_indication_diffusion_labels_to_indices = load_data_dict(f'{data_path}map_indication_labels_to_indices')
    map_indication_diffusion_indices_to_labels = {v: k for k, v in map_indication_diffusion_labels_to_indices.items()}
    
    return map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels

map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)


def create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices):
    drug_vector_db = MultiMetricDatabase(dimensions=drug_diffusion_profiles.shape[1], metrics=['manhattan'], n_trees=30)
    drug_vector_db.add_vectors(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)
    return drug_vector_db

drug_vector_db = create_drug_vector_database(drug_diffusion_profiles, map_drug_diffusion_labels_to_indices)

#====================================================================================================================
# Define core recommendation function
#====================================================================================================================

def get_drugs_for_disease(chosen_indication_label, distance_metric='manhattan'):
    
    # Translate indication name to index in indication diffusion profiles, to retrieve diffusion profile
    #chosen_indication_label = graph_manager.mapping_indication_name_to_label[chosen_indication_name]
    chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
    chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

    #====================================
    # Querying Vector Database to return drug candidates
    #====================================
    num_recommendations = 10

    query = chosen_indication_diffusion_profile

    drug_candidates_indices = drug_vector_db.nearest_neighbors(query, distance_metric, num_recommendations)

    drug_candidates_labels = [map_drug_diffusion_indices_to_labels[index] for index in drug_candidates_indices]
    #drug_candidates_names = [graph_manager.mapping_drug_label_to_name[i] for i in drug_candidates_labels]
    drug_candidates_names = [graph_manager.mapping_all_labels_to_names[label] for label in drug_candidates_labels]


    return drug_candidates_names # List


#===================================================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#===================================================================

# Define a Pydantic model for diseases, drugs, and GraphRequest
class Disease(BaseModel):
    value: str
    name: str

class Drug(BaseModel):
    value: str
    name: str

class DiseaseDrugCandidatesRequest(BaseModel):
    disease_label: str

class GraphRequest(BaseModel):
    disease_label: str
    drug_label: str
    k1: int
    k2: int

#====================================================================================================================
# Define application routes
#====================================================================================================================

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    """Serve the index.html page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/diseases", response_model= List[Disease])
async def get_diseases():
    """Return a list of diseases"""
    list_of_diseases = [
        {"value": graph_manager.mapping_indication_name_to_label[name], "name": name}
        for name in graph_manager.indication_names_sorted
    ]
    return list_of_diseases

@app.get("/drugs", response_model= List[Drug])
async def get_drugs():
    """Return a list of diseases"""
    list_of_drugs = [
        {"value": graph_manager.mapping_drug_name_to_label[name], "name": name}
        for name in graph_manager.drug_names_sorted if name in graph_manager.mapping_drug_name_to_label
    ]
    return list_of_drugs

@app.post("/drugs_for_disease", response_model= List[Drug])
async def get_drugs_for_selected_disease(disease_drug_candidates_request: DiseaseDrugCandidatesRequest):
    """Return a list of drugs based on the selected disease"""

    assert isinstance(disease_drug_candidates_request.disease_label, str)

    drug_candidates = get_drugs_for_disease(disease_drug_candidates_request.disease_label)
    list_of_drug_candidates = [
        {"value": graph_manager.mapping_drug_name_to_label[name], "name": name}
        for name in drug_candidates
    ]
    return list_of_drug_candidates


#============================================================================
# Visualise MOA network using vis.js
#============================================================================


def generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label, chosen_drug_label, num_drug_nodes, num_indication_nodes):

    chosen_indication_index = map_indication_diffusion_labels_to_indices[chosen_indication_label]
    chosen_indication_diffusion_profile = indication_diffusion_profiles[chosen_indication_index]

    chosen_drug_index = map_drug_diffusion_labels_to_indices[chosen_drug_label]
    chosen_drug_diffusion_profile = drug_diffusion_profiles[chosen_drug_index]

    # Find top_k_nodes from diffusion profile
    top_k_nodes_drug_subgraph = graph_manager.get_top_k_nodes(chosen_drug_diffusion_profile, num_drug_nodes)
    top_k_nodes_indication_subgraph = graph_manager.get_top_k_nodes(chosen_indication_diffusion_profile, num_indication_nodes)

    
    #chosen_MOA_diffusion_profile = chosen_indication_diffusion_profile + chosen_drug_diffusion_profile

    # Find top_k_nodes from diffusion profile
    #top_k_nodes_MOA_subgraph = graph_manager.get_top_k_nodes(chosen_MOA_diffusion_profile, num_nodes_subgraph)
    top_k_nodes_MOA_subgraph = top_k_nodes_drug_subgraph + top_k_nodes_indication_subgraph

    # Make subgraph
    MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.create_subgraph(top_k_nodes_MOA_subgraph)

    return MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes


def convert_networkx_to_vis_graph_data(graph, node_colors, node_shapes):
    # Create a list of nodes and edges
    nodes = [{"id": graph_manager.mapping_label_to_index[node_label], 
              "label": f'{graph_manager.mapping_all_labels_to_names[node_label]}',
              "color": node_colors[node_label],
              "shape": node_shapes[node_label]
             } 
             for node_label in graph.nodes]
    
    #edges = [{"from": graph_manager.mapping_label_to_index[edge[0]], "to": graph_manager.mapping_label_to_index[edge[1]]} for edge in graph.edges]

    edges = [{"from": graph_manager.mapping_label_to_index[edge[0]], 
              "to": graph_manager.mapping_label_to_index[edge[1]],
              "arrows": "to"} for edge in graph.edges]

    # Return the graph data
    return {"nodes": nodes, "edges": edges}

@app.post("/graph", response_class=JSONResponse)
async def get_graph_data(request: GraphRequest):
    # Extract parameters from request
    disease_label = request.disease_label
    drug_label = request.drug_label
    k1 = request.k1
    k2 = request.k2

    print(f'disease_label: {disease_label}')
    print(f'drug_label: {drug_label}')
    print(f'k1: {k1}')
    print(f'k2: {k2}')

    # Generate MOA graph data
    MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = generate_MOA_nx_subgraph_adding_together_label(chosen_indication_label=disease_label, chosen_drug_label=drug_label, num_drug_nodes=k2, num_indication_nodes=k1)

    # Convert graph data into a format that vis.js can handle
    graph_data = convert_networkx_to_vis_graph_data(graph=MOA_subgraph, node_colors=MOA_subgraph_node_colors, node_shapes=MOA_subgraph_node_shapes)

    # Create the response
    response = {
        "MOA_network": graph_data,
    }

    return response


