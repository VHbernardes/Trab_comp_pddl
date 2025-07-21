from .lexer import Token, TokenCode, Lexer # Importação do seu lexer aprimorado
import sys

class Parser:
    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.current_token = self.lexer.get_next_token()

    def check_token(self, expected_token_code: TokenCode):
        # Este método verifica se o token atual é o esperado e avança para o próximo.
        # Se não for, ele levanta um erro de sintaxe.
        if self.current_token.code != expected_token_code:
            raise RuntimeError(f"Syntax Error: Expected {expected_token_code.name} but got '{self.current_token.content}' ({self.current_token.code.name}) at line {self.current_token.line_num}")
        self.next_token()

    def next_token(self):
        # Avança para o próximo token, ignorando comentários.
        # A lógica para ignorar comentários pode ser aqui ou no lexer.
        # Se o lexer já retorna TOKEN_COMMENTS, o parser pode descartá-los.
        self.current_token = self.lexer.get_next_token()
        while self.current_token.code == TokenCode.TOKEN_COMMENTS:
            self.current_token = self.lexer.get_next_token()

    def parse(self) -> bool:
        """
        Método principal para iniciar a análise sintática de um arquivo PDDL.
        Espera a estrutura (define (...)).
        """
        try:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre (
            self.check_token(TokenCode.TOKEN_DEFINE)      # define
            self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre o sub-expressão (domain ...) ou (problem ...)

            if self.current_token.code == TokenCode.TOKEN_DOMAIN:
                self.check_token(TokenCode.TOKEN_DOMAIN)
                self.parse_domain_definition() # Chama o método para analisar a definição de domínio
            elif self.current_token.code == TokenCode.TOKEN_PROBLEM:
                self.check_token(TokenCode.TOKEN_PROBLEM)
                self.parse_problem_definition() # Chama o método para analisar a definição de problema
            else:
                raise RuntimeError(f"Syntax Error: Expected 'domain' or 'problem' after 'define' at line {self.current_token.line_num}")
            
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha o 'define' principal
            self.check_token(TokenCode.TOKEN_EOF) # Garante que não há mais nada no arquivo
            return True
        except RuntimeError as e:
            # Re-lança a exceção para que o main.py possa capturá-la e imprimir a mensagem
            raise e 

    # --- Métodos para analisar seções específicas do PDDL ---

    def parse_domain_definition(self):
        """
        Analisa a estrutura de uma definição de domínio: (domain <identifier> ...)
        """
        self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome do domínio
        self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha (domain <identifier>)

        # Loop para analisar as seções opcionais do domínio
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.next_token() # Consome o '(' que abre a seção
            if self.current_token.code == TokenCode.TOKEN_COLON: # Quase todas as seções começam com ':'
                self.next_token() # Consome o ':'
                if self.current_token.code == TokenCode.TOKEN_REQUIREMENTS:
                    self.parse_requirements_section()
                elif self.current_token.code == TokenCode.TOKEN_TYPES:
                    self.parse_types_section()
                elif self.current_token.code == TokenCode.TOKEN_CONSTANTS:
                    self.parse_constants_section()
                elif self.current_token.code == TokenCode.TOKEN_PREDICATES:
                    self.parse_predicates_section()
                elif self.current_token.code == TokenCode.TOKEN_FUNCTIONS:
                    self.parse_functions_section()
                elif self.current_token.code == TokenCode.TOKEN_ACTION:
                    self.parse_action_definition()
                # Adicione mais 'elif' para outras seções como 'durative-action', 'derived', etc.
                else:
                    raise RuntimeError(f"Syntax Error: Unexpected domain section '{self.current_token.content}' at line {self.current_token.line_num}")
            else:
                 raise RuntimeError(f"Syntax Error: Expected ':' or closing ')' for domain section at line {self.current_token.line_num}")
            
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha a seção atual
    
    def parse_problem_definition(self):
        """
        Analisa a estrutura de uma definição de problema: (problem <identifier> ...)
        """
        self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome do problema
        self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha (problem <identifier>)

        # Próxima seção deve ser o domínio associado
        self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre (
        self.check_token(TokenCode.TOKEN_COLON)        # :
        self.check_token(TokenCode.TOKEN_DOMAIN)       # domain
        self.check_token(TokenCode.TOKEN_IDENTIFIER)   # Nome do domínio
        self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha (:domain ...)

        # Loop para analisar as seções opcionais do problema
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.next_token() # Consome o '(' que abre a seção
            if self.current_token.code == TokenCode.TOKEN_COLON:
                self.next_token() # Consome o ':'
                if self.current_token.code == TokenCode.TOKEN_OBJECTS:
                    self.parse_objects_section()
                elif self.current_token.code == TokenCode.TOKEN_INIT:
                    self.parse_init_section()
                elif self.current_token.code == TokenCode.TOKEN_GOAL:
                    self.parse_goal_section()
                elif self.current_token.code == TokenCode.TOKEN_METRIC:
                    self.parse_metric_section()
                # Adicione mais 'elif' para outras seções de problema
                else:
                    raise RuntimeError(f"Syntax Error: Unexpected problem section '{self.current_token.content}' at line {self.current_token.line_num}")
            else:
                 raise RuntimeError(f"Syntax Error: Expected ':' or closing ')' for problem section at line {self.current_token.line_num}")
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha a seção atual


    def parse_requirements_section(self):
        """Analisa a seção (:requirements ...)"""
        # Já consumiu o ( e o :requirements
        # Espera uma sequência de requisitos (que geralmente começam com :)
        while self.current_token.code == TokenCode.TOKEN_COLON:
            self.next_token() # Consome o ':' do requisito (ex: :strips)
            self.check_token(TokenCode.TOKEN_IDENTIFIER) # O nome do requisito (e.g., strips, typing)
            # Pode haver mais complexidade em requisitos, mas por enquanto, um identificador basta.

    def parse_types_section(self):
        """Analisa a seção (:types ...)"""
        # Já consumiu o ( e o :types
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER: # Pode ser um tipo
            self.next_token() # Consome o tipo
            # Opcional: lidar com herança de tipos (ex: - object)
            if self.current_token.content == '-': # Check for type inheritance
                self.next_token() # Consume '-'
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Consume parent type

    def parse_constants_section(self):
        """Analisa a seção (:constants ...)"""
        # Já consumiu o ( e o :constants
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
            self.next_token() # Consome a constante
            if self.current_token.content == '-':
                self.next_token()
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Consome o tipo

    def parse_predicates_section(self):
        """Analisa a seção (:predicates ...)"""
        # Já consumiu o ( e o :predicates
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS: # Cada predicado é uma S-expression
            self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre o predicado (pode-voar ?x - aviao)
            self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome do predicado
            self.parse_parameters() # Analisa os parâmetros do predicado
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha o predicado

    def parse_functions_section(self):
        """Analisa a seção (:functions ...)"""
        # Já consumiu o ( e o :functions
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS: # Cada função é uma S-expression
            self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre a função (custo-viagem ?a - aviao)
            self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome da função
            self.parse_parameters() # Analisa os parâmetros da função
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha a função
            # Opcional: lidar com o tipo de retorno da função (ex: - number)
            if self.current_token.content == '-':
                self.next_token()
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Tipo de retorno (geralmente number)

    def parse_action_definition(self):
        """Analisa a estrutura de uma ação (:action <name> :parameters (...) :precondition (...) :effect (...))"""
        # Já consumiu o ( e o :action
        self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome da ação

        # Analisa as sub-seções da ação
        while self.current_token.code == TokenCode.TOKEN_COLON: # As seções de ação começam com :
            self.next_token() # Consome o ':'
            if self.current_token.code == TokenCode.TOKEN_PARAMETERS:
                self.parse_parameters_section()
            elif self.current_token.code == TokenCode.TOKEN_PRECONDITION:
                self.parse_precondition_section()
            elif self.current_token.code == TokenCode.TOKEN_EFFECT:
                self.parse_effect_section()
            # Adicione mais 'elif' para 'duration', 'condition' de durative-action se for implementar
            else:
                raise RuntimeError(f"Syntax Error: Unexpected action section '{self.current_token.content}' at line {self.current_token.line_num}")
    
    def parse_parameters_section(self):
        """Analisa a seção :parameters (...)"""
        # Já consumiu o :parameters
        self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre o (parameters ...)
        # Parâmetros são variáveis tipadas
        while self.current_token.code == TokenCode.TOKEN_VAR_IDENTIFIER:
            self.next_token() # Consome a variável (?x)
            if self.current_token.content == '-': # Checa por tipagem
                self.next_token() # Consome '-'
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Consome o tipo
        self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha o (parameters ...)

    def parse_precondition_section(self):
        """Analisa a seção :precondition (...)"""
        # Já consumiu o :precondition
        # Preconditions são geralmente expressões lógicas. Vamos simplificar por enquanto.
        # Por exemplo, pode ser uma lista de predicados.
        self.parse_expression() # Método genérico para analisar expressões

    def parse_effect_section(self):
        """Analisa a seção :effect (...)"""
        # Já consumiu o :effect
        # Efeitos são geralmente listas de predicados que se tornam verdadeiros ou falsos, ou modificadores numéricos.
        self.parse_expression() # Método genérico para analisar expressões

    def parse_objects_section(self):
        """Analisa a seção (:objects ...) em um problema."""
        # Já consumiu o ( e o :objects
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER: # Pode ser um objeto
            self.next_token() # Consome o objeto
            # Opcional: lidar com tipos (ex: - object)
            if self.current_token.content == '-': # Check for type inheritance
                self.next_token() # Consume '-'
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Consume type

    def parse_init_section(self):
        """Analisa a seção (:init ...) em um problema."""
        # Já consumiu o ( e o :init
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS: # Cada estado inicial é uma S-expression
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            # Pode ser um predicado (pode-voar aviao1) ou uma atribuição (= (custo aviao1) 10)
            if self.current_token.code == TokenCode.TOKEN_EQUAL: # Para funções
                self.next_token()
                self.parse_function_assignment()
            else: # Para predicados
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome do predicado
                while self.current_token.code == TokenCode.TOKEN_IDENTIFIER: # Argumentos
                    self.next_token()
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)

    def parse_function_assignment(self):
        """Analisa uma atribuição de função como (= (funcao_x ?arg) 10)"""
        # Já consumiu o '='
        self.check_token(TokenCode.TOKEN_LPARENTHESIS) # Abre (funcao_x ?arg)
        self.check_token(TokenCode.TOKEN_IDENTIFIER) # Nome da função
        # Argumentos da função
        while self.current_token.code in [TokenCode.TOKEN_IDENTIFIER, TokenCode.TOKEN_VAR_IDENTIFIER]:
            self.next_token()
        self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha (funcao_x ?arg)
        self.check_token(TokenCode.TOKEN_NUMBER) # O valor da atribuição

    def parse_goal_section(self):
        """Analisa a seção (:goal ...) em um problema."""
        # Já consumiu o ( e o :goal
        self.parse_expression() # Metas são expressões lógicas

    def parse_metric_section(self):
        """Analisa a seção (:metric ...) em um problema."""
        # Já consumiu o ( e o :metric
        # Ex: (:metric minimize (total-cost))
        self.next_token() # Deve ser minimize ou maximize
        if self.current_token.code not in [TokenCode.TOKEN_MINIMIZE, TokenCode.TOKEN_MAXIMIZE]:
            raise RuntimeError(f"Syntax Error: Expected 'minimize' or 'maximize' in metric section at line {self.current_token.line_num}")
        self.next_token() # Consome o minimize/maximize
        self.parse_expression() # A expressão da métrica

    def parse_expression(self):
        """
        Um método genérico para analisar expressões que podem ser complexas
        (e.g., (:and (pred1) (pred2)) ou (= (funcao) 10)).
        Esta é uma simplificação e precisaria de mais regras para um parser completo.
        """
        # Por enquanto, vamos apenas consumir tokens dentro de um parêntese
        # até encontrar o fechamento, sem validar a estrutura interna da expressão.
        # ISSO É UMA SIMPLIFICAÇÃO GRANDE e precisa ser melhorado para um parser real.
        if self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.next_token() # Consome o '('
            while self.current_token.code != TokenCode.TOKEN_RPARENTHESIS and self.current_token.code != TokenCode.TOKEN_EOF:
                self.parse_expression() # Chamada recursiva para expressões aninhadas
            self.check_token(TokenCode.TOKEN_RPARENTHESIS) # Fecha o ')'
        elif self.current_token.code in [TokenCode.TOKEN_IDENTIFIER, TokenCode.TOKEN_VAR_IDENTIFIER, TokenCode.TOKEN_NUMBER]:
            self.next_token() # Consome um identificador/número
        elif self.current_token.code in [TokenCode.TOKEN_AND, TokenCode.TOKEN_OR, TokenCode.TOKEN_NOT, TokenCode.TOKEN_EQUAL,
                                        TokenCode.TOKEN_PLUS, TokenCode.TOKEN_MINUS, TokenCode.TOKEN_MULTIPLY, TokenCode.TOKEN_DIVIDE,
                                        TokenCode.TOKEN_LESS, TokenCode.TOKEN_GREATER, TokenCode.TOKEN_LESS_EQUAL, TokenCode.TOKEN_GREATER_EQUAL,
                                        TokenCode.TOKEN_FORALL, TokenCode.TOKEN_EXISTS, TokenCode.TOKEN_WHEN, TokenCode.TOKEN_ASSIGN,
                                        TokenCode.TOKEN_SCALE_UP, TokenCode.TOKEN_SCALE_DOWN, TokenCode.TOKEN_INCREASE, TokenCode.TOKEN_DECREASE,
                                        TokenCode.TOKEN_AT, TokenCode.TOKEN_OVER, TokenCode.TOKEN_START, TokenCode.TOKEN_END,
                                        TokenCode.TOKEN_MINIMIZE, TokenCode.TOKEN_MAXIMIZE]:
            self.next_token() # Consome um operador ou palavra-chave dentro da expressão
        else:
            # Se não é um parêntese, um token direto ou um operador, é um erro ou algo inesperado
            raise RuntimeError(f"Syntax Error: Unexpected token '{self.current_token.content}' in expression at line {self.current_token.line_num}")
            
    def parse_parameters(self):
        """
        Analisa uma lista de parâmetros, comum em predicados, funções e ações.
        Ex: (?x - type1 ?y - type2)
        """
        while self.current_token.code == TokenCode.TOKEN_VAR_IDENTIFIER:
            self.next_token() # Consome a variável (e.g., ?x)
            if self.current_token.content == '-': # Verifica se tem tipagem
                self.next_token() # Consome o '-'
                self.check_token(TokenCode.TOKEN_IDENTIFIER) # Consome o tipo (e.g., object)