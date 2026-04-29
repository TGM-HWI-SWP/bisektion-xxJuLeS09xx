"""
Aufgabe 7: Grafische Aufbereitung der Nullstellenfindung
Animierte Visualisierung des Bisektions- und Regula-Falsi-Verfahrens
mittels Matplotlib (zwei Subplots in einer Figure).
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, List, Tuple

from Aufgabe5 import bisect, sqrt_func
from Aufgabe6 import regula_falsi

sys.stdout.reconfigure(encoding="utf-8")


def animate_solver(
    history: List[Tuple[float, float]],
    true_root: float,
    title: str,
    pause: float = 0.08
) -> None:
    """
    Animiert die Nullstellenfindung mit zwei Subplots in einem Fenster.

    Subplot 1: Aktuelle Genauigkeit |f(c)| je Iterationsschritt.
               Nähert sich dem Wert 0, da die Nullstelle gesucht wird.
    Subplot 2: Aktuelle Näherung c je Iterationsschritt.
               Zeigt, wie c langsam gegen die Lösung konvergiert.

    Args:
        history:   Liste von (c, |f(c)|) aus dem Solver.
        true_root: Analytische Lösung für den Vergleich.
        title:     Titel der Figure.
        pause:     Pause zwischen zwei Frames in Sekunden.
    """
    steps: List[int] = list(range(1, len(history) + 1))
    c_values: List[float] = [h[0] for h in history]
    accuracy_values: List[float] = [h[1] for h in history]

    # Einmaliges Erstellen der Figure – wird während der Animation aktualisiert
    plt.close("all")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(title, fontsize=13, fontweight="bold")

    for i in range(len(history)):
        # --- Subplot 1: Genauigkeit |f(c)| nähert sich 0 ---
        ax1.cla()
        ax1.semilogy(
            steps[:i + 1], accuracy_values[:i + 1],
            "b-o", markersize=4, linewidth=1.2, label="|f(c)|"
        )
        ax1.set_xlabel("Iterationsschritt")
        ax1.set_ylabel("|f(c)|  (log. Skala)")
        ax1.set_title("Aktuelle Genauigkeit je Iterationsschritt")
        ax1.set_xlim(1, max(len(history), 2))
        ax1.grid(True, which="both", linestyle="--", alpha=0.5)
        ax1.legend(loc="upper right")

        # --- Subplot 2: Näherung c nähert sich der Nullstelle ---
        ax2.cla()
        ax2.plot(
            steps[:i + 1], c_values[:i + 1],
            "r-o", markersize=4, linewidth=1.2, label="Näherung c"
        )
        ax2.axhline(
            y=true_root, color="green", linestyle="--",
            linewidth=1.5, label=f"Lösung = {true_root:.4f}"
        )
        ax2.set_xlabel("Iterationsschritt")
        ax2.set_ylabel("c")
        ax2.set_title("Aktuelle Näherung c je Iterationsschritt")
        ax2.set_xlim(1, max(len(history), 2))
        ax2.legend(loc="upper right")
        ax2.grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        # plt.pause() aktualisiert das Fenster in-place – kein neues Fenster
        plt.pause(pause)

    # Fenster offen halten bis der Nutzer es schließt
    plt.show(block=True)


def plotter() -> None:
    """
    Demonstriert die animierte Visualisierung für Bisektion und Regula Falsi.
    Verwendet die Wurzelfunktion für n = 25 als Beispiel.
    """
    n: float = 25.0
    a: float = 0.0
    b: float = 25.0
    func = sqrt_func(n)
    true_root: float = float(np.sqrt(n))

    # --- Bisektion animieren ---
    try:
        _, _, history_bisect = bisect(func, a, b, epsilon=1e-8)
        print(f"Bisektion für sqrt({n:.0f}): {len(history_bisect)} Iterationen")
        animate_solver(
            history_bisect, true_root,
            title=f"Bisektion  –  sqrt({n:.0f})  (Nullstelle bei x = {true_root:.4f})"
        )
    except (ValueError, RuntimeError) as e:
        print(f"Fehler Bisektion: {e}")

    # --- Regula Falsi animieren ---
    try:
        _, _, history_rf = regula_falsi(func, a, b, epsilon=1e-8)
        print(f"Regula Falsi für sqrt({n:.0f}): {len(history_rf)} Iterationen")
        animate_solver(
            history_rf, true_root,
            title=f"Regula Falsi  –  sqrt({n:.0f})  (Nullstelle bei x = {true_root:.4f})"
        )
    except (ValueError, RuntimeError) as e:
        print(f"Fehler Regula Falsi: {e}")


if __name__ == "__main__":
    plotter()
