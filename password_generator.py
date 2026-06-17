#!/usr/bin/env python3
"""
Password Generator
==================
A secure, feature-rich password generator using cryptographically
safe randomness (secrets module) with CLI support, passphrase mode,
entropy calculation, clipboard copy, and file export.
"""

import secrets
import string
import argparse
import math
import sys
import os

# ---------------------------------------------------------------------------
# Optional dependencies — degrade gracefully if not installed
# ---------------------------------------------------------------------------
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Stub so the rest of the code works without colorama
    class _NoColor:
        def __getattr__(self, _): return ''
    Fore = Style = _NoColor()

# ---------------------------------------------------------------------------
# Word list for passphrase mode (EFF short wordlist subset — 200 common words)
# ---------------------------------------------------------------------------
WORDLIST = [
    "apple", "brave", "cabin", "dance", "eagle", "flame", "grape", "happy",
    "ivory", "jolly", "karma", "lemon", "mango", "noble", "ocean", "piano",
    "queen", "river", "solar", "tiger", "ultra", "vivid", "waltz", "xenon",
    "yacht", "zebra", "amber", "blaze", "cedar", "delta", "ember", "frost",
    "gloom", "haven", "indie", "jewel", "knack", "lunar", "maple", "ninja",
    "olive", "pixel", "quirk", "rapid", "stone", "tower", "unity", "venom",
    "whirl", "pixel", "acorn", "bison", "coast", "drift", "epoch", "fjord",
    "glyph", "hinge", "inlet", "joust", "kiosk", "latch", "metal", "nymph",
    "orbit", "prism", "quilt", "raven", "scout", "talon", "untie", "vapor",
    "weave", "xylem", "yearn", "zesty", "agent", "blunt", "chime", "depot",
    "elbow", "flint", "guava", "helix", "igloo", "juicy", "kinky", "llama",
    "mirth", "notch", "optic", "plumb", "quota", "risky", "slick", "thyme",
    "udder", "vigor", "windy", "xeric", "young", "zonal", "adept", "bliss",
    "craft", "debug", "elite", "foggy", "giant", "humid", "irony", "jumpy",
    "kitty", "lusty", "misty", "novel", "oaken", "plush", "quest", "ridge",
    "swamp", "trove", "unzip", "vault", "witch", "xerox", "yield", "zilch",
    "agile", "boxer", "climb", "dirty", "elope", "fixed", "glare", "hornet",
    "input", "jazzy", "kebab", "lofty", "moose", "north", "outdo", "pivot",
    "qualm", "rocky", "swept", "tutor", "unwed", "vista", "woken", "xylem",
    "yodel", "zippy", "abbot", "brisk", "crisp", "dizzy", "exact", "fairy",
    "gruff", "holly", "ideal", "joker", "kneel", "light", "mulch", "nutty",
    "ovoid", "plank", "quiet", "ruddy", "sugar", "torch", "urban", "valve",
    "wider", "xenon", "yummy", "zappy", "alkyd", "burnt", "canon", "dowry",
    "equip", "fluke", "glint", "hazel", "infer", "jelly", "koala", "lyric",
]

# ---------------------------------------------------------------------------
# Character sets
# ---------------------------------------------------------------------------
LOWERCASE = string.ascii_lowercase          # a-z
UPPERCASE = string.ascii_uppercase          # A-Z
DIGITS    = string.digits                   # 0-9
SYMBOLS   = '!@#$%^&*().,?-_=+[]{}|;:<>'  # common symbols


def build_charset(use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
    """Build the character pool from selected categories."""
    pool = ''
    if use_lower:   pool += LOWERCASE
    if use_upper:   pool += UPPERCASE
    if use_digits:  pool += DIGITS
    if use_symbols: pool += SYMBOLS
    if not pool:
        print(Fore.RED + "Error: at least one character set must be selected.")
        sys.exit(1)
    return pool


def enforce_requirements(password, use_lower, use_upper, use_digits, use_symbols):
    """
    Guarantee the password contains at least one character from each
    enabled category. Replaces random positions to avoid bias.
    """
    pwd = list(password)
    required = []
    if use_lower:   required.append(secrets.choice(LOWERCASE))
    if use_upper:   required.append(secrets.choice(UPPERCASE))
    if use_digits:  required.append(secrets.choice(DIGITS))
    if use_symbols: required.append(secrets.choice(SYMBOLS))

    # Randomly place required chars at distinct positions
    positions = secrets.SystemRandom().sample(range(len(pwd)), len(required))
    for pos, char in zip(positions, required):
        pwd[pos] = char

    # Shuffle to avoid predictable positions
    secrets.SystemRandom().shuffle(pwd)
    return ''.join(pwd)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def generate_password(length=16, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=True):
    """Generate a single cryptographically secure random password."""
    charset = build_charset(use_lower, use_upper, use_digits, use_symbols)
    pwd = ''.join(secrets.choice(charset) for _ in range(length))
    # Enforce at least one character from each enabled set
    pwd = enforce_requirements(pwd, use_lower, use_upper, use_digits, use_symbols)
    return pwd


def generate_passphrase(words=4, separator='-'):
    """Generate a memorable passphrase using random words."""
    chosen = [secrets.choice(WORDLIST) for _ in range(words)]
    return separator.join(chosen)


# ---------------------------------------------------------------------------
# Entropy / strength
# ---------------------------------------------------------------------------

def calculate_entropy(password):
    """Shannon-like entropy: log2(charset_size ^ length)."""
    charset_size = len(set(password))
    if charset_size < 2:
        return 0.0
    return len(password) * math.log2(charset_size)


def strength_label(entropy):
    """Map entropy (bits) to a human-readable strength label."""
    if entropy < 28:
        return Fore.RED    + "Very Weak  ▓░░░░"
    elif entropy < 36:
        return Fore.RED    + "Weak       ▓▓░░░"
    elif entropy < 60:
        return Fore.YELLOW + "Fair       ▓▓▓░░"
    elif entropy < 80:
        return Fore.GREEN  + "Strong     ▓▓▓▓░"
    else:
        return Fore.GREEN  + Style.BRIGHT + "Very Strong▓▓▓▓▓"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_header():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════╗
║      Password Generator      ║
║   Secure · Fast · Flexible   ║
╚══════════════════════════════╝
""")


def print_password(pwd, index=None, show_entropy=True):
    """Print a password with optional index and entropy info."""
    prefix = f"  {Fore.YELLOW}{index:>2}.{Style.RESET_ALL} " if index is not None else "  "
    print(prefix + Fore.WHITE + Style.BRIGHT + pwd)
    if show_entropy:
        entropy = calculate_entropy(pwd)
        label = strength_label(entropy)
        print(f"      {Style.DIM}entropy: {entropy:.1f} bits  strength: {Style.RESET_ALL}{label}{Style.RESET_ALL}")


# ---------------------------------------------------------------------------
# Clipboard / export
# ---------------------------------------------------------------------------

def copy_to_clipboard(text):
    if not CLIPBOARD_AVAILABLE:
        print(Fore.YELLOW + "  ⚠  pyperclip not installed — clipboard unavailable.")
        print(Fore.YELLOW + "     Install with: pip install pyperclip")
        return
    try:
        pyperclip.copy(text)
        print(Fore.GREEN + "  ✔  Copied to clipboard!")
    except Exception as e:
        print(Fore.RED + f"  ✘  Clipboard error: {e}")


def export_to_file(passwords, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(passwords) + '\n')
        print(Fore.GREEN + f"\n  ✔  Passwords saved to: {filepath}")
    except OSError as e:
        print(Fore.RED + f"\n  ✘  Could not write file: {e}")


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

def ask(prompt, default=None, cast=str, valid=None):
    """Prompt the user for input with an optional default value."""
    hint = f" [{default}]" if default is not None else ""
    while True:
        raw = input(Fore.CYAN + f"  {prompt}{hint}: " + Style.RESET_ALL).strip()
        value = raw if raw else str(default)
        try:
            result = cast(value)
        except (ValueError, TypeError):
            print(Fore.RED + f"  Invalid input — expected {cast.__name__}.")
            continue
        if valid and result not in valid:
            print(Fore.RED + f"  Choose one of: {valid}")
            continue
        return result


def ask_bool(prompt, default=True):
    hint = "Y/n" if default else "y/N"
    raw = input(Fore.CYAN + f"  {prompt} [{hint}]: " + Style.RESET_ALL).strip().lower()
    if not raw:
        return default
    return raw in ('y', 'yes', '1', 'true')


def interactive_mode():
    print_header()

    mode = ask("Mode: (p)assword or (P)assphrase", default='p',
               valid=['p', 'P', 'password', 'passphrase'])
    passphrase_mode = mode.lower().startswith('p') and mode == 'P' or mode == 'passphrase'

    if passphrase_mode:
        words   = ask("Number of words per passphrase", default=4, cast=int)
        sep     = ask("Word separator", default='-')
        count   = ask("How many passphrases?", default=1, cast=int)
        entropy = ask_bool("Show entropy?", default=True)
        clip    = ask_bool("Copy first passphrase to clipboard?", default=False)
        outfile = ask("Save to file? (leave blank to skip)", default='')

        print(Fore.CYAN + "\n  Your passphrases:\n")
        results = []
        for i in range(1, count + 1):
            pwd = generate_passphrase(words, sep)
            print_password(pwd, index=i, show_entropy=entropy)
            results.append(pwd)

        if clip:
            copy_to_clipboard(results[0])
        if outfile:
            export_to_file(results, outfile)

    else:
        length  = ask("Password length", default=16, cast=int)
        if length < 4:
            print(Fore.RED + "  Minimum length is 4. Setting to 4.")
            length = 4

        count   = ask("How many passwords?", default=1, cast=int)
        lower   = ask_bool("Include lowercase (a-z)?", default=True)
        upper   = ask_bool("Include uppercase (A-Z)?", default=True)
        digits  = ask_bool("Include digits (0-9)?",    default=True)
        symbols = ask_bool("Include symbols (!@#...)?", default=True)
        entropy = ask_bool("Show entropy/strength?",    default=True)
        clip    = ask_bool("Copy first password to clipboard?", default=False)
        outfile = ask("Save to file? (leave blank to skip)", default='')

        print(Fore.CYAN + "\n  Your passwords:\n")
        results = []
        for i in range(1, count + 1):
            pwd = generate_password(length, lower, upper, digits, symbols)
            print_password(pwd, index=i, show_entropy=entropy)
            results.append(pwd)

        if clip:
            copy_to_clipboard(results[0])
        if outfile:
            export_to_file(results, outfile)

    print(Fore.CYAN + "\n  Done. Stay safe! 🔒\n")


# ---------------------------------------------------------------------------
# CLI (argparse) mode
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog='password_generator',
        description='Secure password / passphrase generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 password_generator.py                    # interactive mode
  python3 password_generator.py -n 5 -l 20         # 5 passwords, length 20
  python3 password_generator.py -l 32 --no-symbols # no special characters
  python3 password_generator.py --passphrase -w 5  # 5-word passphrase
  python3 password_generator.py -n 3 -c -o pw.txt  # copy + save to file
        """
    )

    parser.add_argument('-n', '--count',      type=int, default=1,
                        help='Number of passwords to generate (default: 1)')
    parser.add_argument('-l', '--length',     type=int, default=16,
                        help='Password length (default: 16)')
    parser.add_argument('--no-lower',         action='store_true',
                        help='Exclude lowercase letters')
    parser.add_argument('--no-upper',         action='store_true',
                        help='Exclude uppercase letters')
    parser.add_argument('--no-digits',        action='store_true',
                        help='Exclude digits')
    parser.add_argument('--no-symbols',       action='store_true',
                        help='Exclude symbols')
    parser.add_argument('--passphrase',       action='store_true',
                        help='Generate a memorable passphrase instead')
    parser.add_argument('-w', '--words',      type=int, default=4,
                        help='Words per passphrase (default: 4)')
    parser.add_argument('-s', '--separator',  default='-',
                        help='Passphrase word separator (default: -)')
    parser.add_argument('-c', '--clipboard',  action='store_true',
                        help='Copy first result to clipboard')
    parser.add_argument('-o', '--output',     metavar='FILE',
                        help='Save all results to a text file')
    parser.add_argument('--no-entropy',       action='store_true',
                        help='Hide entropy / strength display')
    return parser


def cli_mode(args):
    print_header()
    show_entropy = not args.no_entropy
    results = []

    if args.passphrase:
        print(Fore.CYAN + f"  Generating {args.count} passphrase(s):\n")
        for i in range(1, args.count + 1):
            pwd = generate_passphrase(args.words, args.separator)
            print_password(pwd, index=i, show_entropy=show_entropy)
            results.append(pwd)
    else:
        if args.length < 4:
            print(Fore.RED + "  Minimum length is 4. Setting to 4.")
            args.length = 4
        print(Fore.CYAN + f"  Generating {args.count} password(s) (length={args.length}):\n")
        for i in range(1, args.count + 1):
            pwd = generate_password(
                length=args.length,
                use_lower=not args.no_lower,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
            )
            print_password(pwd, index=i, show_entropy=show_entropy)
            results.append(pwd)

    if args.clipboard:
        copy_to_clipboard(results[0])
    if args.output:
        export_to_file(results, args.output)

    print(Fore.CYAN + "\n  Done. Stay safe! 🔒\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()

    # No arguments → interactive mode
    if len(sys.argv) == 1:
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n  Interrupted. Goodbye!")
            sys.exit(0)
    else:
        args = parser.parse_args()
        cli_mode(args)


if __name__ == '__main__':
    main()
