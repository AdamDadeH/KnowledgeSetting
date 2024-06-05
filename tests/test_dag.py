from unittest import TestCase

import core

from core.concept import Concept
from concept_store.local_concept_store import LocalConceptStore


class TestDictionaryStore(TestCase):
    dag = LocalConceptStore(
        {"cats_id": Concept(name="cats", content="Meow meow", content_type="animal")},
        {},
    )

    def test_get_content_by_name_if_found(self):
        dag = self.dag
        content_returned = dag.get_concept_or_default("cats_id")
        self.assertEqual(content_returned.get_title(), "cats")
        self.assertEqual(content_returned.get_content(), "Meow meow")

    def test_get_content_by_name_if_missing(self):
        dag = self.dag
        content_returned = dag.get_concept_or_default("dogs_id")
        self.assertEqual(content_returned.get_title(), "dogs_id")
        self.assertEqual(content_returned.get_content(), "")


class TestContentDag(TestCase):
    def test_disconnected_nodes(self):
        self.fail()

    def test_get_source_content(self):
        self.fail()

    def test_usage_count(self):
        self.fail()

    def test_get_minimum_requirements(self):
        self.fail()

    def test_subset_by_known_and_targets(self):
        self.fail()

    def test_subset_by_targets(self):
        self.fail()
