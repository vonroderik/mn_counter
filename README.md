# MN Counter

A CLI tool for high-throughput cytogenetic analysis and cell counting.

[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](https://github.com/vonroderik)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/vonroderik)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## About the Project

**MN Counter** is a Python-based desktop application designed to streamline the workflow of cytogeneticists and biology researchers. It replaces traditional manual clickers with a keyboard-driven interface for counting nucleated cells and cellular anomalies (such as micronuclei).

The application focuses on speed and data integrity, offering real-time statistical feedback, automated protocol limits, and persistent CSV data storage.

---

## Core Features

* **High-Throughput Logging:** Optimized keyboard shortcuts allow for rapid data entry without looking away from the microscope.
* **Dual Analysis Modes:**
    * **Nuclei Mode:** For counting mono-, bi-, tri-, and tetra-nucleated cells, including necrosis and apoptosis.
    * **Damage Mode:** Specialized tracking for micronuclei (MN), nuclear buds (NBUD), and nucleoplasmic bridges (NPB).
* **Automated Protocol Limits:** The system automatically pauses and alerts (audio/visual) when sample size targets are met (e.g., 500 nucleated cells or 1000 binucleated cells).
* **Data Persistence:** All counts are automatically saved to structured `.csv` files in a local `data/` directory, preventing data loss.
* **Real-Time Statistics:** Instant access to partial counts and summaries via hotkeys.

---

## Technologies

To build or run this project from source, you will need:

* **Python 3.10+**
* **Libraries:**
    * `keyboard` (Global hook events)
    * `tabulate` (CLI data visualization)
    * `winsound` (Windows-native audio feedback)

---

## How to Run

You can run the application via the Python interpreter.


### Running from Source

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vonroderik/mn-counter.git](https://github.com/vonroderik/mn-counter.git)
    cd mn-counter
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install keyboard tabulate
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

---

## Operation Guide

### 1. Nuclei Counting Mode
**Goal:** Assess cell division status and cytotoxicity.  
**Limit:** Stops automatically at **500** valid nucleated cells (M1-M4).

| Key | Event Code | Biological Description |
|:---:|:----------:|:-----------------------|
| `1` | **M1** | Mononuclear cell |
| `2` | **M2** | Binuclear cell |
| `3` | **M3** | Trinuclear cell |
| `4` | **M4** | Tetranuclear cell |
| `5` | **NEC** | Necrosis |
| `6` | **AP** | Apoptosis |
| `7` | **IDNC** | Indistinguishable/Undefined |

### 2. Damage Counting Mode
**Goal:** Quantify genotoxicity markers.  
**Limit:** Stops automatically at **1000** Binucleated cells (BN).

| Key | Event Code | Biological Description |
|:---:|:----------:|:-----------------------|
| `Q` | **BN** | Binucleated cell (Reference) |
| `W` | **MN** | Micronucleus |
| `E` | **NBUD** | Nuclear Bud |
| `R` | **NPB** | Nucleoplasmic Bridge |

**Global Hotkeys:**
* `TAB`: Display current count summary.
* `ESC`: Abort current session and return to menu.

---

## Project Structure

The application maintains a simple directory structure for ease of use and portability.
