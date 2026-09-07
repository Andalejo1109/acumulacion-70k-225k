#!/usr/bin/env python3
"""De 70k a 225k en 5 anos, luego retiro de 10k indexado al 3%."""
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
WITHDRAW0 = 10_000.0
COLA = 0.03
RATES = {"r10": 0.10, "r13": 0.13, "r17": 0.17}
COLORS = {"r10": "#3DDB8A", "r13": "#F5B042", "r17": "#6EA8FE", "target": "#8B93A7"}
LABELS = {"r10": "~10%", "r13": "~13%", "r17": "~17%"}
BG, GRID, TEXT, MUTED = "#0B1020", "#1C2438", "#E8ECF4", "#8B93A7"
OUT = Path(".")

def path(rate: float, months: int = YEARS * 12) -> np.ndarray:
    r = (1.0 + rate) ** (1.0 / 12.0) - 1.0
    v = np.empty(months + 1, dtype=float)
    v[0] = START
    for m in range(1, months + 1):
        v[m] = v[m - 1] * (1.0 + r) + MONTHLY
    return v

def series():
    return {k: path(r) for k, r in RATES.items()}

def phase2(rate: float, start: float, years: int = 10):
    v = start
    spent = 0.0
    rows = []
    for y in range(1, years + 1):
        v *= 1.0 + rate
        wd = WITHDRAW0 * ((1.0 + COLA) ** (y - 1))
        v -= wd
        spent += wd
        rows.append((y, v, wd, spent))
    return rows

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

def build_figure(data, upto=None, dpi=160):
    months = np.arange(YEARS * 12 + 1)
    cut = len(months) - 1 if upto is None else int(upto)
    x = months[: cut + 1] / 12.0
    fig, ax = plt.subplots(figsize=(10.2, 12.8), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.text(0.5, 0.965, "Plan de acumulacion  ·  DCA mensual", ha="center", va="top", color=MUTED, fontsize=9, fontname="DejaVu Sans")
    fig.text(0.5, 0.928, "DE 70 MIL A 225 MIL", ha="center", va="top", color=TEXT, fontsize=20, fontweight="bold", fontname="DejaVu Sans")
    fig.text(0.5, 0.898, "LUEGO RETIRO PARCIAL INDEXADO", ha="center", va="top", color=TEXT, fontsize=16, fontweight="bold", fontname="DejaVu Sans")
    fig.text(0.5, 0.868, "23 mil al ano  ·  meta 225 mil  ·  retiro 10 mil +3% anual", ha="center", va="top", color=MUTED, fontsize=8.0, fontname="DejaVu Sans")
    ax.set_position([0.12, 0.16, 0.78, 0.66])
    ax.axhline(TARGET, color=COLORS["target"], linewidth=1.15, linestyle=(0, (6, 4)), alpha=0.9, zorder=2)
    for key in ("r10", "r13", "r17"):
        ax.plot(x, data[key][: cut + 1], color=COLORS[key], linewidth=2.3, solid_capstyle="round", zorder=4)
    _style(ax)
    ax.set_xlim(0, YEARS)
    ymax = max(data["r17"].max(), TARGET) * 1.12
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xticklabels(["Hoy", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"])
    def _ytick(v, _p):
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M".replace(".0M", "M")
        if v >= 1_000:
            return f"${v / 1_000:.0f}K"
        return "$0"
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_ytick))
    last_y = data["r17"][cut]
    ax.scatter([x[-1]], [last_y], s=42, color=COLORS["r17"], zorder=6, edgecolors="white", linewidths=0.6)
    ax.text(YEARS + 0.06, TARGET, "  meta 225K", color=COLORS["target"], fontsize=8.5, va="center")
    ax.text(0.08, START + 4000, "hoy 70K", color=MUTED, fontsize=8)
    if upto is None:
        offsets = {"r10": -4000, "r13": 4000, "r17": 12000}
        for key in ("r10", "r13", "r17"):
            ax.text(YEARS, data[key][-1] + offsets[key], f"  {LABELS[key]}  {fmt_money(data[key][-1])}", color=COLORS[key], fontsize=9.2, fontweight="bold", va="center")
    else:
        fig.text(0.88, 0.84, f"Ano {x[-1]:.1f}", ha="right", color=TEXT, fontsize=20, fontweight="bold", alpha=0.9)
        ax.text(x[-1], last_y, f"  {fmt_money(last_y)}", color=COLORS["r17"], fontsize=10, fontweight="bold", va="center")
    fig.text(0.5, 0.078, "Al cruzar 225 mil empieza el retiro: 10 mil el ano 1, +3% cada ano.\nSi el portafolio rinde mas que ese retiro, el capital sigue creciendo.", ha="center", va="center", color=MUTED, fontsize=8.0, linespacing=1.45)
    fig.text(0.5, 0.028, "Escenarios ilustrativos al 10% / 13% / 17%. No es garantia. El mercado no sube en linea recta.", ha="center", color="#5C6478", fontsize=6.6)
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

def print_tables(data) -> None:
    print("FASE 1  (70k + 23k/ano, 5 anos)")
    for k, r in RATES.items():
        print(f"  {LABELS[k]:>5}  {data[k][-1]:,.0f}")
    print("\nFASE 2  desde 225k | retiro 10k +3%/ano | sin aportes")
    for k, r in RATES.items():
        rows = phase2(r, TARGET, 10)
        print(f"{LABELS[k]:>5} y1={rows[0][1]:,.0f} y5={rows[4][1]:,.0f} y10={rows[9][1]:,.0f} cobrado={rows[9][3]:,.0f}")

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = series()
    print_tables(data)
    print("PNG:", save_static(data, OUT / "acumulacion_70k_225k.png"))
    print("GIF:", save_gif(data, OUT / "acumulacion_70k_225k.gif"))

if __name__ == "__main__":
    main()
