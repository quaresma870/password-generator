# 🔐 Password Generator

A secure, feature-rich command-line password and passphrase generator written in Python.

Uses the `secrets` module for **cryptographically secure** randomness — safe for real passwords.

---

## Run online (no install needed)

| Platform | Link |
|----------|------|
| 🚀 **Binder** — interactive notebook in the browser | [![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/quaresma870/password-generator/HEAD?labpath=password_generator.ipynb) |
| 💻 **Codespaces** — full VS Code environment | [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/quaresma870/password-generator) |
| 🐍 **Python version** | ![Python](https://img.shields.io/badge/python-3.6%2B-blue?logo=python&logoColor=white) |

### Binder
Click the **Launch Binder** badge above. A Jupyter Notebook opens in the browser — no account required. Run each cell with `Shift+Enter` or click **Run All**.

> First launch takes ~1 minute while the environment builds. Subsequent launches are faster.

### Codespaces
Click the **Open in Codespaces** badge (requires a GitHub account). A full VS Code opens in the browser with a terminal ready to use:

```bash
pip install colorama pyperclip
python3 password_generator.py
```

---

## CI / GitHub Actions

Every push triggers a demo run that generates sample passwords and uploads them as an artifact.

[![Password Generator Demo](https://github.com/quaresma870/password-generator/actions/workflows/demo.yml/badge.svg)](https://github.com/quaresma870/password-generator/actions/workflows/demo.yml)

You can also trigger it manually with custom parameters:

1. Go to **Actions → Password Generator Demo → Run workflow**
2. Fill in: count, length, mode (password or passphrase)
3. Click **Run workflow** — results appear in the logs and as a downloadable artifact

---

## Features

- ✅ Cryptographically secure (`secrets` module, not `random`)
- ✅ Configurable character sets (lowercase, uppercase, digits, symbols)
- ✅ Guaranteed character policy — every enabled category always appears
- ✅ Passphrase mode (e.g. `horse-river-amber-frost`)
- ✅ Entropy calculation and strength indicator
- ✅ Clipboard copy (`pyperclip`)
- ✅ Export to file
- ✅ Interactive mode (no arguments needed)
- ✅ Full CLI with `argparse`
- ✅ Coloured output (`colorama`)
- ✅ Input validation — never crashes on bad input

---

## Local installation

```bash
git clone https://github.com/quaresma870/password-generator.git
cd password-generator
pip install colorama pyperclip   # optional but recommended
```

Python 3.6+ required. No mandatory dependencies.

---

## Usage

### Interactive mode

```bash
python3 password_generator.py
```

### CLI mode

```
python3 password_generator.py [OPTIONS]
```

| Option              | Default | Description                              |
|---------------------|---------|------------------------------------------|
| `-n, --count`       | `1`     | Number of passwords to generate          |
| `-l, --length`      | `16`    | Password length                          |
| `--no-lower`        | off     | Exclude lowercase letters (a–z)          |
| `--no-upper`        | off     | Exclude uppercase letters (A–Z)          |
| `--no-digits`       | off     | Exclude digits (0–9)                     |
| `--no-symbols`      | off     | Exclude symbols (`!@#$%...`)             |
| `--passphrase`      | off     | Generate passphrase instead of password  |
| `-w, --words`       | `4`     | Words per passphrase                     |
| `-s, --separator`   | `-`     | Word separator for passphrase            |
| `-c, --clipboard`   | off     | Copy first result to clipboard           |
| `-o, --output FILE` | —       | Save all results to a text file          |
| `--no-entropy`      | off     | Hide entropy / strength display          |

### Examples

```bash
# 5 passwords, 20 characters each
python3 password_generator.py -n 5 -l 20

# 32-char password, no symbols (e.g. for APIs)
python3 password_generator.py -l 32 --no-symbols

# 5-word passphrase with underscore separator
python3 password_generator.py --passphrase -w 5 -s _

# 3 passwords, copy first to clipboard, save all to file
python3 password_generator.py -n 3 -c -o passwords.txt

# Only digits and uppercase (PIN-style)
python3 password_generator.py --no-lower --no-symbols -l 8
```

---

## Entropy & Strength

```
  1. kR#9mP!xZq@2vLnT
     entropy: 102.4 bits  strength: Very Strong ▓▓▓▓▓
```

| Entropy      | Strength    |
|--------------|-------------|
| < 28 bits    | Very Weak   |
| 28–35 bits   | Weak        |
| 36–59 bits   | Fair        |
| 60–79 bits   | Strong      |
| 80+ bits     | Very Strong |

---

## Project structure

```
password-generator/
├── password_generator.py          # Main script
├── password_generator.ipynb       # Jupyter Notebook (Binder)
├── .github/
│   └── workflows/
│       └── demo.yml               # GitHub Actions workflow
├── requirements.txt
└── README.md
```

---

## Security notes

- Uses Python's `secrets` module backed by the OS CSPRNG (`/dev/urandom` on Linux/macOS, `CryptGenRandom` on Windows)
- Passwords are never stored beyond the session unless explicitly exported
- Word list is embedded — no external file dependency
- Minimum length of 4 enforced to satisfy character-set requirements

---

## License

MIT — free to use, modify, and distribute.
