from typing import List, Tuple
from .lexer import Token, TokenCode, Lexer
import sys

class Parser:
    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.current_token = self.lexer.get_next_token()

    def check_token(self, expected_token_code: TokenCode):
        if self.current_token.code != expected_token_code:
            raise RuntimeError(
                f"Erro de Sintaxe: Esperava {expected_token_code.name} "
                f"mas encontrou '{self.current_token.content}' ({self.current_token.code.name}) "
                f"na linha {self.current_token.line_num}"
            )
        self.next_token()

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
        while self.current_token.code == TokenCode.TOKEN_COMMENTS:
            self.current_token = self.lexer.get_next_token()

    def parse(self) -> bool:
        try:
            print("   [Parser]: Iniciando análise do bloco 'define'...")
            self.parse_define_block()
            self.check_token(TokenCode.TOKEN_EOF)
            return True
        except RuntimeError as e:
            raise e

    def parse_define_block(self):
        self.check_token(TokenCode.TOKEN_LPARENTHESIS)
        print("   [Parser]: Encontrou '(' de abertura do 'define'.")
        self.check_token(TokenCode.TOKEN_DEFINE)
        print("   [Parser]: Encontrou palavra-chave 'define'.")
        self.check_token(TokenCode.TOKEN_LPARENTHESIS)
        print("   [Parser]: Encontrou '(' de abertura do tipo de definição (domain/problem).")

        if self.current_token.code == TokenCode.TOKEN_DOMAIN:
            print("   [Parser]: Identificou que é uma definição de DOMÍNIO.")
            self.parse_domain_definition()
        elif self.current_token.code == TokenCode.TOKEN_PROBLEM:
            print("   [Parser]: Identificou que é uma definição de PROBLEMA.")
            self.parse_problem_definition()
        else:
            raise RuntimeError(
                f"Erro de Sintaxe: Esperava 'domain' ou 'problem' após 'define' "
                f"na linha {self.current_token.line_num}"
            )
        
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)
        print("   [Parser]: Encontrou ')' de fechamento do 'define' principal.")

    def parse_domain_definition(self):
        self.check_token(TokenCode.TOKEN_DOMAIN)
        print("   [Parser]: Encontrou palavra-chave 'domain'.")
        domain_name = self.current_token.content
        self.check_token(TokenCode.TOKEN_IDENTIFIER)
        print(f"   [Parser]: Nome do domínio: '{domain_name}'.")
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)
        print("   [Parser]: Encontrou ')' de fechamento do 'domain' name.")
        
        self.parse_domain_body()

    def parse_problem_definition(self):
        self.check_token(TokenCode.TOKEN_PROBLEM)
        print("   [Parser]: Encontrou palavra-chave 'problem'.")
        problem_name = self.current_token.content
        self.check_token(TokenCode.TOKEN_IDENTIFIER)
        print(f"   [Parser]: Nome do problema: '{problem_name}'.")
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)
        print("   [Parser]: Encontrou ')' de fechamento do 'problem' name.")
        
        print("   [Parser]: Esperando seção ':domain' no problema...")
        self.check_token(TokenCode.TOKEN_LPARENTHESIS)
        self.check_token(TokenCode.TOKEN_COLON)
        self.check_token(TokenCode.TOKEN_DOMAIN)
        associated_domain_name = self.current_token.content
        self.check_token(TokenCode.TOKEN_IDENTIFIER)
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)
        print(f"   [Parser]: Encontrou seção ':domain' referenciando '{associated_domain_name}'.")
        
        self.parse_problem_body_sections()

    def parse_domain_body(self):
        print("   [Parser]: Iniciando análise do corpo do domínio...")
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            self.check_token(TokenCode.TOKEN_COLON)
            print(f"   [Parser]: Encontrou início de seção. Tipo: {self.current_token.content}")

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
            elif self.current_token.code == TokenCode.TOKEN_DURATIVE_ACTION:
                self.parse_durative_action_definition()
            elif self.current_token.code == TokenCode.TOKEN_DERIVED:
                self.parse_derived_predicates_definition()
            else:
                raise RuntimeError(
                    f"Erro de Sintaxe: Token inesperado '{self.current_token.content}' "
                    f"como palavra-chave de seção de domínio na linha {self.current_token.line_num}"
                )
            
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)
            print(f"   [Parser]: Seção '{self.current_token.content}' finalizada com ')'.")
        print("   [Parser]: Finalizou análise do corpo do domínio.")

    def parse_problem_body_sections(self):
        print("   [Parser]: Iniciando análise das seções do corpo do problema...")
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            self.check_token(TokenCode.TOKEN_COLON)
            print(f"   [Parser]: Encontrou início de seção. Tipo: {self.current_token.content}")

            if self.current_token.code == TokenCode.TOKEN_OBJECTS:
                self.parse_objects_section()
            elif self.current_token.code == TokenCode.TOKEN_INIT:
                self.parse_init_section()
            elif self.current_token.code == TokenCode.TOKEN_GOAL:
                self.parse_goal_section()
            elif self.current_token.code == TokenCode.TOKEN_METRIC:
                self.parse_metric_section()
            else:
                raise RuntimeError(
                    f"Erro de Sintaxe: Token inesperado '{self.current_token.content}' "
                    f"como palavra-chave de seção de problema na linha {self.current_token.line_num}"
                )
            
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)
            print(f"   [Parser]: Seção '{self.current_token.content}' finalizada com ')'.")
        print("   [Parser]: Finalizou análise das seções do corpo do problema.")

    def parse_requirements_section(self):
        self.check_token(TokenCode.TOKEN_REQUIREMENTS)
        print("     [Parser]: Analisando seção ':requirements'.")
        while self.current_token.code == TokenCode.TOKEN_COLON:
            self.next_token()
            req_name = self.current_token.content
            self.check_token(TokenCode.TOKEN_IDENTIFIER)
            print(f"       [Parser]: Requisito: ':{req_name}'.")

    def parse_types_section(self):
        self.check_token(TokenCode.TOKEN_TYPES)
        print("     [Parser]: Analisando seção ':types'.")
        current_types_group = []
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
            type_name = self.current_token.content
            self.next_token()
            current_types_group.append(type_name)
            
            if self.current_token.content == '-':
                self.next_token()
                parent_type_name = self.current_token.content
                self.check_token(TokenCode.TOKEN_IDENTIFIER)
                print(f"       [Parser]: Tipos: {', '.join(current_types_group)} - '{parent_type_name}'.")
                current_types_group = []
            elif self.current_token.code != TokenCode.TOKEN_IDENTIFIER:
                print(f"       [Parser]: Tipos: {', '.join(current_types_group)}.")
                current_types_group = []

    def parse_constants_section(self):
        self.check_token(TokenCode.TOKEN_CONSTANTS)
        print("     [Parser]: Analisando seção ':constants'.")
        current_constants_group = []
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
            const_name = self.current_token.content
            self.next_token()
            current_constants_group.append(const_name)

            if self.current_token.content == '-':
                self.next_token()
                const_type_name = self.current_token.content
                self.check_token(TokenCode.TOKEN_IDENTIFIER)
                print(f"       [Parser]: Constantes: {', '.join(current_constants_group)} - '{const_type_name}'.")
                current_constants_group = []
            elif self.current_token.code != TokenCode.TOKEN_IDENTIFIER:
                print(f"       [Parser]: Constantes: {', '.join(current_constants_group)}.")
                current_constants_group = []

    def parse_predicates_section(self):
        self.check_token(TokenCode.TOKEN_PREDICATES)
        print("     [Parser]: Analisando seção ':predicates'.")
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            name = self.current_token.content
            self.check_token(TokenCode.TOKEN_IDENTIFIER)
            params = self.parse_parameters()
            print(f"       [Parser]: Predicado: '{name}' com parâmetros: {params}.")
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)

    def parse_functions_section(self):
        self.check_token(TokenCode.TOKEN_FUNCTIONS)
        print("     [Parser]: Analisando seção ':functions'.")
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            func_name = self.current_token.content
            self.check_token(TokenCode.TOKEN_IDENTIFIER)
            params = self.parse_parameters()
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)
            
            return_type = "number"
            if self.current_token.content == '-':
                self.next_token()
                return_type = self.current_token.content
                self.check_token(TokenCode.TOKEN_IDENTIFIER)
            print(f"       [Parser]: Função: '{func_name}' com parâmetros: {params} e retorno '{return_type}'.")

    def parse_action_definition(self):
        self.check_token(TokenCode.TOKEN_ACTION)
        action_name = self.current_token.content
        self.check_token(TokenCode.TOKEN_IDENTIFIER)
        print(f"     [Parser]: Analisando ação: '{action_name}'.")

        while self.current_token.code == TokenCode.TOKEN_COLON:
            self.next_token()
            section_type = self.current_token.content

            if self.current_token.code == TokenCode.TOKEN_PARAMETERS:
                self.parse_parameters_section()
            elif self.current_token.code == TokenCode.TOKEN_PRECONDITION:
                self.parse_precondition_section()
            elif self.current_token.code == TokenCode.TOKEN_EFFECT:
                self.parse_effect_section()
            else:
                raise RuntimeError(
                    f"Erro de Sintaxe: Sub-seção inesperada da ação '{self.current_token.content}' "
                    f"na linha {self.current_token.line_num}"
                )
            print(f"       [Parser]: Sub-seção de ação '{section_type}' finalizada.")

    def parse_parameters_section(self):
        self.check_token(TokenCode.TOKEN_PARAMETERS)
        self.check_token(TokenCode.TOKEN_LPARENTHESIS)
        print("       [Parser]: Analisando :parameters de ação...")
        self.parse_parameters()
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)

    def parse_precondition_section(self):
        self.check_token(TokenCode.TOKEN_PRECONDITION)
        print("       [Parser]: Analisando :precondition de ação...")
        self.parse_expression("precondition")

    def parse_effect_section(self):
        self.check_token(TokenCode.TOKEN_EFFECT)
        print("       [Parser]: Analisando :effect de ação...")
        self.parse_expression("effect")

    def parse_objects_section(self):
        self.check_token(TokenCode.TOKEN_OBJECTS)
        print("     [Parser]: Analisando seção ':objects'.")
        current_objects_group = []
        while self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
            obj_name = self.current_token.content
            self.next_token()
            current_objects_group.append(obj_name)
            
            if self.current_token.content == '-':
                self.next_token()
                obj_type_name = self.current_token.content
                self.check_token(TokenCode.TOKEN_IDENTIFIER)
                print(f"       [Parser]: Objetos: {', '.join(current_objects_group)} - '{obj_type_name}'.")
                current_objects_group = []
            elif self.current_token.code != TokenCode.TOKEN_IDENTIFIER:
                print(f"       [Parser]: Objetos: {', '.join(current_objects_group)}.")
                current_objects_group = []

    def parse_init_section(self):
        self.check_token(TokenCode.TOKEN_INIT)
        print("     [Parser]: Analisando seção ':init'.")
        while self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.check_token(TokenCode.TOKEN_LPARENTHESIS)
            
            if self.current_token.code == TokenCode.TOKEN_EQUAL or \
               self.current_token.code in [TokenCode.TOKEN_PLUS, TokenCode.TOKEN_MINUS, TokenCode.TOKEN_MULTIPLY, TokenCode.TOKEN_DIVIDE,
                                           TokenCode.TOKEN_ASSIGN, TokenCode.TOKEN_INCREASE, TokenCode.TOKEN_DECREASE,
                                           TokenCode.TOKEN_SCALE_UP, TokenCode.TOKEN_SCALE_DOWN]:
                self.parse_function_assignment_or_modification()
            elif self.current_token.code == TokenCode.TOKEN_NOT:
                self.next_token()
                print("       [Parser]: Encontrou 'not' em init.")
                self.parse_expression("init (negated)")
            else:
                name = self.current_token.content
                self.next_token()
                args = []
                while self.current_token.code in [TokenCode.TOKEN_IDENTIFIER, TokenCode.TOKEN_VAR_IDENTIFIER, TokenCode.TOKEN_NUMBER]:
                    args.append(self.current_token.content)
                    self.next_token()
                print(f"       [Parser]: Fato inicial: '({name} {' '.join(args)})'.")
            
            self.check_token(TokenCode.TOKEN_RPARENTHESIS)

    def parse_function_assignment_or_modification(self):
        operator = self.current_token.content
        self.next_token()
        print(f"       [Parser]: Encontrou atribuição/modificação de função com operador '{operator}'.")

        self.check_token(TokenCode.TOKEN_LPARENTHESIS)
        func_name = self.current_token.content
        self.check_token(TokenCode.TOKEN_IDENTIFIER)
        args = []
        while self.current_token.code in [TokenCode.TOKEN_IDENTIFIER, TokenCode.TOKEN_VAR_IDENTIFIER]:
            args.append(self.current_token.content)
            self.next_token()
        self.check_token(TokenCode.TOKEN_RPARENTHESIS)
        
        value = self.current_token.content
        self.parse_expression_atom()
        
        print(f"         [Parser]: Função '{func_name}' com args ({' '.join(args)}) e valor '{value}'.")

    def parse_goal_section(self):
        self.check_token(TokenCode.TOKEN_GOAL)
        print("     [Parser]: Analisando seção ':goal'.")
        self.parse_expression("goal")

    def parse_metric_section(self):
        self.check_token(TokenCode.TOKEN_METRIC)
        print("     [Parser]: Analisando seção ':metric'.")
        metric_type = self.current_token.content
        if self.current_token.code not in [TokenCode.TOKEN_MINIMIZE, TokenCode.TOKEN_MAXIMIZE]:
            raise RuntimeError(f"Erro de Sintaxe: Esperava 'minimize' ou 'maximize' na seção metric na linha {self.current_token.line_num}")
        self.next_token()
        print(f"       [Parser]: Métrica definida como '{metric_type}'.")
        self.parse_expression("metric expression")

    def parse_parameters(self) -> List[Tuple[str, str]]:
        params_info = []
        while self.current_token.code == TokenCode.TOKEN_VAR_IDENTIFIER:
            var_name = self.current_token.content
            self.next_token()
            param_type = "object"
            if self.current_token.content == '-':
                self.next_token()
                param_type = self.current_token.content
                self.check_token(TokenCode.TOKEN_IDENTIFIER)
            params_info.append(f"{var_name} - {param_type}")
        print(f"         [Parser]: Parâmetros reconhecidos: [{', '.join(params_info)}]")
        return params_info


    def parse_expression(self, context: str = "general expression"):
        if self.current_token.code == TokenCode.TOKEN_LPARENTHESIS:
            self.next_token()
            
            if self.current_token.code == TokenCode.TOKEN_RPARENTHESIS:
                print(f"         [Parser]: Expressão '{context}': Encontrou expressão vazia '()'.")
            
            elif self.current_token.code in [
                TokenCode.TOKEN_AND, TokenCode.TOKEN_OR, TokenCode.TOKEN_NOT, TokenCode.TOKEN_WHEN,
                TokenCode.TOKEN_EQUAL, TokenCode.TOKEN_PLUS, TokenCode.TOKEN_MINUS, 
                TokenCode.TOKEN_MULTIPLY, TokenCode.TOKEN_DIVIDE,
                TokenCode.TOKEN_LESS, TokenCode.TOKEN_GREATER, TokenCode.TOKEN_LESS_EQUAL, TokenCode.TOKEN_GREATER_EQUAL,
                TokenCode.TOKEN_ASSIGN, TokenCode.TOKEN_INCREASE, TokenCode.TOKEN_DECREASE,
                TokenCode.TOKEN_SCALE_UP, TokenCode.TOKEN_SCALE_DOWN,
                TokenCode.TOKEN_FORALL, TokenCode.TOKEN_EXISTS,
                TokenCode.TOKEN_AT, TokenCode.TOKEN_OVER, TokenCode.TOKEN_START, TokenCode.TOKEN_END
            ]:
                operator_value = self.current_token.content.lower()
                self.next_token()
                print(f"         [Parser]: Expressão '{context}': Operador '{operator_value}'.")
                
                if self.current_token.code == TokenCode.TOKEN_RPARENTHESIS:
                    print(f"           [Parser]: Expressão '{context}' ({operator_value}): Encontrou operador sem argumentos.")
                else:
                    while self.current_token.code != TokenCode.TOKEN_RPARENTHESIS and \
                            self.current_token.code != TokenCode.TOKEN_EOF:
                        self.parse_expression(f"{context} (sub-expr de {operator_value})")
                
            elif self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
                name = self.current_token.content
                self.next_token()
                args = []
                while self.current_token.code in [TokenCode.TOKEN_IDENTIFIER, TokenCode.TOKEN_VAR_IDENTIFIER]:
                    args.append(self.current_token.content)
                    self.next_token()
                print(f"         [Parser]: Expressão '{context}': Literal/Chamada: '({name} {' '.join(args)})'.")

            else:
                 raise RuntimeError(
                    f"Erro de Sintaxe: Token inesperado '{self.current_token.content}' "
                    f"dentro de uma expressão na linha {self.current_token.line_num}. Esperava operador, identificador ou ')'. "
                    f"Contexto: {context}"
                )

            self.check_token(TokenCode.TOKEN_RPARENTHESIS)
            print(f"         [Parser]: Expressão '{context}' finalizada com ')'.")
        
        else:
            self.parse_expression_atom(context)


    def parse_expression_atom(self, context: str = "atom"):
        if self.current_token.code == TokenCode.TOKEN_IDENTIFIER:
            val = self.current_token.content
            self.next_token()
            print(f"         [Parser]: Átomo '{context}': Identificador '{val}'.")
        elif self.current_token.code == TokenCode.TOKEN_VAR_IDENTIFIER:
            val = self.current_token.content
            self.next_token()
            print(f"         [Parser]: Átomo '{context}': Variável '{val}'.")
        elif self.current_token.code == TokenCode.TOKEN_NUMBER:
            val = self.current_token.content
            self.next_token()
            print(f"         [Parser]: Átomo '{context}': Número '{val}'.")
        else:
            raise RuntimeError(
                f"Erro de Sintaxe: Token inesperado '{self.current_token.content}' "
                f"em átomo de expressão na linha {self.current_token.line_num}. Esperava identificador, variável ou número."
            )

    def parse_durative_action_definition(self):
        self.check_token(TokenCode.TOKEN_DURATIVE_ACTION)
        print("     [Parser]: Ignorando seção ':durative-action' (não implementada).")
        while self.current_token.code != TokenCode.TOKEN_RPARENTHESIS and \
              self.current_token.code != TokenCode.TOKEN_EOF:
            self.next_token()

    def parse_derived_predicates_definition(self):
        self.check_token(TokenCode.TOKEN_DERIVED)
        print("     [Parser]: Ignorando seção ':derived' (não implementada).")
        while self.current_token.code != TokenCode.TOKEN_RPARENTHESIS and \
              self.current_token.code != TokenCode.TOKEN_EOF:
            self.next_token()