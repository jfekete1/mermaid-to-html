import re

def parse_mermaid_and_labels(mermaid):
    lines = mermaid.strip().split('\n')
    graph = {}
    labels = {}

    for line in lines:
        if '-->' in line:
            # Use regex to extract nodes and labels
            match = re.match(r'(\w+)(?:\(([^)]+)\))?\s*-->\s*(\w+)(?:\(([^)]+)\))?', line.strip())
            if match:
                parent, parent_label, child, child_label = match.groups()
                parent, child = parent.strip(), child.strip()
                if parent_label:
                    labels[parent] = parent_label.strip()
                if child_label:
                    labels[child] = child_label.strip()
                if parent not in graph:
                    graph[parent] = []
                graph[parent].append(child)
    
    return graph, labels

def build_html_list(graph, labels, root):
    html = '<ul class="nested">'
    for node in graph.get(root, []):
        label = labels.get(node, '')
        node_display = f"{node} ({label})" if label else node
        html += f'<li><span class="box">{node_display}</span>'
        if node in graph:
            html += build_html_list(graph, labels, node)
        html += '</li>'
    html += '</ul>'
    return html

def convert_mermaid_to_html(graph, labels):
    # Identify roots: nodes that are not children of any other node
    all_nodes = set(graph.keys()).union({child for children in graph.values() for child in children})
    children = {child for children in graph.values() for child in children}
    roots = all_nodes - children

    html = '<ul id="myUL">'
    for root in roots:
        label = labels.get(root, '')
        root_display = f"{root} ({label})" if label else root
        html += f'<li><span class="box">{root_display}</span>'
        html += build_html_list(graph, labels, root)
        html += '</li>'
    html += '</ul>'
    return html

# Example usage
mermaid = """
graph TD;
  A(root) --> B(child 1);
  B --> C(child 1 1);
  B --> D(child 1 2);
  D --> E(child 2 1);
  E --> F(child 3 1);
"""

# Parse the Mermaid graph and extract labels
graph, labels = parse_mermaid_and_labels(mermaid)

# Convert the parsed graph and labels to HTML
html_list = convert_mermaid_to_html(graph, labels)
print(html_list)
