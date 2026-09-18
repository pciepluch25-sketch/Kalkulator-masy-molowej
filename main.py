import tkinter as tk
from tkinter import ttk, messagebox

# Standard atomic weights (approximate values).
ATOMIC_MASSES = {
    "H": 1.008, "He": 4.003, "Li": 6.94, "Be": 9.012, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98, "Ru": 101.07, "Rh": 102.906,
    "Pd": 106.42, "Ag": 107.868, "Cd": 112.414, "In": 114.818, "Sn": 118.710,
    "Sb": 121.760, "Te": 127.60, "I": 126.904, "Xe": 131.293, "Cs": 132.905,
    "Ba": 137.327, "La": 138.905, "Ce": 140.116, "Pr": 140.908, "Nd": 144.242,
    "Pm": 145, "Sm": 150.36, "Eu": 151.964, "Gd": 157.25, "Tb": 158.925,
    "Dy": 162.500, "Ho": 164.930, "Er": 167.259, "Tm": 168.934, "Yb": 173.045,
    "Lu": 174.967, "Hf": 178.49, "Ta": 180.948, "W": 183.84, "Re": 186.207,
    "Os": 190.23, "Ir": 192.217, "Pt": 195.084, "Au": 196.967, "Hg": 200.592,
    "Tl": 204.383, "Pb": 207.2, "Bi": 208.980, "Po": 209, "At": 210,
    "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.038,
    "Pa": 231.036, "U": 238.029, "Np": 237, "Pu": 244, "Am": 243,
    "Cm": 247, "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257, "Md": 258,
    "No": 259, "Lr": 266, "Rf": 267, "Db": 268, "Sg": 269, "Bh": 270,
    "Hs": 277, "Mt": 278, "Ds": 281, "Rg": 282, "Cn": 285, "Nh": 286,
    "Fl": 289, "Mc": 290, "Lv": 293, "Ts": 294, "Og": 294
}


def parse_formula(formula):
    formula = formula.strip()
    if not formula:
        raise ValueError("Podaj wzór chemiczny.")

    pos = 0

    def read_number():
        nonlocal pos
        start = pos
        while pos < len(formula) and formula[pos].isdigit():
            pos += 1

        if start == pos:
            return 1

        number = int(formula[start:pos])
        if number <= 0:
            raise ValueError("Liczba we wzorze musi być większa od 0.")
        return number

    def merge(target, source, multiplier=1):
        for element, count in source.items():
            target[element] = target.get(element, 0) + count * multiplier

    def read_group(expect_closing=False):
        nonlocal pos
        atoms = {}

        while pos < len(formula):
            char = formula[pos]

            if char == ")":
                if not expect_closing:
                    raise ValueError("Nieoczekiwany znak ')'.")
                pos += 1
                return atoms

            if char == "(":
                pos += 1
                group = read_group(True)
                multiplier = read_number()
                merge(atoms, group, multiplier)
                continue

            if char.isupper():
                symbol = char
                pos += 1

                if pos < len(formula) and formula[pos].islower():
                    symbol += formula[pos]
                    pos += 1

                if symbol not in ATOMIC_MASSES:
                    raise ValueError(f"Nieznany symbol pierwiastka: {symbol}")

                count = read_number()
                atoms[symbol] = atoms.get(symbol, 0) + count
                continue

            raise ValueError(f"Nieprawidłowy znak '{char}' w pozycji {pos + 1}.")

        if expect_closing:
            raise ValueError("Brakuje zamykającego nawiasu ')'.")

        return atoms

    result = read_group(False)

    if pos != len(formula):
        raise ValueError("Nieprawidłowy wzór chemiczny.")

    return result


def calculate_molar_mass(formula):
    composition = parse_formula(formula)
    total = sum(ATOMIC_MASSES[element] * count for element, count in composition.items())
    return total, composition


def calculate():
    formula = formula_entry.get().strip()

    try:
        mass, composition = calculate_molar_mass(formula)

        result_label.config(text=f"{mass:.3f} g/mol")

        for item in table.get_children():
            table.delete(item)

        for element, count in composition.items():
            contribution = ATOMIC_MASSES[element] * count
            table.insert(
                "",
                "end",
                values=(element, count, f"{ATOMIC_MASSES[element]:.3f}", f"{contribution:.3f}")
            )

    except ValueError as error:
        messagebox.showerror("Błąd", str(error))


def clear():
    formula_entry.delete(0, tk.END)
    result_label.config(text="—")
    for item in table.get_children():
        table.delete(item)


def set_example(formula):
    formula_entry.delete(0, tk.END)
    formula_entry.insert(0, formula)
    calculate()


window = tk.Tk()
window.title("Kalkulator masy molowej")
window.geometry("720x560")
window.minsize(650, 500)

title = tk.Label(
    window,
    text="KALKULATOR MASY MOLOWEJ",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    window,
    text="Python + Tkinter • 118 pierwiastków • obsługa nawiasów",
    font=("Segoe UI", 10)
)
subtitle.pack(pady=(0, 15))

input_frame = tk.Frame(window)
input_frame.pack()

tk.Label(
    input_frame,
    text="Wzór chemiczny:",
    font=("Segoe UI", 11)
).grid(row=0, column=0, padx=5)

formula_entry = tk.Entry(
    input_frame,
    width=28,
    font=("Segoe UI", 14)
)
formula_entry.grid(row=0, column=1, padx=5)
formula_entry.focus()

calculate_button = tk.Button(
    input_frame,
    text="OBLICZ",
    font=("Segoe UI", 10, "bold"),
    command=calculate,
    width=10
)
calculate_button.grid(row=0, column=2, padx=5)

result_label = tk.Label(
    window,
    text="—",
    font=("Segoe UI", 24, "bold")
)
result_label.pack(pady=15)

examples_frame = tk.Frame(window)
examples_frame.pack(pady=5)

tk.Label(
    examples_frame,
    text="Przykłady:",
    font=("Segoe UI", 10, "bold")
).pack(side=tk.LEFT, padx=5)

for formula in ("H2O", "CO2", "H2SO4", "Ca(OH)2", "Al2(SO4)3"):
    tk.Button(
        examples_frame,
        text=formula,
        command=lambda f=formula: set_example(f)
    ).pack(side=tk.LEFT, padx=3)

columns = ("element", "count", "mass", "contribution")

table = ttk.Treeview(
    window,
    columns=columns,
    show="headings",
    height=12
)

table.heading("element", text="Pierwiastek")
table.heading("count", text="Liczba atomów")
table.heading("mass", text="Masa atomowa")
table.heading("contribution", text="Wkład [g/mol]")

table.column("element", width=120, anchor="center")
table.column("count", width=140, anchor="center")
table.column("mass", width=140, anchor="center")
table.column("contribution", width=160, anchor="center")

table.pack(fill="both", expand=True, padx=25, pady=15)

buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=(0, 15))

tk.Button(
    buttons_frame,
    text="WYCZYŚĆ",
    command=clear,
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    buttons_frame,
    text="ZAMKNIJ",
    command=window.destroy,
    width=12
).pack(side=tk.LEFT, padx=5)

formula_entry.bind("<Return>", lambda event: calculate())

window.mainloop()
