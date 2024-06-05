from lark import Lark


def get_prefix_text_parser(content_reference_token = "«"):
    parser = Lark(f"""
    value: (TEXT|inline_parametric)+
    KEYWORD: /[a-z._]+/
    TEXT: /[^{content_reference_token}]+/
    SAFETEXT: /[^{content_reference_token},()]+/
    argument: (SAFETEXT|inline_parametric)+
    inline_parametric:  "{content_reference_token}"KEYWORD"()" | "«"KEYWORD"("argument(","" "*argument)*")"
    """,
    start="value",
    parser="earley")
    return parser
