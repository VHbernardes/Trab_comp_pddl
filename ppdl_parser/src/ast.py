import re

def tokenize(code):
    tokens = re.findall(r'\(|\)|[^\s()]+', code)
    return tokens

def parse_tokens(tokens):
    if not tokens:
        return []

    token = tokens.pop(0)
    
    if token == '(':
        subtree = []
        while tokens[0] != ')':
            subtree.append(parse_tokens(tokens))
        tokens.pop(0)
        return subtree
    else:
        return token

def parse_file_to_ast(path):
    with open(path, 'r') as f:
        content = f.read()
    tokens = tokenize(content)
    ast = []
    while tokens:
        ast.append(parse_tokens(tokens))
    return ast
