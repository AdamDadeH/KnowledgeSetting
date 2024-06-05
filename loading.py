from concept_store.local_concept_store import LocalConceptStore
from concept_store.local_graph_store import NxConceptGraph
from source.source import FileListSource
from source.yaml import YamlFile


def build_local_content_repo(input_files):
    """

    :param input_files:
    :return:
    """
    concept_store = LocalConceptStore()
    graph_store = NxConceptGraph()
    source = FileListSource(input_files, YamlFile)
    source.load_to(concept_store, graph_store)
    return concept_store, graph_store
