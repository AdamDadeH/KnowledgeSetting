from unittest import TestCase

from source.markdown.math_reference_parser import get_math_reference_parser
from lark import Token, Tree
from dataclasses import dataclass

@dataclass
class TestTriple:
    name: str
    content: str
    target: Tree


class TestBracketParser(TestCase):

    test_cases = [
        TestTriple(
            name="just_text",
            content="hi I am text",
            target= Tree(Token('RULE', 'value'), [Token('SAFETEXT', 'hi I am text')])
        ),
        TestTriple("reference", "I have a [[reference]]",
         [Token('SAFETEXT', 'I have a '),
          Tree('reference',
               [Token('KEYWORD', 'reference')])]),
        TestTriple("parametric reference",
         "this has a [[parametric(x,y)]] reference",
         [Token('SAFETEXT', 'this has a '),
          Tree('inline_parametric',
               [Token('KEYWORD', 'parametric'),
                Tree('argument',
                     [Token('SAFETEXT', 'x')]),
                Tree('argument',
                     [Token('SAFETEXT', 'y')])]),
          Token('SAFETEXT', ' reference')]),
        TestTriple("parametric reference with difference whitespace", "this has a [[parametric(x, y)]] reference", None),
        TestTriple ("parametric reference with reference inside", "this has a [[parametric(x, [[set]])]] wow", None),
        TestTriple ("commas", "one, two, three", None),
        TestTriple("commas and ref", "one, [[two]], three", None),
        TestTriple("math", "dog $a_b$ cat", None)

    ]

    parser = get_math_reference_parser()
    def test_all(self):
        for test_triple in self.test_cases:
            result = self.parser.parse(test_triple.content)
            print(f"{test_triple.target} : {result}")





