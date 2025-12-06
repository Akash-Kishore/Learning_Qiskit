import nbformat
from nbformat import ValidationError

src = "ImplementingCircuits.ipynb"
dst = "ImplementingCircuits_fixed.ipynb"

try:
    # Try reading normally
    nb = nbformat.read(src, as_version=4)
    nbformat.validate(nb)
    nbformat.write(nb, dst)
    print("Valid notebook saved to:", dst)

except Exception as e:
    print("Standard read failed:", e)
    print("Attempting recovery by trimming invalid text...")

    # Load raw text
    text = open(src, "r", encoding="utf-8", errors="replace").read()

    # Find first { and last } (best-guess JSON recovery)
    first = text.find("{")
    last = text.rfind("}")

    if first != -1 and last != -1 and last > first:
        candidate = text[first:last+1]

        try:
            nb = nbformat.reads(candidate, as_version=4)
            nbformat.write(nb, dst)
            print("Recovered notebook saved to:", dst)
        except Exception as e2:
            print("Recovery failed:", e2)
    else:
        print("Could not locate valid JSON braces in the notebook.")
