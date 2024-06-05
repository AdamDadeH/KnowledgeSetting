import os
from abc import ABC, abstractmethod


class ConceptSource(ABC):
    """
    Abstract base class for content sources.

    Specific content source implementations
    should inherit from this class and implement the load_to method.

    """
    @abstractmethod
    def load_to(self, content_store, graph_store):
        pass


class DirectorySource(ConceptSource):
    """
    Load each item in a given directory.
    """
    def __init__(self, directory_path, source_constructor):
        self.directory_path = directory_path
        self.source_constructor = source_constructor
        self.sources = []

    def discover_sources(self):
        for filename in os.listdir(self.directory_path):
            filepath = os.path.join(self.directory_path, filename)
            if os.path.isfile(filepath):
                self.sources.append(self.source_constructor(filepath))

    def load_to(self, content_store, graph_store):
        for source in self.sources:
            source.load_to(content_store, graph_store)


class FileListSource(ConceptSource):
    def __init__(self, file_list, source_constructor):
        self.source_constructor = source_constructor
        self.sources = [source_constructor(file) for file in file_list]

    def load_to(self, content_store, graph_store):
        for source in self.sources:
            source.load_to(content_store, graph_store)


