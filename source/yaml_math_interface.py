from core.concept import Concept
from source.content_block_parser import ContentDictParser


class TheoremYamlParser(ContentDictParser):
    """ """

    def __init__(self, relation_names):
        super().__init__(relation_names=relation_names)

    def parse(self, key, data):
        """
        This sort of conflates the process of raising errors and the
        process of generating content. Should likely not be overriding
        the behavior of "name" or "definition" but instead collect errors
        / debug info in a separate place.
        """

        title = self.parse_title(data)
        inline_name = self.parse_instance_rep(data)
        deps = self.parse_relation(data, "depends_on")
        statement = data.get("statement", "missing")
        proof = data.get("proven_by", "missing")

        if "proof" in data and "statement" in data:
            return [
                (
                    key,
                    (
                        Concept(
                            content_type="Theorem",
                            name=title,
                            content=statement,
                            instance_rep=inline_name,
                            inline_content="missing",
                            errors=self.logger,
                        ),
                        {"depends_on": deps},
                    ),
                ),
                (
                    key + "_proof",
                    (
                        Concept(
                            content_type="Proof",
                            name=title,
                            content=proof,
                            instance_rep=inline_name,
                            inline_content="missing",
                            errors=self.logger,
                        ),
                        {"depends_on": deps + [key]},
                    ),
                ),
            ]
        else:
            return [
                (
                    key,
                    (
                        Concept(
                            content_type="Theorem",
                            name=title,
                            content=statement,
                            instance_rep=inline_name,
                            inline_content="missing",
                            errors=self.logger,
                        ),
                        {"depends_on": deps},
                    ),
                )
            ]


def yaml_to_math_content(key, yaml_entry):
    """

    :param yaml_entry:
    :return:
    """

    relation_names = [("depends_on", True), ("is_a", False)]

    if yaml_entry is None:
        return [(key, [Concept.default_from_name(key), {}])]

    if type(yaml_entry) != dict:
        print(yaml_entry)

    entry_type = yaml_entry.get("type", "unknown")
    if entry_type == "definition":
        return [(key, ContentDictParser(relation_names=relation_names).parse(yaml_entry))]
    if entry_type == "theorem":
        return TheoremYamlParser(relation_names=relation_names).parse(key, yaml_entry)
    return [(key, ContentDictParser(relation_names=relation_names).parse(yaml_entry))]
