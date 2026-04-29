"""
Aufgabe 5: Bisektions-SOLVER
Numerisches Lösen von Nullstellen-Problemen mittels Intervallhalbierung.
"""

import sys
import math
from typing import Callable, Tuple, List

sys.stdout.reconfigure(encoding="utf-8")


def bisect(
    func: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float = 1e-10,
    max_iter: int = 1000
) -> Tuple[float, int, List[Tuple[float, float]]]:
    """
    Bisektionsverfahren zur Nullstellenfindung einer stetigen Funktion in [a, b].

    Das Intervall [a, b] wird solange halbiert, bis die gewünschte Genauigkeit
    epsilon erreicht ist. Voraussetzung: f(a) * f(b) < 0 (Zwischenwertsatz).

    Args:
        func:      Stetige Funktion f(x), die eine Nullstelle in [a, b] hat.
        a:         Linke Intervallgrenze.
        b:         Rechte Intervallgrenze.
        epsilon:   Gewünschte Genauigkeit (Abbruchkriterium).
        max_iter:  Maximale Anzahl an Iterationen.

    Returns:
        Tuple bestehend aus:
          - Nullstellennäherung (float)
          - Anzahl benötigter Iterationen (int)
          - Verlauf als Liste von (c, |f(c)|) pro Iterationsschritt (List)

    Raises:
        ValueError:   Wenn f(a) * f(b) >= 0, also kein Vorzeichenwechsel.
        RuntimeError: Wenn max_iter überschritten wird.
    """
    try:
        fa: float = func(a)
        fb: float = func(b)
    except Exception as e:
        raise ValueError(f"Fehler bei der Funktionsauswertung: {e}")

    if fa * fb >= 0:
        raise ValueError(
            f"Zwischenwertsatz nicht erfüllt: f({a})={fa:.6f} und "
            f"f({b})={fb:.6f} haben gleiches Vorzeichen. "
            "Keine Nullstelle im Intervall garantiert."
        )

    history: List[Tuple[float, float]] = []
    c: float = a

    for i in range(max_iter):
        c = (a + b) / 2.0        # Mittelpunkt des Intervalls
        fc: float = func(c)
        history.append((c, abs(fc)))

        # Abbruch wenn Funktionswert oder Intervallbreite klein genug
        if abs(fc) < epsilon or (b - a) / 2.0 < epsilon:
            return c, i + 1, history

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    raise RuntimeError(
        f"Maximale Iterationszahl ({max_iter}) erreicht. "
        f"Letzter Näherungswert: {c:.10f}"
    )


def sqrt_func(n: float) -> Callable[[float], float]:
    """
    Erstellt die Nullstellenfunktion f(x) = x^2 - n für die Wurzelberechnung.

    Gesucht ist x mit x^2 = n, also die Nullstelle von f(x) = x^2 - n.

    Args:
        n: Der Radikand (z.B. n=25 für sqrt(25)=5).

    Returns:
        Callable: Die Funktion f(x) = x^2 - n.
    """
    return lambda x: x ** 2 - n


def solver() -> None:
    """
    Demonstriert den Bisektions-SOLVER mit der Wurzelfunktion.

    Testet n = 25, 81 und 144. Vergleicht die numerische Näherung
    mit der analytischen Lösung math.sqrt(n).
    """
    print("=" * 65)
    print("Aufgabe 5: Bisektions-SOLVER  –  Wurzelfunktions-Test")
    print("=" * 65)

    # (n, a, b): Intervall [a, b] mit f(a)*f(b) < 0
    test_cases: List[Tuple[float, float, float]] = [
        (25,  0.0,  25.0),
        (81,  0.0,  81.0),
        (144, 0.0, 144.0),
    ]

    for n, a, b in test_cases:
        try:
            func = sqrt_func(n)
            root, iterations, _ = bisect(func, a, b)
            analytical: float = math.sqrt(n)
            error: float = abs(root - analytical)

            print(f"\nsqrt({n:3.0f}):")
            print(f"  Numerisch  = {root:.10f}")
            print(f"  Analytisch = {analytical:.10f}")
            print(f"  Fehler     = {error:.2e}")
            print(f"  Iterationen= {iterations}")

        except (ValueError, RuntimeError) as e:
            print(f"\nFehler für n={n}: {e}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    solver()
