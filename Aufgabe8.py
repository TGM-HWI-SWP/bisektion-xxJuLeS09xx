"""
Aufgabe 8: Polynom P4(x) = 2x + x^2 + 3x^3 - x^4
Nullstellenfindung bei x = 3.4567 und Genauigkeitstests.
"""

import sys
from Aufgabe5 import bisect

sys.stdout.reconfigure(encoding="utf-8")


def p4(x: float) -> float:
    """
    Polynom P4(x) = 2x + x^2 + 3x^3 - x^4.

    Hat Nullstellen bei x = 0 und x ≈ 3.4567.

    Args:
        x: Eingabewert.

    Returns:
        Funktionswert P4(x).
    """
    return 2 * x + x ** 2 + 3 * x ** 3 - x ** 4


def run_aufgabe8() -> None:
    """
    Findet die Nullstelle von P4 bei x ≈ 3.4567 im Intervall [3, 4].
    Führt anschließend Genauigkeitstests für epsilon = 10^-2 und 10^-8 durch.
    """
    print("=" * 65)
    print("Aufgabe 8: Polynom  P4(x) = 2x + x^2 + 3x^3 - x^4")
    print("=" * 65)

    # Intervall [3, 4]: P4(3) > 0, P4(4) < 0 --> Vorzeichenwechsel
    a: float = 3.0
    b: float = 4.0

    print(f"\nPrüfe Intervall [{a}, {b}]:")
    print(f"  P4({a}) = {p4(a):.6f}")
    print(f"  P4({b}) = {p4(b):.6f}")

    try:
        # Standardlösung mit hoher Genauigkeit
        root, iters, _ = bisect(p4, a, b)
        print(f"\nNullstelle: x ≈ {root:.6f}  (erwartet: x ≈ 3.4567)")
        print(f"P4(x)      = {p4(root):.2e}")
        print(f"Iterationen: {iters}")

        # Genauigkeitstests
        print("\nGenauigkeitstests:")
        print(f"  {'epsilon':<12} {'Iterationen':>12} {'x (Näherung)':>18} {'|f(x)|':>12}")
        print("  " + "-" * 56)

        for exp in [-2, -8]:
            epsilon: float = 10.0 ** exp
            root_eps, iters_eps, _ = bisect(p4, a, b, epsilon=epsilon)
            print(
                f"  10^{exp:<8} {iters_eps:>12}    {root_eps:>16.10f}   "
                f"{abs(p4(root_eps)):>12.2e}"
            )

    except (ValueError, RuntimeError) as e:
        print(f"Fehler: {e}")

    print("\n" + "=" * 65)
    print("Interpretation:")
    print("  Für epsilon=10^-2 genügen wenige Iterationen (~7).")
    print("  Für epsilon=10^-8 sind deutlich mehr Iterationen nötig (~27).")
    print("  Pro Iteration halbiert sich das Intervall --> log2-Konvergenz.")


if __name__ == "__main__":
    run_aufgabe8()
