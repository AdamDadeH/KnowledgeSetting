class ConceptStore:
    """
    Repository of information about content.
    """

    def add_concept(self, key: str, concept_data):
        """create_concept(concept_data): Adds a new concept to the graph."""
        pass

    def add_anonymous_concept(self, concept_data):
        pass

    def update_concept(self, key: str, updates):
        """Updates properties of an existing concept."""
        pass

    def delete_concept(self, key: str):
        """Removes concept and its relations"""
        pass

    def concept_defined(self, key: str):
        pass

    def get_concept(self, key: str):
        """
        Get content if it exists.
        :param key:
        :return:
        """
        pass

    def get_concept_or_default(self, key: str):
        """
        Prioritizing always returning something.
        This method should return a natural default in cases where there
        is no content associated to the key.

        :param key:
        :return:
        """
        pass

    def get_relations(self, concept_id, relationship_type):
        """Retrieves all concepts related to a given concept by a specified relationship type."""

    def add_relation(self, from_concept, to_concept, relationship_type):
        """Adds a relationship between two concepts."""
        pass

    def get_all_keys(self):
        """
        This could become an unsafe operation accessing WAY too much data.

        :return:
        """
        pass

    def get_all_dependencies(self):
        pass
