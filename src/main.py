import csv
import msvcrt
import os
import sys
import threading
import time

import keyboard
from tabulate import tabulate

# Attempt to import winsound for Windows users.
# If you are on Linux/Mac, you get a silent print instead of a beep.
try:
    import winsound

    def beep():
        """
        Makes a beep noise. Useful to wake you up when the count is done.
        """
        winsound.Beep(750, 300)

except ImportError:

    def beep():
        # Fallback for non-Windows systems
        print("\a", end="", flush=True)


# ----- Data Directory Configuration -----
def get_data_dir():
    """
    Figures out where to store the CSVs.
    Handles the edge case where this script is frozen (e.g., PyInstaller).
    """
    if getattr(sys, "frozen", False):
        base = os.getcwd()
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


DATA_DIR = get_data_dir()
# Mapping file keys to actual paths
CSV_FILES = {
    "nuclei": os.path.join(DATA_DIR, "nuclei.csv"),
    "damage": os.path.join(DATA_DIR, "damage.csv"),
}


# ----- Utility Functions -----


def save_csv(path, slide_id, header_keys, values):
    """
    Appends the counting results to a CSV file.
    Creates the file with headers if it doesn't exist yet.
    """
    is_new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["Slide ID"] + header_keys)
        writer.writerow([slide_id] + values)


def print_table(data_dict, title=None):
    """
    Pretty prints the dictionary using tabulate because reading raw dicts is painful.
    """
    if title:
        print(f"\n{title}")
    print(tabulate(data_dict.items(), headers=["Type", "Count"], tablefmt="fancy_grid"))


def clear_keyboard_buffer():
    """
    The 'Sanity Saver'.
    Flushes the keyboard buffer to prevent accidental inputs from carrying over
    between menus or after a frenzy of counting keypresses.
    """
    # Wait for the user to release all keys
    while any(keyboard.is_pressed(key) for key in keyboard._pressed_events):  # type: ignore
        time.sleep(0.05)
    time.sleep(0.2)  # Short pause to ensure buffer is truly empty

    # Clear any residual input in stdin
    while msvcrt.kbhit():
        msvcrt.getch()


# ----- Generic Counting Mode -----


def count_mode(
    mode_name: str, key_map: dict, limit_key: str, limit_count: int, csv_key: str
):
    """
    The core logic. Hooks keyboard events to counters.
    Stops when the limit is reached or the user rage-quits (ESC).
    """
    # Clean slate
    keyboard.unhook_all()
    stop_event = threading.Event()
    counts = {k: 0 for k in key_map}

    # Getting the slide ID before starting counting
    slide_id = input(f"\nEnter Slide ID for {mode_name}: ").upper().strip()

    print(f"\n=== Starting {mode_name} Count (Slide: {slide_id}) ===")
    print("\nControls:")
    for type_label, key in key_map.items():
        print(f"  {key!r} → {type_label}")
    print("  'TAB' → Show current stats")
    print("  'ESC' → Manual abort\n")

    # Define which keys contribute to the "Nucleated" limit (everything except NEC, AP, IDNC)
    nucleated_types = [k for k in key_map if k not in ("NEC", "AP", "IDNC")]

    def get_total_nucleated():
        return sum(counts[t] for t in nucleated_types)

    def make_handler(cell_type):
        """Factory to create a closure for each key press."""

        def handler(e):
            counts[cell_type] += 1

            # Logic for Nuclei mode: Stop when sum of nucleated cells hits limit
            if limit_key is None and get_total_nucleated() >= limit_count:
                print(f"\nLimit of {limit_count} nucleated cells reached!")
                beep()
                stop_event.set()

            # Logic for Damage mode: Stop when specific cell type (e.g., BN) hits limit
            elif cell_type == limit_key and counts[limit_key] >= limit_count:
                print(f"\nLimit of {limit_count} {limit_key} reached!")
                beep()
                stop_event.set()

        return handler

    def show_current_stats(e=None):
        print_table(counts, title=f"Current Status ({mode_name})")

        if limit_key is None:
            total = sum(counts[t] for t in ("M1", "M2", "M3", "M4") if t in counts)
            print(f">> Total nucleated cells (M1–M4): {total}")
        elif limit_key == "BN":
            total = counts.get("BN", 0)
            print(f">> Total Binucleated cells (BN): {total}")

    # Hook up the keys
    for cell_type, key in key_map.items():
        keyboard.on_press_key(key, make_handler(cell_type))

    keyboard.on_press_key("esc", lambda e: stop_event.set())
    keyboard.on_press_key("tab", show_current_stats)

    # Main loop waits here until stop_event is triggered
    while not stop_event.is_set():
        time.sleep(0.1)

    # Cleanup
    keyboard.unhook_all()
    print_table(counts, title=f"Summary {mode_name} - Slide {slide_id}")

    save_csv(CSV_FILES[csv_key], slide_id, list(counts.keys()), list(counts.values()))
    print(f">> Data saved to {CSV_FILES[csv_key]}\n")


# ----- General Summary Function -----


def show_summary():
    """Reads the CSVs and dumps them to the terminal."""
    for key, path in CSV_FILES.items():
        mode = "Nuclei" if key == "nuclei" else "Damage"
        print(f"\n📊 Summary for {mode}:")

        if not os.path.exists(path):
            print("  (No records found yet)")
            continue

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)

        if not data:
            print("  (File is empty)")
        else:
            print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))
    print()


# ----- Main Menu -----


def main():
    while True:
        print("===== Main Menu =====")
        print("1) Count Nuclei")
        print("2) Count Damage")
        print("3) View Summary")
        print("4) Exit")

        clear_keyboard_buffer()
        choice = input("Option: ").strip()

        if choice == "1":
            count_mode(
                mode_name="Nuclei",
                key_map={
                    "M1": "1",
                    "M2": "2",
                    "M3": "3",
                    "M4": "4",
                    "NEC": "5",
                    "AP": "6",
                    "IDNC": "7",
                },
                limit_key=None,  # type: ignore
                limit_count=500,
                csv_key="nuclei",
            )
        elif choice == "2":
            count_mode(
                mode_name="Damage",
                key_map={"BN": "q", "MN": "w", "NBUD": "e", "NPB": "r"},
                limit_key="BN",
                limit_count=1000,
                csv_key="damage",
            )
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Shutting down...")
            sys.exit(0)
        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()
