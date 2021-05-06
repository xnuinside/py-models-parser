from parsimonious.grammar import Grammar

grammar = Grammar(
    r"""
    expr = (class / call_result / attr_def / emptyline)*
    class = class_def attr_def* ws?
    class_def   = intend? class_name args? ":"* ws?
    attr_def  = intend? id ("=" right_part)* ws?
    right_part = args / call_result / id / string / text
    string = one_quote_str / double_quotes_str
    one_quote_str = ~"\'[^\']+\'"
    double_quotes_str = ~'"[^\"]+"'
    args     = "(" (( call_result / args / attr_def / id )* ","* )* ")"
    call_result = id args ws?
    class_name  = "class" id
    id          = (((dot_id / text)+ ","*) *  / dot_id / text) ws?
    dot_id      = (text".")*text
    intend      = "    " / "\t"
    text        = !class ~"['\_A-Z 0-9\{\}\[\]_\"\-\/\$:<%>\w]*"i
    ws          = ~"\s*"
    emptyline   = ws+
"""
)
