# Molar Mass Calculator

A simple desktop GUI application written in **Python** using **Tkinter** for calculating the molar mass of chemical compounds.

## Features

- Supports all 118 chemical elements
- Calculates molar mass in g/mol
- Supports element subscripts, e.g. `H2O`
- Supports parentheses, e.g. `Ca(OH)2`
- Displays the contribution of each element
- Built-in example formulas
- No external Python packages required

## Examples

| Formula | Molar mass |
|---|---:|
| H2O | 18.015 g/mol |
| CO2 | 44.009 g/mol |
| H2SO4 | 98.072 g/mol |
| Ca(OH)2 | 74.092 g/mol |
| Al2(SO4)3 | 342.132 g/mol |

## Requirements

- Python 3.10 or newer
- Tkinter (normally included with standard Python installations)

## Running the program

Clone or download the repository, then run:

```bash
python main.py
```

On Windows, if `python` does not work, try:

```bash
py main.py
```

## Supported formula syntax

Examples:

```text
H2O
CO2
NaCl
H2SO4
Ca(OH)2
Al2(SO4)3
Fe2(SO4)3
NH4NO3
```

The calculator validates brackets and element symbols and reports invalid formulas.

## Project structure

```text
molar-mass-calculator/
├── main.py
├── README.md
├── LICENSE
└── .gitignore
```

## Technology

- Python
- Tkinter
- Standard library only

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
