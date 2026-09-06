#!/usr/bin/env python3
"""De 70k a 225k en 5 años — imagen + GIF. Proyección de DCA, no backtest."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from PIL import Image

START = 70_000.0
ANNUAL = 23_000.0
MONTHLY = ANNUAL / 12.0
YEARS = 5
TARGET = 225_000.0
WITHDRAW = 10_000.0
RATES = {"solo_aportes": 0.00, "r8": 0.08, "r10": 0.10}
COLORS = {
    "solo_aportes": "#8B93A7",
    "r8": "#F5B042",
    "r10": "#3DDB8A",
    "target": "#6EA8FE",
}
BG = "#0B1020"
GRID = "#1C2438"
TEXT = "#E8ECF4"
MUTED = "#8B93A7"
OUT = Path(".")


def path(rate: float, months: int = YEARS * 12) -> np.ndarray:
    r = (1.0 + rate) ** (1.0 / 12.0) - 1.0
    v = np.empty(months + 1, dtype=float)
    v[0] = START
    for m in range(1, months + 1):
        v[m] = v[m - 1] * (1.0 + r) + MONTHLY
    return v


def fmt_money(x: float) -> str:
    if abs(x) >= 1_000_000:
        return f"USD {x / 1_000_000:.2f}M".replace(".00M", "M")
    if abs(x) >= 1_000:
        return f"USD {x / 1_000:.0f}K"
    return f"USD {x:.0f}"


def _style(ax) -> None:
    ax.set_facecolor(BG)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7, alpha=0.9)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)


def series() -> dict[str, np.ndarray]:
    return {k: path(r) for k, r in RATES.items()}


def build_figure(data: dict[str, np.ndarray], upto: int | None = None, dpi: int = 160):
    months = np.arange(YEARS * 12 + 1)
    cut = len(months) - 1 if upto is None else int(upto)
    x = months[: cut + 1] / 12.0

    fig, ax = plt.subplots(figsize=(10.2, 12.8), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    fig.text(0.5, 0.965, "Plan de acumulación  ·  DCA mensual",
             ha="center", va="top", color=MUTED, fontsize=9, fontname="DejaVu Sans")
    fig.text(0.5, 0.928, "DE 70 MIL A 225 MIL",
             ha="center", va="top", color=TEXT, fontsize=20, fontweight="bold", fontname="DejaVu Sans")
    fig.text(0.5, 0.898, "EN 5 AÑOS, SIN DEJAR DE APORTAR",
             ha="center", va="top", color=TEXT, fontsize=16, fontweight="bold", fontname="DejaVu Sans")
    fig.text(0.5, 0.868,
             "Empiezo con 70 mil   ·   aporto 23 mil al año   ·   meta: retiro parcial 10 mil / año",
             ha="center", va="top", color=MUTED, fontsize=8.0, fontname="DejaVu Sans")

    ax.set_position([0.12, 0.16, 0.78, 0.66])
    ax.axhline(TARGET, color=COLORS["target"], linewidth=1.15, linestyle=(0, (6, 4)), alpha=0.9, zorder=2)
    ax.plot(x, data["solo_aportes"][: cut + 1], linestyle=(0, (5, 5)),
            color=COLORS["solo_aportes"], linewidth=1.7, zorder=3, alpha=0.9)
    ax.plot(x, data["r8"][: cut + 1], color=COLORS["r8"], linewidth=2.2, solid_capstyle="round", zorder=4)
    ax.plot(x, data["r10"][: cut + 1], color=COLORS["r10"], linewidth=2.4, solid_capstyle="round", zorder=5)

    _style(ax)
    ax.set_xlim(0, YEARS)
    ymax = max(data["r10"].max(), TARGET) * 1.12
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xticklabels(["Hoy", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"])

    def _ytick(v, _p):
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M".replace(".0M", "M")
        if v >= 1_000:
            return f"${v / 1_000:.0f}K"
        return "$0"

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_ytick))
    last_y = data["r10"][cut]
    ax.scatter([x[-1]], [last_y], s=42, color=COLORS["r10"], zorder=6, edgecolors="white", linewidths=0.6)
    ax.text(YEARS + 0.06, TARGET, "  meta 225K", color=COLORS["target"], fontsize=8.5, va="center")
    ax.text(0.08, START + 4000, "hoy 70K", color=MUTED, fontsize=8)

    if upto is None:
        ax.text(YEARS, data["solo_aportes"][-1],
                f"  solo aportes\n  {fmt_money(data['solo_aportes'][-1])}",
                color=COLORS["solo_aportes"], fontsize=8.2, va="center")
        ax.text(YEARS, data["r8"][-1], f"  ~8%   {fmt_money(data['r8'][-1])}",
                color=COLORS["r8"], fontsize=9, fontweight="bold", va="bottom")
        ax.text(YEARS, data["r10"][-1] + 3500, f"  ~10%  {fmt_money(data['r10'][-1])}",
                color=COLORS["r10"], fontsize=9.5, fontweight="bold", va="bottom")
    else:
        fig.text(0.88, 0.84, f"Año {x[-1]:.1f}", ha="right", color=TEXT,
                 fontsize=20, fontweight="bold", alpha=0.9)
        ax.text(x[-1], last_y, f"  {fmt_money(last_y)}",
                color=COLORS["r10"], fontsize=10, fontweight="bold", va="center")

    fig.text(0.5, 0.078,
             "Solo ahorrar llega a 185 mil. El interes compuesto cierra el hueco hasta 225 mil+\n"
             "y habilita un retiro parcial de 10 mil al año  ·  cerca del 4% del capital.",
             ha="center", va="center", color=MUTED, fontsize=8.0, linespacing=1.45)
    fig.text(0.5, 0.028,
             "Proyección ilustrativa al 0% / 8% / 10% anual. No es garantía ni recomendación. "
             "El mercado no sube en línea recta.",
             ha="center", color="#5C6478", fontsize=6.6)
    return fig


def save_static(data, path: Path) -> Path:
    fig = build_figure(data, dpi=170)
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    return path


def save_gif(data, path: Path, n_frames: int = 48) -> Path:
    tmp = path.parent / "_frames_225k"
    tmp.mkdir(exist_ok=True)
    n = YEARS * 12
    picks = np.unique(np.linspace(2, n, n_frames).astype(int))
    files = []
    for i, p in enumerate(picks):
        fig = build_figure(data, upto=int(p), dpi=110)
        fp = tmp / f"f{i:03d}.png"
        fig.savefig(fp, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.22)
        plt.close(fig)
        files.append(fp)
    imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=80) for f in files]
    w = min(im.size[0] for im in imgs)
    h = min(im.size[1] for im in imgs)
    imgs = [im.crop((0, 0, w, h)) for im in imgs]
    durations = [90] * (len(imgs) - 1) + [2200]
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=durations, loop=0, disposal=2)
    for f in files:
        f.unlink()
    tmp.rmdir()
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = series()
    print("Final solo aportes:", f"{data['solo_aportes'][-1]:,.0f}")
    print("Final ~8%         :", f"{data['r8'][-1]:,.0f}")
    print("Final ~10%        :", f"{data['r10'][-1]:,.0f}")
    print("PNG:", save_static(data, OUT / "acumulacion_70k_225k.png"))
    print("GIF:", save_gif(data, OUT / "acumulacion_70k_225k.gif"))


if __name__ == "__main__":
    main()
