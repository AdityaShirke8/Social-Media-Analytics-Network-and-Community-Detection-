# app.py
import dash
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output
import networkx as nx
import community as community_louvain
import matplotlib.colors as mcolors

# -------------------------------------------
# Expanded Network: Edge Sequence Definition
# -------------------------------------------
edge_sequence = [
    ("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "David"),
    ("Charlie", "Eve"), ("David", "Eve"), ("Eve", "Frank"),
    ("George", "Helen"), ("Helen", "Ivy"), ("George", "Ivy"),
    ("Alice", "George"), ("David", "Helen"), ("Frank", "Jack"),
    ("Jack", "Karen"), ("Karen", "Leo"), ("Leo", "Mona"),
    ("Mona", "Nate"), ("Nate", "Olivia"), ("Olivia", "Paul"),
    ("Paul", "Quincy"), ("Quincy", "Rachel"), ("Rachel", "Sam"),
    ("Sam", "Tina"), ("Tina", "Uma"), ("Uma", "Victor"),
    ("Victor", "Wendy"), ("Wendy", "Xander"), ("Xander", "Yara"),
    ("Yara", "Zane"), ("Zane", "Alice"), ("Frank", "George"),
    ("Karen", "Helen"), ("Mona", "Eve"), ("Nate", "David"),
    ("Olivia", "Charlie"), ("Paul", "Bob"), ("Quincy", "Charlie"),
    ("Rachel", "Eve"), ("Sam", "Frank"), ("Tina", "George"),
    ("Uma", "Helen"), ("Victor", "Ivy"), ("Wendy", "Jack"),
    ("Xander", "Karen"), ("Yara", "Leo"), ("Zane", "Mona")
]

# --------------------------------------------------
# Utility: Generate a Color List for Community Mapping
# --------------------------------------------------
def generate_community_colors(num_communities):
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_communities <= len(colors):
        return colors[:num_communities]
    else:
        extended_colors = colors * (num_communities // len(colors) + 1)
        return extended_colors[:num_communities]

# --------------------------------------------------
# Utility: Create Network Elements Up to a Given Step
# --------------------------------------------------
def create_network(step):
    G = nx.Graph()
    G.add_edges_from(edge_sequence[:step])
    if G.number_of_nodes() == 0:
        return [], []
    
    # Community detection using Louvain method
    partition = community_louvain.best_partition(G)

    # Calculate various centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # Map communities to colors
    communities = set(partition.values())
    community_colors = generate_community_colors(len(communities))
    community_color_map = dict(zip(communities, community_colors))
    
    # Create node elements with centrality info and community color styling
    nodes = [
        {
            'data': {
                'id': node,
                'label': node,
                'degree': f"{degree_centrality[node]:.2f}",
                'closeness': f"{closeness_centrality[node]:.2f}",
                'betweenness': f"{betweenness_centrality[node]:.2f}",
                'eigenvector': f"{eigenvector_centrality[node]:.2f}",
                'community': partition[node]
            },
            'style': {'background-color': community_color_map[partition[node]]}
        }
        for node in G.nodes()
    ]
    
    # Create edge elements
    edges = [{'data': {'source': u, 'target': v}} for u, v in G.edges()]
    return nodes, edges

# --------------------------------------------------
# Dash App Initialization
# --------------------------------------------------
app = dash.Dash(__name__)
app.title = "Enhanced Social Network Evolution Dashboard"
server = app.server  # necessary for deployment (e.g., Heroku)

# Set the initial network state to step=1
initial_nodes, initial_edges = create_network(1)

app.layout = html.Div([
    html.H2("Enhanced Social Network Metric Analysis Simulation"),
    
    # Slider to control network evolution by step
    dcc.Slider(
        id='time-slider',
        min=1,
        max=len(edge_sequence),
        value=1,
        marks={i: f'Step {i}' for i in range(1, len(edge_sequence)+1)},
        step=1,
        tooltip={"always_visible": True, "placement": "bottom"}
    ),
    html.Br(),
    
    # Cytoscape component to display the interactive network graph
    cyto.Cytoscape(
        id='network-graph',
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '600px'},
        elements=initial_nodes + initial_edges,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'width': '50px',
                    'height': '50px',
                    'font-size': '16px',
                    'text-valign': 'center',
                    'color': 'white',
                    'background-color': 'data(color)',  # Use data(color) if you set it in your node data
                    'text-outline-width': 3,
                    'text-outline-color': '#2a3b4c',
                    'border-width': 3,
                    'border-color': '#4CAF50',
                    'transition-property': 'background-color, border-color',
                    'transition-duration': '0.2s',
                }
            },
            {
                'selector': 'node:hover',
                'style': {
                    'background-color': '#F7A7A6',
                    'border-color': '#FF5722',
                    'cursor': 'pointer',
                    'z-index': 9999,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'line-color': '#888',
                    'width': 3,
                    'opacity': 0.8,
                }
            },
            {
                'selector': 'edge:hover',
                'style': {
                    'line-color': '#FF5722',
                    'width': 5,
                }
            }
        ]
    ),
    html.Br(),
    
    # Div to display node info on hover
    html.Div(id='node-info', style={'marginTop': '20px', 'fontSize': '16px'}),
    html.Br(),
    
    # Div to display top influential users based on centrality measures
    html.Div(id='influential-users', style={'marginTop': '20px', 'fontSize': '16px'}),
    html.Br(),
    
    # Div to display complete centrality measures table for all nodes
    html.Div(id='all-centrality', style={'marginTop': '20px', 'fontSize': '14px'})
])

# --------------------------------------------------
# Callback: Update Network Graph Elements on Slider Change
# --------------------------------------------------
@app.callback(
    Output('network-graph', 'elements'),
    Input('time-slider', 'value')
)
def update_network(step):
    nodes, edges = create_network(step)
    return nodes + edges

# --------------------------------------------------
# Callback: Display Node Details on Hover
# --------------------------------------------------
@app.callback(
    Output('node-info', 'children'),
    Input('network-graph', 'mouseoverNodeData')
)
def display_node_info(data):
    if data:
        return html.Div([
            html.H4(f"Node: {data['label']}"),
            html.P(f"Degree Centrality: {data['degree']}"),
            html.P(f"Closeness Centrality: {data['closeness']}"),
            html.P(f"Betweenness Centrality: {data['betweenness']}"),
            html.P(f"Eigenvector Centrality: {data['eigenvector']}"),
            html.P(f"Community: {data['community']}")
        ])
    return "Hover over a node to view its centrality measures and community."

# --------------------------------------------------
# Callback: Display Top Influential Users (Top 3) for Each Centrality Measure
# --------------------------------------------------
@app.callback(
    Output('influential-users', 'children'),
    Input('time-slider', 'value')
)
def update_influential_users(step):
    G = nx.Graph()
    G.add_edges_from(edge_sequence[:step])
    if G.number_of_nodes() == 0:
        return "No influential users to display."
    
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    
    # Get top 3 for each centrality measure
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:3]

    influencer_text = "### Influential Users\n\n"
    influencer_text += "**Degree Centrality:**\n"
    for node, score in top_degree:
        influencer_text += f"- {node}: {score:.2f}\n"
    
    influencer_text += "\n**Closeness Centrality:**\n"
    for node, score in top_closeness:
        influencer_text += f"- {node}: {score:.2f}\n"
    
    influencer_text += "\n**Betweenness Centrality:**\n"
    for node, score in top_betweenness:
        influencer_text += f"- {node}: {score:.2f}\n"
    
    influencer_text += "\n**Eigenvector Centrality:**\n"
    for node, score in top_eigenvector:
        influencer_text += f"- {node}: {score:.2f}\n"
        
    return dcc.Markdown(influencer_text)

# --------------------------------------------------
# Callback: Display Complete Centrality Measures Table for All Nodes
# --------------------------------------------------
@app.callback(
    Output('all-centrality', 'children'),
    Input('time-slider', 'value')
)
def update_all_centrality(step):
    G = nx.Graph()
    G.add_edges_from(edge_sequence[:step])
    if G.number_of_nodes() == 0:
        return "No nodes available."
    
    partition = community_louvain.best_partition(G)
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    
    header = "| Node | Degree | Closeness | Betweenness | Eigenvector | Community |\n"
    header += "| --- | --- | --- | --- | --- | --- |\n"
    rows = ""
    for node in G.nodes():
        rows += f"| {node} | {degree_centrality[node]:.2f} | {closeness_centrality[node]:.2f} | {betweenness_centrality[node]:.2f} | {eigenvector_centrality[node]:.2f} | {partition[node]} |\n"
    return dcc.Markdown(header + rows)

# --------------------------------------------------
# Run the App
# --------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
