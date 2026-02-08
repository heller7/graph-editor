from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from PIL import Image, ImageDraw, ImageFont
import math

app = Flask(__name__)
CORS(app)

graphs = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/graphs', methods=['GET'])
def get_graphs():
    return jsonify(list(graphs.keys()))

@app.route('/api/graphs/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    if graph_id not in graphs:
        return jsonify({'error': 'Graph not found'}), 404
    return jsonify(graphs[graph_id])

@app.route('/api/graphs/<graph_id>', methods=['POST'])
def save_graph(graph_id):
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
    graphs[graph_id] = data
    return jsonify({'message': 'Graph saved successfully'})

def render_graph_to_figure(graph_data):
    """Shared rendering logic for PNG and JPG export."""
    node_radius = graph_data.get('nodeRadius', 25)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 1000)
    ax.set_ylim(700, 0)  # Inverted to match canvas (y=0 at top)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw edges
    for edge in graph_data.get('edges', []):
        start_node = None
        end_node = None

        for node in graph_data.get('nodes', []):
            if node['id'] == edge['source']:
                start_node = node
            elif node['id'] == edge['target']:
                end_node = node

        if start_node and end_node:
            x1, y1 = start_node['x'], start_node['y']
            x2, y2 = end_node['x'], end_node['y']

            # Draw edge
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)

            # Draw arrow
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                ux = dx / length
                uy = dy / length
                arrow_x = x2 - 20 * ux
                arrow_y = y2 - 20 * uy
                ax.arrow(arrow_x, arrow_y, 10*ux, 10*uy,
                        head_width=8, head_length=10, fc='k', ec='k')

            # Draw edge label
            if edge.get('label'):
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.text(mid_x, mid_y, edge['label'], ha='center', va='center',
                       fontsize=10, color='#333',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))

    # Draw nodes
    for node in graph_data.get('nodes', []):
        x, y = node['x'], node['y']
        label = node.get('label', str(node['id']))

        # Draw circle
        circle = patches.Circle((x, y), node_radius, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(circle)

        # Add label
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')

    return fig

@app.route('/api/graphs/<graph_id>/export/png', methods=['POST'])
def export_png(graph_id):
    if graph_id not in graphs:
        return jsonify({'error': 'Graph not found'}), 404

    fig = render_graph_to_figure(graphs[graph_id])

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name=f'{graph_id}.png')

@app.route('/api/graphs/<graph_id>/export/jpg', methods=['POST'])
def export_jpg(graph_id):
    if graph_id not in graphs:
        return jsonify({'error': 'Graph not found'}), 404

    fig = render_graph_to_figure(graphs[graph_id])

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='jpeg', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/jpeg', as_attachment=True, download_name=f'{graph_id}.jpg')

@app.route('/api/graphs/<graph_id>/export/tikz', methods=['POST'])
def export_tikz(graph_id):
    if graph_id not in graphs:
        return jsonify({'error': 'Graph not found'}), 404

    graph_data = graphs[graph_id]

    tikz_code = "\\begin{tikzpicture}\n"

    # Add nodes
    for node in graph_data.get('nodes', []):
        x, y = node['x'] / 100, (700 - node['y']) / 100  # Convert to TikZ coordinates
        label = node.get('label', str(node['id']))
        tikz_code += f"    \\node[circle, draw, fill=blue!20, minimum size=1cm] ({node['id']}) at ({x:.2f}, {y:.2f}) {{{label}}};\n"

    # Add edges
    for edge in graph_data.get('edges', []):
        if edge.get('label'):
            tikz_code += f"    \\draw[->, thick] ({edge['source']}) -- node[midway, above] {{{edge['label']}}} ({edge['target']});\n"
        else:
            tikz_code += f"    \\draw[->, thick] ({edge['source']}) -- ({edge['target']});\n"

    tikz_code += "\\end{tikzpicture}"

    # Return as text file
    tikz_buffer = io.BytesIO()
    tikz_buffer.write(tikz_code.encode('utf-8'))
    tikz_buffer.seek(0)

    return send_file(tikz_buffer, mimetype='text/plain', as_attachment=True, download_name=f'{graph_id}.tex')

if __name__ == '__main__':
    app.run(debug=True)
