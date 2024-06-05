from lark import Lark, Transformer
from lark.exceptions import UnexpectedEOF, UnexpectedCharacters
from concept_store.concept_store import ConceptStore
from source.markdown.bracket_markdown_parser import get_bracket_parser

"""
Push substitution involves a pair of nodes (n1, n2) with n2 depending on n1.
n1 says "hey I think you should just inline my definition and then not depend on me."
- it is push because n1 decides when to do this

* Requires modification of all content for n2
* Requires modification of dependencies for n2
* Requires modification of graph (if we are using a graph representation of content)
"""
#


class DependencyCollectorTransformer(Transformer):
    """
    Want to only collect the keywords
    """

    def TEXT(self, args):
        return ""

    def SAFETEXT(self, args):
        return ""

    def COMMA(self, args):
        return ""

    def keyword(self, args):
        """

        :param args:
        :return:
        """
        return args[0]

    def argument(self, args):
        """

        :param args:
        :return:
        """
        return [str(a) for a in args if len(str(a)) != 0]

    def value(self, args):
        """

        :param args:
        :return:
        """
        #return ""
        return [str(a) for a in args if len(str(a)) != 0]

    def inline_parametric(self, args):
        """

        :param args:
        :return:
        """
        return args[0]

class DependencyCollector:

    def __init__(self, parser):
        self.parser = parser

    def get_dependencies(self, text):
        if text=="":
            return []
        t = self.parser.parse(text)
        v = DependencyCollectorTransformer()
        return v.transform(t)

class InlineTransformer(Transformer):
    """
    Generates transform from parsed expression.

    Configuration depends on specification of whether to access long
    or short form of content.
    """

    def __init__(self,
                 content_repo: ConceptStore,
                 to_inline):
        self.content_repo = content_repo
        self.to_inline = to_inline

    def TEXT(self, args):
        """
        Text gets directly transformed to string.

        :param args:
        :return:
        """
        return args

    def SAFETEXT(self, args):
        """
        Text gets directly transformed to string.

        :param args:
        :return:
        """
        return args

    def KEYWORD(self, args):
        """

        :param args:
        :return:
        """
        return args

    def argument(self, args):
        """

        :param args:
        :return:
        """
        return "".join([str(a) for a in args])

    def value(self, args):
        """

        :param args:
        :return:
        """
        return "".join([str(a) for a in args])

    def reference(self, args):
        if args[0] in self.to_inline:
            to_inline = self.content_repo.get_concept(args[0])
            return to_inline.inline_content([])
        else:
            to_inline = self.content_repo.get_concept(args[0])
            return to_inline.inline_name([])


    def inline_parametric(self, args):
        """

        :param args:
        :return:
        """
        if args[0] in self.to_inline:
            to_inline = self.content_repo.get_concept(args[0])
            return to_inline.inline_content(args[1:])
        else:
            to_inline = self.content_repo.get_concept(args[0])
            return to_inline.inline_name(args[1:])


class SubstitutionHandler(object):
    """
    Should inline anything in defined list `to_substitute`

    Specifically the behavior is

    Break up the text into sequence of literal text and things to replace.
    And then given a list of things that should always be full inlined
      - leave literal text alone
      - if inlined -> replace with inlined content
      - if not to be inlined -> replace with inlined title
    """

    def __init__(self,
                 to_substitute,
                 all_data,
                 parser=get_bracket_parser()):
        self.to_sub = to_substitute
        self.all_data = all_data
        self.transformer = InlineTransformer(self.all_data, self.to_sub)
        self.parser = parser

    def substitute(self, content, fixed_point=False):
        """
        Brute force recursive substitution.
        :param content:
        :return:
        """
        while fixed_point is False:
            res = self.single_substitute(content)
            return self.substitute(res, res==content)
        else:
            return content


    def single_substitute(self, content):
        """
        Replaces content if noted as "to replace"
        :param content: Takes in content to be possibly modified.
        :return:
        """
        if content == "":
            return content

        try:
            t = self.parser.parse(content)
        except UnexpectedEOF:
            print("Error parsing : {}".format(content))
            raise
        except UnexpectedCharacters:
            print("Error parsing : {}".format(content))
            raise

        try:
            return self.transformer.transform(t)
        except:
            print("cats")
            raise
