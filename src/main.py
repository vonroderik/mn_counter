import os
import sys
import csv
import threading
import time
import msvcrt


try:
    import winsound

    def beep():
        winsound.Beep(750, 300)

except ImportError:

    def beep():
        print("\a", end="", flush=True)


import keyboard
from tabulate import tabulate


# ----- Configuração de diretório de dados -----
def get_data_dir():
    if getattr(sys, "frozen", False):
        base = os.getcwd()
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


DATA_DIR = get_data_dir()
CSV_FILES = {
    "nuclei": os.path.join(DATA_DIR, "nucleos.csv"),
    "damage": os.path.join(DATA_DIR, "danos.csv"),
}

# ----- Funções utilitárias -----


def save_csv(path, lamina_id, header_keys, values):
    novo = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if novo:
            writer.writerow(["ID da Lâmina"] + header_keys)
        writer.writerow([lamina_id] + values)


def print_table(data_dict, title=None):
    if title:
        print(f"\n{title}")
    print(
        tabulate(
            data_dict.items(), headers=["Tipo", "Quantidade"], tablefmt="fancy_grid"
        )
    )


def limpar_buffer_teclado():
    # Aguarda o usuário soltar todas as teclas do sistema
    while any(keyboard.is_pressed(key) for key in keyboard._pressed_events):
        time.sleep(0.05)
    time.sleep(0.2)  # pausa para esvaziar buffer

    # Limpa qualquer entrada residual no stdin
    while msvcrt.kbhit():
        msvcrt.getch()


# ----- Modo genérico de contagem -----


def count_mode(
    nome_modo: str, key_map: dict, limit_key: str, limit_count: int, csv_key: str
):
    keyboard.unhook_all()
    stop_event = threading.Event()
    contagem = {tipo: 0 for tipo in key_map}

    lamina = input(f"\nID da lâmina para {nome_modo}: ").upper().strip()
    print(f"\n=== Iniciando contagem de {nome_modo} (lâmina {lamina}) ===")
    print("\nPressione as teclas:")
    for tipo, tecla in key_map.items():
        print(f"  {tecla!r} → {tipo}")
    print("  'TAB' → mostrar contagem atual")
    print("  'ESC' → abortar manualmente\n")

    tipos_com_nucleo = [k for k in key_map if k not in ("NEC", "AP", "IDNC")]

    def total_nucleados():
        return sum(contagem[tipo] for tipo in tipos_com_nucleo)

    def make_handler(tipo):
        def handler(e):
            contagem[tipo] += 1

            if limit_key is None and total_nucleados() >= limit_count:
                print(f"\nLimite de {limit_count} células com núcleo atingido!")
                beep()
                stop_event.set()

            elif tipo == limit_key and contagem[limit_key] >= limit_count:
                print(f"\nLimite de {limit_count} {limit_key} atingido!")
                beep()
                stop_event.set()

        return handler

    def mostrar_contagem(e=None):
        print_table(contagem, title=f"Contagem atual ({nome_modo})")

        if limit_key is None:
            total = sum(contagem[t] for t in ("M1", "M2", "M3", "M4") if t in contagem)
            print(f">> Total de células nucleadas (M1–M4): {total}")
        elif limit_key == "BN":
            total = contagem.get("BN", 0)
            print(f">> Total de células binucleadas (BN): {total}")

    for tipo, tecla in key_map.items():
        keyboard.on_press_key(tecla, make_handler(tipo))
    keyboard.on_press_key("esc", lambda e: stop_event.set())
    keyboard.on_press_key("tab", mostrar_contagem)

    while not stop_event.is_set():
        time.sleep(0.1)

    keyboard.unhook_all()
    print_table(contagem, title=f"Resumo {nome_modo} - lâmina {lamina}")
    save_csv(CSV_FILES[csv_key], lamina, list(contagem.keys()), list(contagem.values()))
    print(f">> Dados salvos em {CSV_FILES[csv_key]}\n")


# ----- Função de resumo geral -----


def show_summary():
    for key, path in CSV_FILES.items():
        modo = "Núcleos" if key == "nuclei" else "Danos"
        print(f"\n📊 Resumo {modo}:")
        if not os.path.exists(path):
            print("  (nenhum registro encontrado)")
            continue
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)
        if not data:
            print("  (arquivo vazio)")
        else:
            print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))
    print()


# ----- Menu principal -----


def main():
    while True:
        print("===== Menu Principal =====")
        print("1) Contagem de Núcleos")
        print("2) Contagem de Danos")
        print("3) Resumo Geral")
        print("4) Sair")
        limpar_buffer_teclado()
        escolha = input("Opção: ").strip()
        if escolha == "1":
            count_mode(
                nome_modo="Núcleos",
                key_map={
                    "M1": "1",
                    "M2": "2",
                    "M3": "3",
                    "M4": "4",
                    "NEC": "5",
                    "AP": "6",
                    "IDNC": "7",
                },
                limit_key=None,
                limit_count=500,
                csv_key="nuclei",
            )
        elif escolha == "2":
            count_mode(
                nome_modo="Danos",
                key_map={"BN": "q", "MN": "w", "NBUD": "e", "NPB": "r"},
                limit_key="BN",
                limit_count=1000,
                csv_key="damage",
            )
        elif escolha == "3":
            show_summary()
        elif escolha == "4":
            print("Encerrando...")
            sys.exit(0)
        else:
            print("Opção inválida, tente novamente.\n")


if __name__ == "__main__":
    main()
