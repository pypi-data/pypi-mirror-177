#Using owlready2 to load the core ontology in-memory and then automatically generate Python classes for constructing RDF triples
from owlready2 import get_ontology, Thing, World # type: ignore  # pylint: disable=E0401
#Suggest looking at uuid to do uuid generation for graph IRIs.
from pyshacl import validate
from . import utils

def load_pattern_ontology(world=World(), ontology_root="https://ncei.noaa.gov/vaip/patterns/", ontology_stem=""):
    """
    Given an ontology root and an ontology stem, open a clean ontology in the specified world as the specified path.
    Do not enforce a join character for the two ontology strings, allow for use of # or / (or other) delimiters.
    ontology_path = f"{ontology_root}{ontology_stem}"
    pattern_ontology = world.get_ontology(ontology_path)
    return pattern_ontology
    """
    return world.get_ontology(f"{ontology_root}{ontology_stem}")

vaip_ontology = get_ontology(utils.get_ontology_file_string()).load()
aiu_ontology = load_pattern_ontology(vaip_ontology.world, utils.get_aiu_pattern_namespace())
skos = get_ontology("http://www.w3.org/2004/02/skos/core#").load() # skos:prefLabel is used for primary labeling of all nodes

###The following classes define most of the concepts in the vAIP along with methods that are relevant to each.###


### THE INFORMATION OBJECT SET ###



def create_aiu_pattern(primary_label, supporting_labels=None):
    aiu = ArchivalInformationUnit(utils.generate_node_id(), namespace=aiu_ontology.get_namespace(f'{utils.get_aiu_pattern_namespace()}/'))
    utils.set_labels(aiu, primary_label, supporting_labels)
    return aiu

class InformationObject(Thing):
    """InformationObject is the fundamental data structure of the vAIP Knowledge graph and is taken directly from the OAIS reference model and encoded in RDF in the knowledge graph.
    Users do not create InformationObjects directly, but use specialized subclasses (Content, StructureRepresentation, SemanticRepresentation, Description, Packaging, etc.). Creating an information object
    to user methods looks like choosing an appropriate sublcass of InformationObject and providing a primary label, optional supporting labels, deciding on the type of data being held (linked or valued), and
    adding 
        adding 
    adding 
    """
    namespace = vaip_ontology

    def as_rdflib_graph(self):
        graph = self.namespace.ontology.world.as_rdflib_graph()
        return graph

    def serialize_rdf_text(self, serialization_format="rdfxml", return_as_string=True, qualified_save_path=f'{utils.get_file_resource_path(f"serialized_graph.owl")}'):
        return utils.serialize_ontology(self.namespace.ontology, serialization_format=serialization_format, return_as_string=return_as_string, qualified_save_path=qualified_save_path)

    def set_linked_data(self, primary_label: str, link: str, supporting_labels=None):
        """Set linked data in this InformationObject.

        Args:
            primary_label (str): Name of the linked data
            link (str): URL of data
            supporting_labels (str, optional): Additional labels for the linked data. Defaults to None.

        Returns:
            DigitalObject: the linked data object
        """
        data = vaip_ontology.DigitalObject(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self), hasBits=[link])
        utils.set_labels(data, f"{primary_label} Link", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def set_valued_data(self, primary_label: str, value: str, supporting_labels=None):
        data = vaip_ontology.DigitalObject(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self), hasBits=[value])
        utils.set_labels(data, f"{primary_label} Value", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def add_structure_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.StructureRepresentation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        self.hasStructureRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_structure_representation(self, structure_representation):
        while structure_representation in self.hasStructureRepresentation:
            self.hasStructureRepresentation.remove(structure_representation)

    def add_semantic_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.SemanticRepresentation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        self.hasSemanticRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_semantic_representation(self, semantic_representation):
        while semantic_representation in self.hasSemanticRepresentation:
            self.hasSemanticRepresentation.remove(semantic_representation)

    def add_other_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.OtherRepresentation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        self.hasOtherRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_other_representation(self, other_representation):
        while other_representation in self.hasOtherRepresentation:
            self.hasOtherRepresentation.remove(other_representation)

### THE INFORMATION PACKAGE SET ###

class InformationPackage(Thing):
    """Base class that isn't used directly. It should be used through one of its subclasses. 
    InformationPackages represent patternable storage in the knowledge graph.
    All resources in the knowledge graph are representable as whole InformationPackages.
    """
    namespace = vaip_ontology

    def validate(self):
        """Intentionally left empty for implementation by inheriting classes
        """
        pass
    
    def as_rdflib_graph(self):
        graph = self.namespace.ontology.world.as_rdflib_graph()
        return graph
    
    def serialize_rdf_text(self, serialization_format="rdfxml", return_as_string=True, qualified_save_path=f'{utils.get_file_resource_path(f"serialized_graph.owl")}'):
        return utils.serialize_ontology(self.namespace.ontology, serialization_format=serialization_format, return_as_string=return_as_string, qualified_save_path=qualified_save_path)

    def add_description(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.UnitDescription(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.describedBy.append(node)
        node.derivedFromPackage.append(self)

        return node

    def add_content(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ContentInformationObject(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.hasContentInformation.append(node)

        return node

    def add_packaging(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.PackagingInformationObject(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.packagedBy.append(node)

        return node

    def add_fixity(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.FixityPreservation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasFixity.append(node)

        return node

    def add_access_rights(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.AccessRightsPreservation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasAccessRights.append(node)

        return node
    
    def add_context(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ContextPreservation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasContext.append(node)

        return node
    
    def add_provenance(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ProvenancePreservation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasProvenance.append(node)

        return node

    def add_reference(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ReferencePreservation(utils.generate_node_id(), namespace=utils.get_dynamic_namespace(self))
        utils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasReference.append(node)

        return node

class ArchivalInformationUnit(Thing):
    """Archive Information Units relate to patterning and recording of identity of any type of entity that might be stored in the knowledge graph.
    This includes things like users, roles, orders, granules, collection records, files, cruises, models, code packages, etc.
    ArchivalInformationUnits should be stored as the data object for AIU pattern metadata. Creating an AIU pattern means creating and persisting a new pattern metadata
    record that holds a new central AIU node of an information package. All information objects are related to information packages through relationship to the central node.
    The central node of the ArchivalInformationUnit is considered the IRI of the entire 'pattern' or thing and other things are logically stored in relationship to it.
    """
    namespace = vaip_ontology
    
    def validate(self):
        data_graph = self.serialize_rdf_text()
        onto_graph = utils.serialize_ontology(vaip_ontology)
        shacl_graph = utils.load_core_shacl()
        conforms, results_graph, results_text = validate(data_graph, ont_graph=onto_graph, shacl_graph=shacl_graph)
        return {
            "conforms": conforms,
            "results_graph": results_graph,
            "results_text": results_text
        }
