"""
Aufgabe 9: Kettenlinie – Länge einer elektrischen Leitung
Zwei gleich hohe Masten, Abstand w = 100 m, Durchhang = 10 m.

Kettenlinie: y(x) = a * cosh(x / a) - a + y0
Randbedingung: y(50) = y0 + 10
  -->  a * cosh(50/a) - a + y0 = y0 + 10
  -->  f(a) = a * cosh(50/a) - a - 10 = 0    (Nullstellenproblem!)

Leitungslänge: l = 2a * sinh(w / (2a)) = 2a * sinh(50/a)
"""

import sys
import math
from typing import Tuple, List

from Aufgabe5 import solver, bisect
from Aufgabe6 import solver2, regula_falsi
from Aufgabe7 import plotter

sys.stdout.reconfigure(encoding="utf-8")


def catenary_func(a: float) -> float:
    """
    Nullstellenfunktion für den Krümmungsradius a der Kettenlinie.

    Aus der Randbedingung y(50) = y0 + 10 folgt:
        f(a) = a * cosh(50/a) - a - 10 = 0

    Args:
        a: Krümmungsradius des Seils am Scheitelpunkt (a > 0).

    Returns:
        Funktionswert f(a).
    """
    return a * math.cosh(50.0 / a) - a - 10.0


def compute_cable_length(a: float) -> float:
    """
    Berechnet die Leitungslänge l = 2a * sinh(50/a).

    Args:
        a: Krümmungsradius (Ergebnis der Nullstellensuche).

    Returns:
        Länge der Leitung in Metern.
    """
    return 2.0 * a * math.sinh(50.0 / a)


def solve_catenary() -> None:
    """
    Berechnet Krümmungsradius a und Leitungslänge l mit Bisektion und Regula Falsi.

    Sinnvolles Startintervall [50, 1000]:
      f(50)   = 50*cosh(1) - 50 - 10  ≈ +17.2  (positiv)
      f(1000) = 1000*cosh(0.05) - 1000 - 10 ≈ -8.7 (negativ)
      --> Vorzeichenwechsel vorhanden.
    """
    print("=" * 65)
    print("Aufgabe 9: Kettenlinie – Leitungslänge")
    print("=" * 65)
    print("Gegeben:  Mastabstand w = 100 m,  Durchhang = 10 m")
    print("Gesucht:  Krümmungsradius a  und  Leitungslänge l")
    print()
    print("Nullstellenproblem: f(a) = a*cosh(50/a) - a - 10 = 0")

    a_left: float = 50.0
    a_right: float = 1000.0

    print(f"\nStartintervall [{a_left}, {a_right}]:")
    print(f"  f({a_left})    = {catenary_func(a_left):.4f}")
    print(f"  f({a_right}) = {catenary_func(a_right):.4f}")
    print()

    # --- Bisektion ---
    try:
        a_bisect: float
        iters_b: int
        history_b: List[Tuple[float, float]]
        a_bisect, iters_b, history_b = bisect(catenary_func, a_left, a_right)
        l_bisect: float = compute_cable_length(a_bisect)

        print("[Bisektion]")
        print(f"  Krümmungsradius a = {a_bisect:.6f} m")
        print(f"  Leitungslänge   l = {l_bisect:.6f} m")
        print(f"  Iterationen       = {iters_b}")

    except (ValueError, RuntimeError) as e:
        print(f"Fehler Bisektion: {e}")

    print()

    # --- Regula Falsi ---
    try:
        a_rf: float
        iters_rf: int
        history_rf: List[Tuple[float, float]]
        a_rf, iters_rf, history_rf = regula_falsi(catenary_func, a_left, a_right)
        l_rf: float = compute_cable_length(a_rf)

        print("[Regula Falsi]")
        print(f"  Krümmungsradius a = {a_rf:.6f} m")
        print(f"  Leitungslänge   l = {l_rf:.6f} m")
        print(f"  Iterationen       = {iters_rf}")

    except (ValueError, RuntimeError) as e:
        print(f"Fehler Regula Falsi: {e}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    solver()
    solver2()
    plotter()
    solve_catenary()
