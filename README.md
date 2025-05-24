# 📡 Social-Media-Analytics-Network-and-Community-Detection-
Dynamic Social Network Evolution Visualizer: animate the step‑by‑step growth of a social graph with NetworkX &amp; Matplotlib, and explore its communities and key influencers in an interactive Dash Cytoscape dashboard.


> **Author:** Aditya Shirke
> 
> **Tags:** Network Analysis, Dash, NetworkX, Centrality Measures, Visualization, Community Detection

## 🧠 Overview

This project simulates the **evolution of a dynamic social network** using two powerful approaches:

1. **Matplotlib Animation** — Animates the network's construction over time.
2. **Dash Cytoscape Dashboard** — Offers an interactive, analytical view of the network as it evolves, with centrality metrics and community detection.

---

## 🔍 Features

### 🎞️ NetworkX + Matplotlib Animation

* Progressive edge addition over time.
* Spring layout with consistent positioning.
* Clear visual of how network structure builds up.

### 🧬 Interactive Dash Web App

* Timeline slider to explore each stage of the network's growth.
* Louvain community detection (visualized with node colors).
* Centrality metrics (Degree, Closeness, Betweenness, Eigenvector).
* Hover tooltips for node details.
* Dynamic markdown displays:

  * Top 3 influential nodes by each metric.
  * Full centrality table for all nodes.

---

## 🛠️ Tech Stack

* **Dash** & **Dash Cytoscape**
* **NetworkX**
* **Matplotlib**
* **Louvain Community Detection (`python-louvain`)**
* **Gunicorn** (for deployment readiness)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/adityashirke/social-network-evolution.git
cd social-network-evolution
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Dash App

```bash
python app1.py
```

Then visit: [http://127.0.0.1:8050](http://127.0.0.1:8050)

### 4️⃣ Run the Animation (optional)

```bash
python animate_network.py
```

> A Matplotlib window will pop up showing the evolving network step-by-step.

---

## 📁 Project Structure

```
├── app1.py                  # Dash app with interactive graph and metrics
├── animate_network.py       # NetworkX + Matplotlib animated evolution
├── requirements.txt         # Python dependencies
├── custom.css               # Optional CSS
├── network_evolution.gif
├── README.md                # Project description (this file)
```

---

## 🤝 Credits

Special thanks to:

* NetworkX developers
* Plotly Dash community
* Louvain algorithm contributors

---

## 📜 License

MIT License. Feel free to reuse with attribution.

---

> Built with ❤️ by **Aditya Shirke**

