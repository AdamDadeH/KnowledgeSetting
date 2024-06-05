from core.concept import build_inline_method, Concept
from core.content_log import ContentLogData
from core.relation import Relations
from source.markdown.bracket_markdown_parser import get_bracket_parser
from source.inline_handler import DependencyCollector

class ContentDictParser(object):
    """
    Base parser from Dict.
    """
    name_field = "title"

    def __init__(self, 
                 content_field="content",
                 relation_names=None,
                 reference_parser=get_bracket_parser()):
        if relation_names is None:
            relation_names = []
        self.content_field = content_field
        self.logger = ContentLogData()
        self.relation_names = relation_names
        self.ref_parser = reference_parser

    def get_or_else_error(self, data, key, default):
        """
        Check extract `key` from `data` if missing return default and raise error.

        Heavily erring towards always generating transform.

        :param data: Dictionary of content parameters.
        :param key: key to access
        :param default: default value to use
        :return: value at `key` or `default`
        """
        if key not in data:
            self.logger.error("Missing `{}` field".format(key))
        value = data.get(key, default)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            self.logger.error("Empty `{}` field".format(key))
            return default
        return value

    def parse_title(self, data):
        title = data.get(self.name_field, None)
        if title is None:
            return "Missing"
        else:
            return title

    def parse_type(self, data):
        """Extract type of content."""
        return self.get_or_else_error(data, "type", "Unknown Type")

    def parse_relation(self, data, relation_field, required=False):
        """Extract dependencies"""
        if required:
            return set(self.get_or_else_error(data, relation_field, []))
        else:
            return data.get(relation_field, set())

    def parse_properties(self, data):
        key = "properties"
        properties = data.get(key, [])
        property_names = []
        property_defaults = []
        for prop in properties:
            ptype = type(prop)
            if ptype == str:
                property_names.append(prop)
                property_defaults.append(None)
            if ptype == dict:
                plist = list(prop.items())
                property_names.append(plist[0][0])
                property_defaults.append(plist[0][1])
        return property_names, property_defaults

    def parse_instance_rep(self, data, field_name="notation"):
        """Parse means to declare instance of content."""
        # argument_names, = data.get("properties", [])
        arguments, defaults = self.parse_properties(data)

        if field_name not in data:
            inline_name = self.parse_title(data).lower()
            return build_inline_method(inline_name, arguments, defaults)
        else:
            inline_name = data.get(field_name)
            return build_inline_method(inline_name, arguments, defaults)

    def parse_inline_content(self, data):
        """
        ∆ is defining a local scope - indicating to check passed parameters
        :param data:
        :return:
        """
        encoded = data.get("inline_content", "missing")
        argument_names, defaults = self.parse_properties(data)

        return build_inline_method(encoded, argument_names, defaults)

    def parse_content(self, data):
        """
        :param data:
        :return:
        """
        if self.content_field not in data:
            self.logger.warn("Missing `{}` field".format(self.content_field))
            return "missing"
        else:
            content = data.get(self.content_field)
            if content!=None:
                d = DependencyCollector(self.ref_parser)
                #print(f"Parsed Dependencies : {d.get_dependencies(content)}")
            if content is None or (type(content) == "string" and content.strip() == ""):
                self.logger.warn("`{}` is empty".format(self.content_field))
                return "missing"
            return content

    def parse(self, data):
        """

        :param data:
        :return:
        """
        content_type = self.get_or_else_error(data, "type", "Missing Type")
        title = self.parse_title(data)
        inline_name = self.parse_instance_rep(data)
        content = self.parse_content(data)
        inline_content = self.parse_inline_content(data)
        relation_dict = {
            relation_name: self.parse_relation(data, relation_name, is_required)
            for (relation_name, is_required) in self.relation_names
        }
        return (
            Concept(
                content_type=content_type,
                name=title,
                content=content,
                instance_rep=inline_name,
                inline_content=inline_content,
                errors=self.logger,
            ),
            Relations(relation_dict),
        )
