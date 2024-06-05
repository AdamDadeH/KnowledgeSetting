from io import StringIO
from unittest import TestCase

from concept_store.local_concept_store import LocalConceptStore
from concept_store.local_graph_store import NxConceptGraph
from source.yaml import YamlFile, YamlDoc
from source.yaml_math_interface import yaml_to_math_content


class TestYamlSource(TestCase):

    simple_yaml = """
cat:
  type: definition
  title: Cat
  content: Mammal that goes meow.
  depends_on:
    - mammal
"""

    def test_simple_parse(self):
        concept_store = LocalConceptStore()
        graph_store = NxConceptGraph()
        YamlFile(StringIO(self.simple_yaml)).load_to(concept_store, graph_store)

        concept = concept_store.get_concept("cat")
        self.assertEqual(concept.content, "Mammal that goes meow.")
        cat_relations = concept_store.get_relations("cat")
        cat_dependencies = cat_relations.get("depends_on", None)
        self.assertEqual(cat_dependencies, {"mammal"})

    multiple_blocks = """
cat:
  type: definition
  title: Cat
  content: Mammal that goes meow.
  depends_on:
    - mammal
---
cat:
  depends_on:
    - mammal
    - claws
---
cat:
  depends_on:
    - fluffy
    - claws
---
cat:
  is_a:
    - mammal
    """

    def test_multiple_blocks_parse(self):
        concept_store = LocalConceptStore()
        graph_store = NxConceptGraph()
        YamlFile(StringIO(self.multiple_blocks)).load_to(concept_store, graph_store)
        concept = concept_store.get_concept("cat")
        self.assertEqual(concept.content, "Mammal that goes meow.")
        cat_relations = concept_store.get_relations("cat")
        cat_dependencies = cat_relations.get("depends_on", None)
        self.assertEqual(cat_dependencies, {"mammal", "fluffy", "claws"})

    raw_text_blocks = """
cat:
  type: definition
  title: Cat
  content: Mammal that goes meow.
  depends_on:
    - mammal
---
I like cats meow meow
---
cat:
  depends_on:
    - fluffy
    - claws
    """

    def test_raw_test_blocks(self):
        concept_store = LocalConceptStore()
        graph_store = NxConceptGraph()
        YamlFile(StringIO(self.raw_text_blocks)).load_to(concept_store, graph_store)