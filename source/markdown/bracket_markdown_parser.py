from lark import Lark


def get_bracket_parser():

    grammar = """
    value.1: (reference|inline_parametric|TEXT|SAFETEXT|COMMA)+
    TEXT: /(?:(?!\\[\\[|\\]\\]).)+/
    reference.4: "[[" KEYWORD "]]"
    SAFETEXT: /[^\[\],()]+/
    argument.4: " "*(SAFETEXT|inline_parametric|reference)+
    inline_parametric.4: "[[" KEYWORD "(" argument ("," argument)* ")" "]]"
    KEYWORD: /[a-zA-Z._]+/
    COMMA: ","
    """
    #    %ignore /\\s+/


    parser = Lark(
        grammar,
        start="value",
        parser="earley",
    )
    return parser
