from concept_store.concept_store import ConceptStore
from core.concept import Concept


class UnknownContentError(Exception):
    def __init__(self, message):
        self.message = message


class LocalConceptStore(ConceptStore):
    """
    Content Repo given by in memory dictionaries
    """

    def __init__(self, concept_dict=None, relation_dict=None):
        self.concept_dict = concept_dict
        self.relation_dict = relation_dict
        self.anonymous_concept_key = 0
        if self.concept_dict is None:
            self.concept_dict = {}
        if self.relation_dict is None:
            self.relation_dict = {}

    def add_concept(self, key, concept_data):
        """

        :param key:
        :param concept_data:
        :return:
        """
        self.concept_dict[key] = concept_data

    def add_anonymous_concept(self, concept_data):
        self.concept_dict[self.anonymous_concept_key] = concept_data
        self.anonymous_concept_key += 1
        return self.anonymous_concept_key

    def get_concept_or_default(self, key: str):
        """
        Access content by name.
        If not found - returns a default Content instance
        populated with just the `name`.

        :param key: Content key
        :type key: str
        :return: Content instance
        :rtype: Concept
        """
        return self.concept_dict.get(key, Concept.default_from_name(key))

    def get_concept(self, key: str):
        """

        :param key: Content key
        :type key: str
        :return:
        :rtype: Concept
        """
        if key in self.concept_dict:
            return self.concept_dict[key]
        else:
            raise UnknownContentError("Content named {} is not found".format(key))

    def concept_defined(self, key: str):
        if key in self.concept_dict:
            return True
        else:
            return False

    def update_concept(self, key: str, concept_data):
        print("Updating Concept data is not implemented")
        pass

    def add_relation(self, from_concept, to_concept, relation_type):
        """
        Currently only indexed by from_concept
        :param from_concept:
        :param to_concept:
        :param relation_type:
        :return:
        """
        if from_concept not in self.relation_dict:
            self.relation_dict[from_concept] = {}
        relations = self.relation_dict[from_concept]
        if relation_type not in relations:
            relations[relation_type] = set()
        relations[relation_type].add(to_concept)

    def get_relations(self, name: str):
        """

        :param name:
        :return:
        """
        if name in self.relation_dict:
            return self.relation_dict[name]
        else:
            return {}

    def get_all_keys(self):
        """

        :return:
        """
        return self.concept_dict.keys()

    def items(self):
        """

        :return:
        """
        return self.concept_dict.items()

    def get_all_dependencies(self):
        return {k: v.get("depends_on", []) for (k, v) in self.relation_dict.items()}

    # return {k: v.dependencies for (k, v) in self.content_dict.items()}
