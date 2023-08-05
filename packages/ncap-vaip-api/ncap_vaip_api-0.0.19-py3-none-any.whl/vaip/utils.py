import hashlib
import os
import uuid
import io

#TODO: Harden method, prettify method, return message in case nothing defined, allow help on class or object (method overloading)
def get_definition(concept):
#Return proper content on user asking about things they are creating/have created
    try:
        return concept.definition[0]
    except:
        return type(concept).definition[0]

#TODO: Harden method, prettify method, return message in case nothing defined, allow help on class or object (method overloading)
def get_example(concept):
    try:
        return concept.example[0]
    except:
        return type(concept).example[0]

def get_file_resource_path(file_name, root_dir=os.path.dirname(__file__), prefix="", stem_dir="data"):
    resource_dir = f"{root_dir}/{stem_dir}"
    fully_qualified_path = f"{prefix}{resource_dir}/{file_name}"
    return fully_qualified_path

def generate_node_id(seed: str = None):
    """Generates a globally unique uuid, typically used in creating a unique IRI for a node to be stored in the knowledge graph.
    """
    if seed is not None:
        md5 = hashlib.md5()
        md5.update(seed.encode('utf-8'))
        return str(uuid.UUID(hex=md5.hexdigest(), version=4))
    else:
        return str(uuid.uuid4())

def get_root_namespace():
    return "https://ncei.noaa.gov/vaip"

def get_pattern_namespace():
    return f"{get_root_namespace()}/pattern"

def get_storage_pattern_namespace():
    return f"{get_pattern_namespace()}/storage"

def get_aiu_pattern_namespace():
    return f"{get_storage_pattern_namespace()}/aiu"

def get_individual_aiu_pattern_namespace(pattern_id: str):
    return f"{get_aiu_pattern_namespace()}/{pattern_id}"

def get_dynamic_namespace(pattern):
    return pattern.namespace.ontology.get_namespace(f"{pattern.iri}/")

def get_ontology_file_string(onto_file: str ="vaip_core_model.owl"):
    return get_file_resource_path(onto_file, prefix="file://")

def set_labels(node, primary, supporting):
    node.prefLabel = primary
    if supporting is not None:
        node.altLabel.extend(supporting)
    
def load_core_shacl(shapes_file_name="vaip_core_shapes.shacl"):
    """
    Returns the core shacl file for vaip shapes into memory (currently just aiu pattern).
    """
    shapes_file_path = get_file_resource_path(shapes_file_name, stem_dir="data/shacl")
    if os.path.isfile(shapes_file_path):
        shapes_file = open(shapes_file_path, "r")
        shapes_string = shapes_file.read()
        shapes_file.close()
        return shapes_string
    else:
        return None

def serialize_ontology(ontology, serialization_format="rdfxml", return_as_string=True, qualified_save_path="serialized_graph.owl"):
    if return_as_string:
        graph_file = io.BytesIO()
    else:
        graph_file = get_file_resource_path(qualified_save_path)
    ontology.save(file = graph_file, format = serialization_format)
    if return_as_string:
        rdf_string = (graph_file.getvalue().decode("utf-8"))
        graph_file.close()
        return rdf_string
    return None

def visualize_pattern(pattern, classes=False, values=True, supporting_labels=False):
    """Produces a visualization of a specific pattern

    Args:
        pattern (InformationObject or InformationPackage, required) Specifies the resource to visualize, takes a triples graph and produces a visualization for printing.
        classes (bool, optional): Displays classes alongside the pattern instances. Defaults to False.
        values (bool, optional): Displays data values (hasBits edges and values) alongside the pattern. Defaults to True.
        supporting_labels (bool, optional): Displays all supporting label triples for all nodes in the pattern. If False, only the primary label is shown. Defaults to False.
    """
    from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
    import networkx as nx
    import matplotlib.pyplot as plt
    import kglab
    import pyvis.network as pvn

    rdf_text = pattern.serialize_rdf_text("ttl")
    kg = kglab.KnowledgeGraph()
    kg.load_rdf_text(rdf_text)

    # measure = kglab.Measure()
    # measure.measure_graph(kg)

    # print("edges: {}\n".format(measure.get_edge_count()))
    # print("nodes: {}\n".format(measure.get_node_count()))

    pyvis_graph = pvn.Network(notebook=True)

    pyvis_graph.add_node(0, label="foo", title="This is FOO", color="red", size=9)
    pyvis_graph.add_node(1, label="bar", title="That is BAR", color="blue", size=5)
    pyvis_graph.add_node(2, label="baz", title="Here is BAZ", color="green", size=3)

    pyvis_graph.add_edge(0, 1, label="xyzzy", color="gray")
    pyvis_graph.add_edge(0, 2, label="fubar", color="red")

    pyvis_graph.force_atlas_2based()
    pyvis_graph.show("tmp.fig02.html")

    VIS_STYLE = {
        "wtm": {
            "color": "orange",
            "size": 40,
        },
        "ind":{
            "color": "yellow",
            "size": 30,
        },
    }

    subgraph = kglab.SubgraphTensor(kg)
    pyvis_graph = subgraph.build_pyvis_graph(style=VIS_STYLE)
    pyvis_graph.force_atlas_2based()
    # pyvis_graph.show_buttons(filter_=['physics'])
    # pyvis_graph.set_options('"bgcolor": "#222222"')
    pyvis_graph.show("tmp.fig01.html")

    # pos = nx.spring_layout(nx_graph, iterations=200, scale=2)
    # edge_labels = nx.get_edge_attributes(nx_graph, 'r')
    # nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)
    # nx.draw(nx_graph, pos=pos)
    # plt.show()