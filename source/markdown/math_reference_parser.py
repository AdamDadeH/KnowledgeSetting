from lark import Lark

"""
Have not written the corresponding transformations for this.
"""
def get_math_reference_parser():
    """
    keywords: a-z, A-Z, ., and _
    reference: [[keyword]]
    :return:
    """

    grammar = """
    value: (reference|inline_parametric|TEXT|SAFETEXT|COMMA|math)+
    
    reference.4: "[[" KEYWORD "]]"
    KEYWORD: /[a-zA-Z._]+/

    inline_parametric.4: "[[" KEYWORD "(" argument ("," argument)* ")" "]]"

    TEXT.0: /(?:(?!\[\[|\]\ ]|\$).)+/
    SAFETEXT.3: /[^\[\],()$]+/
    argument.3: " "*(SAFETEXT|inline_parametric|reference)+
    math: "$" SAFETEXT "$"
    COMMA: ","

    %ignore /\\s+/
    """

    parser = Lark(
        grammar,
        start="value",
        parser="earley",
    )
    return parser
