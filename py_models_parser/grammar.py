from parsimonious.grammar import Grammar

grammar = Grammar(
    r"""
    expr = (class / if_else/ call_result / return / comments / attr_def / emptyline / funct_def)*
    return = "return" (id* ","*)*
    comments = r"\#" (text / list)
    if_else= ("if" (compare/ id / attr_def) ":")/("elif" (id/attr_def) ":")/("else" ":")
    compare = (call_result / id / args /args_in_brackets  ) operator (call_result/id/args_in_brackets/args)
    operator = "==" / "!=" / ">" / "<" / ">=" / "<="
    class = class_def attr_def* funct_def*
    class_def   = intend? class_name args? ":"* ws?
    attr_def  = intend? id type? ("=" (right_part))* ws?
    right_part =  (id args_in_brackets) / string / args  / call_result / args_in_brackets / id / text
    type = ":" ( (id args_in_brackets) / id)
    string = one_quote_str / double_quotes_str
    one_quote_str = ~"\'[^\']+\'"i
    double_quotes_str = ~'"[^\"]+"'i
    list = "[" (call_result / attr_def / args / id / text)* ","* "]"
    funct_def = intend? "def" id args? ":"* ws?
    args_in_brackets = "[" ((id/string)* ","* )* "]"
    args        = "(" (( list / call_result / args  / attr_def / id  )* ","* )* ")"
    call_result = id args ws?
    class_name  = "class" id
    id          = (((dot_id / text)+ ) *  / dot_id / text) ws?
    dot_id      = (text ".")*text
    intend      = "    " / "\t" / "\n"
    text        = !"class" ~r"['_A-Z 0-9{}_\"\-\/\$<%>\+\-\w*&^%$#!±~`§]*"i
    ws          = ~"\\s*"
    emptyline   = ws+
"""
)
