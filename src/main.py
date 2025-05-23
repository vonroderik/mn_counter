from tabulate import tabulate
from pyfiglet import Figlet
import utils
import keyboard
from functools import partial
import csv
import os
import sys


# Funções gerais
f = Figlet(font="starwars")
print(f.renderText("MN Counter"))
print(f"por Rodrigo Noronha de Mello\n")

# dicionário principal
contagem_nucleos = {}
contagem_danos = {}


def main():
    # organiza a lógica do programa e chama as demais funções

    while True:
        try:
            print("Por favor selecione uma opção:")
            print("1 - Contagem de Núcleos")
            print("2 - Contagem de Danos")
            print("3 - Resumo da Contagem")
            print("4 - Sair")

            opcao = input("Opção: ").strip()

            if opcao.isdigit():
                opcao = int(opcao)
                if opcao == 1:
                    nucleos()
                elif opcao == 2:
                    dano()
                elif opcao == 3:
                    print_resumo_contagem()
                elif opcao == 4:
                    sys.exit()
                else:
                    print("Digite uma opção válida.")
                    continue
            else:
                print("Digite apenas números válidos.")

        except Exception as e:
            print(f"Erro inesperado: {e}")


def nucleos():
    # Função para a contagem do número de células baseado na quantidade de núcleos

    keyboard.unhook_all()

    teclado_nucleos = {
        "M1": "1",
        "M2": "2",
        "M3": "3",
        "M4": "4",
        "NEC": "5",
        "AP": "6",
        "IDNC": "7",
    }

    lamina_nucleos = input("ID da lamina: ").upper().strip()
    utils.nuclei_key_map()
    # Mapeia teclas para funções
    for tipo, tecla in teclado_nucleos.items():
        keyboard.on_press_key(tecla, partial(incrementar_nucleo, lamina_nucleos, tipo))

    keyboard.wait("esc")  # Mantém o programa rodando até pressionar 'ESC'

    print(f"\nResumo da Lâmina {lamina_nucleos + ' - Núcleos'}:")

    print_lamina_individual(contagem_nucleos, lamina_nucleos)
    salvar_em_csv("nucleos.csv", lamina_nucleos, contagem_nucleos[lamina_nucleos])
    print()
    return


def incrementar_nucleo(lamina, tipo, event=None):
    # atualiza a contagem de células em relação aos núcleos

    if lamina not in contagem_nucleos:
        contagem_nucleos[lamina] = {
            key: 0 for key in ["M1", "M2", "M3", "M4", "NEC", "AP", "IDNC"]
        }

    contagem_nucleos[lamina][tipo] += 1

    # limita a contagem até 500 células por lâmina
    if sum(contagem_nucleos[lamina].values()) >= 500:
        print("Total de 500 células contadas\n")
        print_lamina_individual(contagem_nucleos, lamina)
        print()
        return


def dano():
    # Função para a contagem de dano celular em células binucleadas

    keyboard.unhook_all()

    teclado_danos = {
        "BN": "q",
        "MN": "w",
        "NBUD": "e",
        "NPB": "r",
    }

    lamina_danos = input("ID da lamina: ").upper().strip()
    utils.damage_key_map()
    # Mapeia teclas para funções
    for tipo, tecla in teclado_danos.items():
        keyboard.on_press_key(tecla, partial(incrementar_dano, lamina_danos, tipo))

    keyboard.wait("esc")  # Mantém o programa rodando até pressionar 'ESC'
    print_lamina_individual(contagem_danos, lamina_danos)
    salvar_em_csv("danos.csv", lamina_danos, contagem_danos[lamina_danos])
    print()
    return


def incrementar_dano(lamina, tipo, event=None):
    # atualiza a contagem de células em relação aos núcleos

    if lamina not in contagem_danos:
        contagem_danos[lamina] = {key: 0 for key in ["BN", "MN", "NBUD", "NPB"]}

    contagem_danos[lamina][tipo] += 1
    # limita a contagem até 1000 células por lâmina
    if contagem_danos[lamina]["BN"] >= 1000:
        print("Total de 1000 células contadas\n")
        print_lamina_individual(contagem_danos, lamina)
        print()
        return


def print_lamina_individual(tipo, lamina):


    print(
        tabulate(
            tipo[lamina].items(),
            headers=["Tipo", "Quantidade"],
            tablefmt="fancy_grid",
        )
    )


def salvar_em_csv(nome_arquivo, id_lamina, dados):
    # Salva o arquivo em CSV automaticamente após cada contagem

    # Caminho completo para salvar na pasta 'data'
    caminho_completo = os.path.join("..", "data", nome_arquivo)
    arquivo_existe = os.path.exists(caminho_completo)

    with open(caminho_completo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Escreve o cabeçalho se o arquivo ainda não existir
        if not arquivo_existe:
            writer.writerow(["ID da Lamina"] + list(dados.keys()))

        # Escreve os dados da lâmina
        writer.writerow([id_lamina] + list(dados.values()))


def print_resumo_contagem():


    print("\n📊 CONTAGEM - Núcleos")
    print_csv_formatado("nucleos.csv")

    print("\n📊 CONTAGEM - Danos")
    print_csv_formatado("danos.csv")

    print()


def print_csv_formatado(nome_arquivo):
    caminho_completo = os.path.join("..", "data", nome_arquivo)

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_completo):
        print(f"\n⚠️ Arquivo '{nome_arquivo}' não encontrado!")
        return

    # Lê o arquivo CSV e imprime com tabulate
    with open(caminho_completo, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        dados = list(reader)

    # Verifica se o CSV tem dados antes de tentar imprimir
    if not dados:
        print(f"\n⚠️ O arquivo '{nome_arquivo}' está vazio!")
        return


    print(tabulate(dados, headers="firstrow", tablefmt="fancy_grid"))



if __name__ == "__main__":
    main()
