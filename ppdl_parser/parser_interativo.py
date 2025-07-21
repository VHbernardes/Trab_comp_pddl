import subprocess
import json

# Exemplos válidos
exemplos = {
    "1": {
        "nome": "Hello World",
        "domain": "exemplos/domain_helloworld.pddl",
        "problem": "exemplos/problem_helloworld.pddl"
    },
    "2": {
        "nome": "Blocks",
        "domain": "exemplos/domain_blocks.pddl",
        "problem": "exemplos/problem_blocks.pddl"
    },
    "3": {
        "nome": "Brainfuck",
        "domain": "exemplos/domain_brainfuck.pddl",
        "problem": "exemplos/problem_brainfuck.pddl"
    },
    "4": {
        "nome": "JSON",
        "domain": "exemplos/domain_json.pddl",
        "problem": "exemplos/problem_json.pddl"
    },
    "5": {
        "nome": "Lights",
        "domain": "exemplos/domain_lights.pddl",
        "problem": "exemplos/problem_lights.pddl"
    }
}

# Exemplos inválidos
invalidos = {
    "1": {
        "nome": "Blocks Inválido",
        "domain": "exemplos/domain_blocks_invalido.pddl",
        "problem": "exemplos/problem_blocks_invalido.pddl"
    },
    "2": {
        "nome": "JSON Inválido",
        "domain": "exemplos/domain_json_invalido.pddl",
        "problem": "exemplos/problem_json_invalido.pddl"
    }
}

def run_pddl(domain_path, problem_path):
    cmd = ["python", "-m", "src.main", domain_path, problem_path]
    print(f"\n📤 Executando: {' '.join(cmd)}\n")
    resultado = subprocess.run(cmd, capture_output=True, text=True)

    if resultado.returncode == 0:
        print("✅ Execução finalizada com sucesso.\n")
        print("📄 Saída:")
        print(resultado.stdout)
    else:
        print("❌ Erro na execução.\n")
        print("📄 Erro:")
        print(resultado.stderr)

def submenu_invalidos():
    while True:
        print("\n--- Exemplos PDDL Inválidos ---")
        for key, val in invalidos.items():
            print(f"{key} - {val['nome']}")
        print("0 - Voltar")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            break
        elif escolha in invalidos:
            inval = invalidos[escolha]
            run_pddl(inval["domain"], inval["problem"])
        else:
            print("Opção inválida. Tente novamente.")

def gerar_ast():
    print("\n🌳 --- Gerar AST ---")
    for key, val in exemplos.items():
        print(f"{key} - {val['nome']}")
    print("0 - Voltar")

    escolha = input("Escolha um exemplo: ").strip()

    if escolha == "0":
        return

    if escolha in exemplos:
        exemplo = exemplos[escolha]
        try:
            from src.main import parse_to_ast
            domain_ast, problem_ast = parse_to_ast(exemplo["domain"], exemplo["problem"])

            print("\n--- AST do Domain ---")
            print(json.dumps(domain_ast, indent=2))

            print("\n--- AST do Problem ---")
            print(json.dumps(problem_ast, indent=2))
        except Exception as e:
            print(f"Erro ao gerar AST: {e}")
    else:
        print("Opção inválida.")

def imprimir_cabecalho():
    print("==========================")
    print("🔍 Analisador PDDL Interativo")
    print("==========================\n")
    print("Este terminal interativo executa a análise léxica e sintática de arquivos PDDL.\n")
    print("📌 Opções 1 a 5: Executam exemplos válidos, analisando `domain` e `problem`.")
    print("❌ Opção 6: Contém exemplos com erros sintáticos intencionais para teste.")
    print("🌳 Opção 7: Gera a AST (Árvore Sintática Abstrata) dos arquivos PDDL.\n")

def main():
    imprimir_cabecalho()

    print("Escolha um exemplo para executar:\n")
    for key, val in exemplos.items():
        print(f"{key} - {val['nome']}")
    print("6 - Exemplos Inválidos")
    print("7 - Gerar AST de um exemplo")
    print("0 - Sair")

    escolha = input("\nDigite o número da opção desejada: ").strip()

    if escolha == "0":
        print("Saindo...")
        return True
    elif escolha == "6":
        submenu_invalidos()
    elif escolha == "7":
        gerar_ast()
    elif escolha in exemplos:
        exemplo = exemplos[escolha]
        run_pddl(exemplo["domain"], exemplo["problem"])
    else:
        print("Opção inválida. Tente novamente.")

    return False

if __name__ == "__main__":
    while True:
        if main():
            break
        print("\n---\n")
