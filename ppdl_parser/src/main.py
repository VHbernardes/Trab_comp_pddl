import sys
import os
from .parser import Parser # Importa a classe Parser do seu modulo parser.py

def read_source_file(file_path: str) -> str:
    """
    Funcao utilitaria para ler o conteudo de um arquivo.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return file.read()

def main():
    """
    Funcao principal do programa.
    Espera dois argumentos de linha de comando: o caminho para o arquivo de dominio PDDL
    e o caminho para o arquivo de problema PDDL.
    """
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <domain.pddl> <problem.pddl>")
        sys.exit(1) # Sai com codigo de erro 1

    domain_file = sys.argv[1]
    problem_file = sys.argv[2]

    # Processa o arquivo de dominio
    try:
        print(f"--- Analyzing Domain File: {domain_file} ---")
        domain_code = read_source_file(domain_file)
        domain_parser = Parser(domain_code)
        domain_parser.parse()
        print(f"SUCCESS: {domain_file} is syntactically correct.\n")
    except FileNotFoundError as e:
        print(f"ERROR: {e}\n")
        sys.exit(1)
    except RuntimeError as e:
        # A excecao do parser ja contem a mensagem detalhada
        print(f"REJECTED: {domain_file} - {e}\n")
        sys.exit(1)
    
    # Processa o arquivo de problema
    try:
        print(f"--- Analyzing Problem File: {problem_file} ---")
        problem_code = read_source_file(problem_file)
        problem_parser = Parser(problem_code)
        problem_parser.parse()
        print(f"SUCCESS: {problem_file} is syntactically correct.\n")
    except FileNotFoundError as e:
        print(f"ERROR: {e}\n")
        sys.exit(1)
    except RuntimeError as e:
        # A excecao do parser ja contem a mensagem detalhada
        print(f"REJECTED: {problem_file} - {e}\n")
        sys.exit(1)

    print("--- All PDDL files analyzed successfully! ---")

if __name__ == "__main__":
    main()