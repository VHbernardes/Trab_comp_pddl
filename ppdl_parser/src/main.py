import sys
import os
from .ast import parse_file_to_ast

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import Parser
from src.lexer import Lexer, TokenCode

def analyze_pddl_file(file_path: str):
    print(f"\n--- Analisando Arquivo: {file_path} ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        parser = Parser(source_code)
        success = parser.parse() 

        if success:
            print(f"SUCESSO: {file_path} está sintaticamente correto.")
        else:
            print(f"FALHA: {file_path} contém erros sintáticos.")
        
    except RuntimeError as e:
        print(f"REJEITADO: {file_path} - {e}")
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"OCORREU UM ERRO INESPERADO: {e}")

def parse_to_ast(domain_path, problem_path):
    domain_ast = parse_file_to_ast(domain_path)
    problem_ast = parse_file_to_ast(problem_path)
    return domain_ast, problem_ast

if __name__ == "__main__":
    domain_file = "exemplos/domain_helloworld.pddl"
    problem_file = "exemplos/problem_helloworld.pddl"

    if len(sys.argv) > 1:
        domain_file = sys.argv[1]
        if len(sys.argv) > 2:
            problem_file = sys.argv[2]
        else:
            problem_file = None

    analyze_pddl_file(domain_file)
    
    if problem_file:
        print("\n" + "="*60 + "\n")
        analyze_pddl_file(problem_file)
    
    print("\n--- Todos os arquivos PDDL analisados! ---")
