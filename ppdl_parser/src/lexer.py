import re
from enum import Enum, auto

class TokenCode(Enum):
    TOKEN_EMPTY = auto()
    TOKEN_ERROR = auto()
    TOKEN_IDENTIFIER = auto()
    TOKEN_VAR_IDENTIFIER = auto()
    TOKEN_NUMBER = auto()
    TOKEN_EOF = auto()
    TOKEN_COMMENTS = auto()
    TOKEN_UNKNOWN = auto()

    TOKEN_LPARENTHESIS = auto() 
    TOKEN_RPARENTHESIS = auto()
    TOKEN_COLON = auto()

    TOKEN_DEFINE = auto()
    TOKEN_DOMAIN = auto()
    TOKEN_REQUIREMENTS = auto()
    TOKEN_TYPES = auto()
    TOKEN_CONSTANTS = auto()
    TOKEN_PREDICATES = auto()
    TOKEN_FUNCTIONS = auto()
    TOKEN_CONSTRAINTS = auto()
    TOKEN_ACTION = auto()
    TOKEN_PARAMETERS = auto()
    TOKEN_PRECONDITION = auto()
    TOKEN_EFFECT = auto()
    TOKEN_DURATIVE_ACTION = auto()
    TOKEN_DURATION = auto()
    TOKEN_CONDITION = auto()
    TOKEN_DERIVED = auto()
    TOKEN_PROBLEM = auto()
    TOKEN_OBJECTS = auto()
    TOKEN_INIT = auto()
    TOKEN_GOAL = auto()
    TOKEN_METRIC = auto()
    TOKEN_TOTAL_TIME = auto()
    TOKEN_LENGTH = auto()
    TOKEN_SERIAL = auto()
    TOKEN_PARALLEL = auto()

    # Operadores Lógicos (do primeiro código)
    TOKEN_AND = auto()
    TOKEN_OR = auto()
    TOKEN_NOT = auto()
    TOKEN_IMPLY = auto() # imply

    # Operadores Aritméticos e de Comparação (do primeiro código)
    TOKEN_PLUS = auto()      # +
    TOKEN_MINUS = auto()     # -
    TOKEN_MULTIPLY = auto()  # *
    TOKEN_DIVIDE = auto()    # /
    TOKEN_LESS = auto()      # <
    TOKEN_GREATER = auto()   # >
    TOKEN_EQUAL = auto()     # = (já tinha, mas reforça)
    TOKEN_LESS_EQUAL = auto()# <=
    TOKEN_GREATER_EQUAL = auto()# >=

    # Quantifiers (do primeiro código)
    TOKEN_FORALL = auto()
    TOKEN_EXISTS = auto()

    # Operadores Condicionais (do primeiro código)
    TOKEN_WHEN = auto() # when

    # Operadores Modificadores (do primeiro código)
    TOKEN_ASSIGN = auto()
    TOKEN_SCALE_UP = auto()
    TOKEN_SCALE_DOWN = auto()
    TOKEN_INCREASE = auto()
    TOKEN_DECREASE = auto()

    # Operadores Temporais (do primeiro código)
    TOKEN_AT = auto()
    TOKEN_OVER = auto()
    TOKEN_START = auto()
    TOKEN_END = auto()

    # Operadores de Otimização (do primeiro código)
    TOKEN_MINIMIZE = auto()
    TOKEN_MAXIMIZE = auto()


class Token:
    def __init__(self, content: str, code: TokenCode, line_num: int):
        self.content = content
        self.code = code
        self.line_num = line_num

# Listas de palavras-chave e operadores para ajudar o lexer a classificar
# Mapeamos a string para o TokenCode correspondente para facilitar a busca
KEYWORDS_MAP = {
    'define': TokenCode.TOKEN_DEFINE, 'domain': TokenCode.TOKEN_DOMAIN,
    'requirements': TokenCode.TOKEN_REQUIREMENTS, 'types': TokenCode.TOKEN_TYPES,
    'constants': TokenCode.TOKEN_CONSTANTS, 'predicates': TokenCode.TOKEN_PREDICATES,
    'functions': TokenCode.TOKEN_FUNCTIONS, 'constraints': TokenCode.TOKEN_CONSTRAINTS,
    'action': TokenCode.TOKEN_ACTION, 'parameters': TokenCode.TOKEN_PARAMETERS,
    'precondition': TokenCode.TOKEN_PRECONDITION, 'effect': TokenCode.TOKEN_EFFECT,
    'durative-action': TokenCode.TOKEN_DURATIVE_ACTION, 'duration': TokenCode.TOKEN_DURATION,
    'condition': TokenCode.TOKEN_CONDITION, 'derived': TokenCode.TOKEN_DERIVED,
    'problem': TokenCode.TOKEN_PROBLEM, 'objects': TokenCode.TOKEN_OBJECTS,
    'init': TokenCode.TOKEN_INIT, 'goal': TokenCode.TOKEN_GOAL,
    'metric': TokenCode.TOKEN_METRIC, 'total-time': TokenCode.TOKEN_TOTAL_TIME,
    'length': TokenCode.TOKEN_LENGTH, 'serial': TokenCode.TOKEN_SERIAL,
    'parallel': TokenCode.TOKEN_PARALLEL,
    'and': TokenCode.TOKEN_AND, 'or': TokenCode.TOKEN_OR, 'not': TokenCode.TOKEN_NOT, 'imply': TokenCode.TOKEN_IMPLY,
    'forall': TokenCode.TOKEN_FORALL, 'exists': TokenCode.TOKEN_EXISTS,
    'when': TokenCode.TOKEN_WHEN,
    'assign': TokenCode.TOKEN_ASSIGN, 'scale-up': TokenCode.TOKEN_SCALE_UP, 'scale-down': TokenCode.TOKEN_SCALE_DOWN,
    'increase': TokenCode.TOKEN_INCREASE, 'decrease': TokenCode.TOKEN_DECREASE,
    'at': TokenCode.TOKEN_AT, 'over': TokenCode.TOKEN_OVER, 'start': TokenCode.TOKEN_START, 'end': TokenCode.TOKEN_END,
    'minimize': TokenCode.TOKEN_MINIMIZE, 'maximize': TokenCode.TOKEN_MAXIMIZE
}

# Operadores de múltiplos caracteres (ordem importa: verificar os mais longos primeiro)
MULTI_CHAR_OPERATORS = {
    '>=': TokenCode.TOKEN_GREATER_EQUAL,
    '<=': TokenCode.TOKEN_LESS_EQUAL,
}

# Operadores de um único caractere
SINGLE_CHAR_OPERATORS = {
    '+': TokenCode.TOKEN_PLUS,
    '-': TokenCode.TOKEN_MINUS,
    '*': TokenCode.TOKEN_MULTIPLY,
    '/': TokenCode.TOKEN_DIVIDE,
    '<': TokenCode.TOKEN_LESS,
    '>': TokenCode.TOKEN_GREATER,
    '=': TokenCode.TOKEN_EQUAL,
}

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.current_line = 1

    def peek(self, offset=0) -> str:
        if self.position + offset < len(self.source_code):
            return self.source_code[self.position + offset]
        return ''

    def get_next_token(self) -> Token:
        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]

            # 1. Ignorar espaços em branco
            if current_char.isspace():
                if current_char == '\n':
                    self.current_line += 1
                self.position += 1
                continue # Volta para o inicio do loop para verificar o proximo caractere

            # 2. Ignorar Comentários (começam com ';')
            if current_char == ';':
                # Consome o restante da linha ate encontrar uma nova linha ou o fim do arquivo
                while self.position < len(self.source_code) and self.source_code[self.position] != '\n':
                    self.position += 1
                # Se o comentario nao termina em EOF, e sim em nova linha, avanca para a proxima linha
                if self.position < len(self.source_code) and self.source_code[self.position] == '\n':
                    self.current_line += 1
                    self.position += 1
                continue # Volta para o inicio do loop para verificar o proximo caractere
            
            # Se nao eh espaco em branco nem comentario, entao eh o inicio de um token significativo
            break 
        
        # Se chegamos ate aqui e a posicao esta no final do codigo, significa EOF
        if self.position >= len(self.source_code):
            return Token("#EOF", TokenCode.TOKEN_EOF, self.current_line)

        # Agora, o 'current_char' e 'start_pos' devem ser definidos novamente
        # apos o loop, pois a posicao pode ter avancado.
        start_pos = self.position
        current_char = self.source_code[self.position]

        # 3. Delimitadores de um único caractere
        if current_char == '(':
            self.position += 1
            return Token("(", TokenCode.TOKEN_LPARENTHESIS, self.current_line)
        if current_char == ')':
            self.position += 1
            return Token(")", TokenCode.TOKEN_RPARENTHESIS, self.current_line)
        if current_char == ':': # Adicionado do primeiro código
            self.position += 1
            return Token(":", TokenCode.TOKEN_COLON, self.current_line)

        # 4. Comentários (do primeiro código)
        if current_char == ';':
            while self.position < len(self.source_code) and self.source_code[self.position] != '\n':
                self.position += 1
            comment_content = self.source_code[start_pos:self.position]
            # Poderíamos retornar TOKEN_COMMENTS ou simplesmente ignorá-los
            # Por enquanto, vamos retornar para fins de demonstração, mas parsers geralmente os ignoram
            return Token(comment_content, TokenCode.TOKEN_COMMENTS, self.current_line)

        # 5. Operadores (combinação da lógica do primeiro e segundo)
        # Tentar operadores de múltiplos caracteres primeiro
        for op_str, op_code in MULTI_CHAR_OPERATORS.items():
            if self.source_code.startswith(op_str, self.position):
                self.position += len(op_str)
                return Token(op_str, op_code, self.current_line)
        
        # Tentar operadores de um único caractere
        if current_char in SINGLE_CHAR_OPERATORS:
            self.position += 1
            return Token(current_char, SINGLE_CHAR_OPERATORS[current_char], self.current_line)


        # 6. Números (melhoria da lógica do primeiro código para floats)
        if current_char.isdigit():
            number = ''
            while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                number += self.source_code[self.position]
                self.position += 1
            if self.position < len(self.source_code) and self.source_code[self.position] == '.':
                # Verifica se há dígitos após o ponto para ser um float válido
                if self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
                    number += self.source_code[self.position] # Adiciona o ponto
                    self.position += 1
                    while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                        number += self.source_code[self.position]
                        self.position += 1
                # else: caso seja um ponto solto ou seguido de não-dígito, será tratado como UNKNOWN depois ou na próxima iteração
            return Token(number, TokenCode.TOKEN_NUMBER, self.current_line)
        
        # 7. Identificadores e Palavras-Chave (melhoria da lógica do primeiro e segundo)
        # Inclui o '?' para variáveis PDDL
        if current_char.isalpha() or current_char == '?' or current_char == '-': # Identificadores podem começar com '-' em PDDL após a primeira letra
            atom = ""
            # Lógica para capturar o átomo completo (letras, números, hífens, underscores, '?' inicial)
            # A ordem aqui é importante. Primeiro, capturamos o token. Depois, decidimos o tipo.
            while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] in ['-', '_', '?']):
                atom += self.source_code[self.position]
                self.position += 1
            
            # Se o token começa com '?', é uma variável
            if atom.startswith('?'):
                # Podemos adicionar uma validação mais robusta de variável se necessário
                if re.fullmatch(r'^\?[a-zA-Z][\w-]*$', atom): # Do primeiro código
                    return Token(atom, TokenCode.TOKEN_VAR_IDENTIFIER, self.current_line)
                else:
                    return Token(atom, TokenCode.TOKEN_UNKNOWN, self.current_line)
            
            # Verificar se é uma palavra-chave
            if atom in KEYWORDS_MAP:
                return Token(atom, KEYWORDS_MAP[atom], self.current_line)
            
            # Se não for palavra-chave nem variável, é um identificador normal
            # Do primeiro código, regex para identificadores normais: r'^[a-zA-Z][\w-]*$'
            if re.fullmatch(r'^[a-zA-Z][\w-]*$', atom):
                return Token(atom, TokenCode.TOKEN_IDENTIFIER, self.current_line)
            
            # Se não se encaixa em nada, ainda pode ser um UNKNOWN
            return Token(atom, TokenCode.TOKEN_UNKNOWN, self.current_line)

        # 8. Caracteres desconhecidos
        self.position += 1
        return Token(current_char, TokenCode.TOKEN_UNKNOWN, self.current_line)