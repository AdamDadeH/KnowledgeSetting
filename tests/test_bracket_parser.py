from unittest import TestCase

from source.markdown.bracket_markdown_parser import get_bracket_parser
from lark import Token, Tree


class TestBracketParser(TestCase):

    test_cases = [
        ("just_text",
         "hi I am text",
         Tree(Token('RULE', 'value'), [Token('SAFETEXT', 'hi I am text')])
        ),
        ("reference",
         "I have a [[reference]]",
         Tree(Token('RULE', 'value'),
              [Token('SAFETEXT', 'I have a '),
               Tree(
                   Token('RULE', 'reference'),
                    [Token('KEYWORD', 'reference')]
               )
               ]
            )
         ),
        ("parametric reference",
         "this has a [[parametric(x,y)]] ref with $math$",
         Tree(Token('RULE', 'value'), [
             Token('SAFETEXT', 'this has a '),
             Tree(Token('RULE', 'inline_parametric'), [
                 Token('KEYWORD', 'parametric'),
                 Tree(Token('RULE', 'argument'), [
                     Token('SAFETEXT', 'x')]),
                 Tree(Token('RULE', 'argument'), [
                     Token('SAFETEXT', 'y')])
             ]),
            Token('SAFETEXT', ' ref with $math$')])
         ),
        ("multiline",
         """Two sets $A,B$ are a separation of $Y$ $\iff$
         
    * $[[disjoint(A,B)]]$
    * $Y = A \cup B$""",
         None),
        ("parametric reference with difference whitespace", "this has a [[parametric(x, y)]] reference", None),
        ("parametric reference with reference inside", "this has a [[parametric(x, [[set]])]] wow", None),
        ("commas", "one, two, three", None),
        ("commas and ref", "one, [[two]], three", None)
    ]

    parser = get_bracket_parser()
    def test_all(self):
        for (name, input, output) in self.test_cases:
            result = self.parser.parse(input)
            print(f"Expect : {output}\n Actual: {result}")
            assert(result == output)





