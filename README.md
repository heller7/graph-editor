# Graph Editor

A simple web-based graph editor for creating and visualizing graphs with nodes and edges. Export your graphs as PNG, JPG images or TikZ code for LaTeX documents.

## Features

- **Interactive Graph Creation**: Click to add nodes, drag to move them, and connect nodes with edges
- **Visual Editor**: Clean, modern interface with real-time graph visualization
- **Export Options**: 
  - PNG images for presentations and documents
  - JPG images for web use
  - TikZ code for LaTeX documents
- **Graph Management**: Save and load graphs with custom names
- **Responsive Design**: Works on desktop and mobile devices

## Demo

https://graph-editor.vercel.app/

## How it Works

This application uses Flask as the backend API with a modern HTML5 Canvas frontend for interactive graph editing. The backend handles graph storage and export functionality using matplotlib for image generation and custom TikZ code generation.

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
cd api
python index.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Adding Nodes**: Enter a label and click "Add Node", or click directly on the canvas
2. **Moving Nodes**: Click and drag nodes to reposition them
3. **Adding Edges**: Select source and target nodes from the dropdown menus, then click "Add Edge"
4. **Saving Graphs**: Enter a name and click "Save Graph" to store your work
5. **Exporting**: Choose from PNG, JPG, or TikZ export options

## API Endpoints

- `GET /` - Main application interface
- `GET /api/graphs` - List all saved graphs
- `GET /api/graphs/<id>` - Get a specific graph
- `POST /api/graphs/<id>` - Save a graph
- `POST /api/graphs/<id>/export/png` - Export as PNG
- `POST /api/graphs/<id>/export/jpg` - Export as JPG
- `POST /api/graphs/<id>/export/tikz` - Export as TikZ code

## Deployment

This application is configured for deployment on Vercel with serverless functions.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2Fgraph-editor)

## Technologies Used

- **Backend**: Flask, matplotlib, networkx
- **Frontend**: HTML5 Canvas, vanilla JavaScript, CSS3
- **Deployment**: Vercel serverless functions
