import pyaml

from source.source import ConceptSource
from source.yaml_math_interface import yaml_to_math_content


class YamlFile(ConceptSource):
    def __init__(self, input_source):
        self.input_source = input_source

    def load_to(self, content_store, graph_store):
        if isinstance(self.input_source, str):
            with open(self.input_source, 'r') as file:
                data = list(pyaml.yaml.load_all(file, Loader=UniqueKeyLoader))
        else:
            data = list(pyaml.yaml.load_all(self.input_source, Loader=UniqueKeyLoader))

        for doc in data:
            YamlDoc(doc).load_to(content_store, graph_store)
            print(f"Loaded from {self.input_source}")


class UniqueKeyLoader(pyaml.yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            assert key not in mapping
            mapping.append(key)
        return super().construct_mapping(node, deep)


class YamlDoc(ConceptSource):

    def __init__(self, data, doc_parser=yaml_to_math_content):
        self.data = data
        self.parser = doc_parser

    def load_to(self, content_store, graph_store):
        """

        :param content_store:
        :param graph_store:
        :return:
        """
        if self.data is None:
            pass
        # Here we would need to check the doc type and parse correctly

        if type(self.data) is str:
            #print(f"Skip Loading - need to safely generate key : {self.data}")
            # increment should be automatic / guarentee uniqueness
            content_store.add_anonymous_concept({"content": self.data, "type": "text block"})


        if type(self.data) is dict:
            for (key, value) in self.data.items():
                try:
                    parsed = self.parser(key, value)
                except:
                    print(f"Error Parsing {key} : {value}")

                for (name, (content, relations)) in parsed:
                    # prefer to also join together multiple content types - so should also have a dictionary of content_type to content
                    # could break up content that is `summary`, `detailed`, `discussion`, and have a separate block for each.
                    if content_store.concept_defined(name):
                        content_store.update_concept(name, content)
                    else:
                        content_store.add_concept(name, content)
                    for (relation_type, target_list) in relations.items():
                        if relation_type=="depends_on":
                            for target in target_list:
                                graph_store.add_relation(name, target)
                        for target in target_list:
                            content_store.add_relation(name, target, relation_type)
