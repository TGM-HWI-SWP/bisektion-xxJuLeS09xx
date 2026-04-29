"""
Aufgabe 6: Regula Falsi (Methode der falschen Position)
Alternative zum Bisektionsverfahren aus Aufgabe 5.

Anstatt den Mittelpunkt des Intervalls zu nehmen, wird eine Sekante durch
die Punkte (a, f(a)) und (b, f(b)) gelegt und deren Nullstelle als neue
Intervallgrenze verwendet:
    c = b - f(b) * (b - a) / (f(b) - f(a))
"""

import sys
import math
from typing import Callable, Tuple, List

from Aufgabe5 import sqrt_func

sys.stdout.reconfigure(encoding="utf-8")


def regula_falsi(
    func: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float = 1e-10,
    max_iter: int = 1000
) -> Tuple[float, int, List[Tuple[float, float]]]:
    """
    Regula-Falsi-Verfahren zur Nullstellenfindung in [a, b].

    Verwendet die Sekanten-Formel: c = b - f(b) * (b-a) / (f(b) - f(a))
    um die Nullstelle schneller zu nähern als bei der reinen Bisektion.

    Args:
        func:      Stetige Funktion f(x) mit Nullstelle in [a, b].
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
        ValueError:   Wenn f(a)*f(b) >= 0 oder Division durch Null auftritt.
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
            f"f({b})={fb:.6f} haben gleiches Vorzeichen."
        )

    history: List[Tuple[float, float]] = []
    c: float = b

    for i in range(max_iter):
        denom: float = fb - fa
        if abs(denom) < 1e-15:
            raise ValueError(
                "Division durch Null: f(b) - f(a) ist nahezu 0. "
                "Sekante ist (fast) horizontal."
            )

        # Sekantenschnittpunkt als neue Intervallgrenze
        c = b - fb * (b - a) / denom
        fc: float = func(c)
        history.append((c, abs(fc)))

        if abs(fc) < epsilon:
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


def solver2() -> None:
    """
    Demonstriert das Regula-Falsi-Verfahren mit der Wurzelfunktion.

    Testet n = 25, 81 und 144. Vergleicht die numerische Näherung
    mit der analytischen Lösung math.sqrt(n).
    """
    print("=" * 65)
    print("Aufgabe 6: Regula Falsi  –  Wurzelfunktions-Test")
    print("=" * 65)

    test_cases: List[Tuple[float, float, float]] = [
        (25,  0.0,  25.0),
        (81,  0.0,  81.0),
        (144, 0.0, 144.0),
    ]

    for n, a, b in test_cases:
        try:
            func = sqrt_func(n)
            root, iterations, _ = regula_falsi(func, a, b)
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
    solver2()
