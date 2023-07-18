# Import necessary libraries
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# Import personalised modules
from database import *
from utils import *
from optimised_manager import *

# Memory optimisation
from memory_profiler import profile

#===================================================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#===================================================================


# Create Driver and Connect to database
uri= 'bolt://3.83.107.114:7687'
username= 'neo4j'
password= 'children-insulation-transmitters'

# Connect to neo4j sandbox
driver = connect_to_neo4j_sandbox(uri, username, password)

# Initialize the FastAPI application
app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware setup to allow requests from the specified origins
origins = [
    'http://localhost',
    'http://127.0.0.1:8000',
    'https://primal-hybrid-391911.ew.r.appspot.com', #New for google cloud
    'http://localhost:8080',  # Allow your local frontend to access the server

    uri, # add neo4j sandbox graph database uri
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

map_drug_diffusion_labels_to_indices, map_drug_diffusion_indices_to_labels, map_indication_diffusion_labels_to_indices, map_indication_diffusion_indices_to_labels = load_dictionaries(data_path)


#====================================================================================================================
# Define core recommendation function
#====================================================================================================================



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

    #drug_candidates = get_drugs_for_disease(disease_drug_candidates_request.disease_label)

    drug_candidates_names_list = graph_manager.get_drugs_for_disease_precomputed(chosen_indication_label= disease_drug_candidates_request.disease_label)
    list_of_drug_candidates = [
        {"value": name, "name": name}
        for name in drug_candidates_names_list
    ]
    return list_of_drug_candidates


#============================================================================
# Visualise MOA network using vis.js
#============================================================================

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


    try:

        # Start a new session
        session = driver.session()

        # Retrieve MOA graph data from neo4j sandbox
        MOA_subgraph, MOA_subgraph_node_colors, MOA_subgraph_node_shapes = graph_manager.generate_subgraph_with_database(chosen_indication_label= disease_label, 
                                                                                                       chosen_drug_label= drug_label, 
                                                                                                       num_drug_nodes= k2, 
                                                                                                       num_indication_nodes= k1, 
                                                                                                       map_drug_diffusion_labels_to_indices= map_drug_diffusion_labels_to_indices, 
                                                                                                       map_indication_diffusion_labels_to_indices= map_indication_diffusion_labels_to_indices, 
                                                                                                       session= session)
        # Close database session to free up resources
        session.close()

    except Exception as e:
        print(f"An error occurred: {e}") # should probably return this error and log it on console in main.js
    

    # Convert graph data into a format that vis.js can handle
    graph_data = graph_manager.convert_networkx_to_vis_graph_data(graph=MOA_subgraph, node_colors=MOA_subgraph_node_colors, node_shapes=MOA_subgraph_node_shapes)

    # Create the response
    response = {
        "MOA_network": graph_data,
    }

    return response


