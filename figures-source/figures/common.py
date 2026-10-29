"""Shared style for the website figure series (same look as the talk figures:
shaded-sphere atoms, beige BZ tori, muted blue / orange accents)."""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

_argv = sys.argv
sys.argv = sys.argv[:1]                       # helper modules read argv at import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]      # package root
ASSETS = str(ROOT / "assets")
sys.path.insert(0, str(ROOT / "lib"))
import scientist_electron as SE              # noqa: E402
import electron_vacuum as EV                 # noqa: E402
import electron_obstacles as EO              # noqa: E402
sys.argv = _argv

sphere = SE.sphere
INK = "#24303b"
NAVY = "#2f4a63"
GRAY = "#7d8a96"
LIGHT = "#b9c8d6"
ATOM = SE.ATOM
BODY = SE.BODY
ORANGE = "#e07a3c"
GREEN = "#3f7d62"
BOND = "#9aa8b5"
VAC_BG = "#f2f6fa"
STREAK = "#9fb6cb"
plt.rcParams["font.family"] = "Inter"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

W_IN, H_IN, DPI = 12.0, 6.75, 200
OUT = os.environ.get("FIG_OUT", str(ROOT / "out"))
os.makedirs(OUT, exist_ok=True)


def figure(w=W_IN, h=H_IN):
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    fig.patch.set_facecolor("white")
    return fig


def canvas(fig):
    """Full-figure overlay axes in figure-fraction coordinates (for labels/arrows)."""
    ax = fig.add_axes([0, 0, 1, 1], zorder=50)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.patch.set_alpha(0)
    return ax


# Every text size below is written at the original (print) scale and multiplied by TEXT_SCALE.
# The website shows these 2400 px figures only ~590 px wide, so fig1-fig6 use WEB_TEXT_SCALE.
TEXT_SCALE = 1.0
WEB_TEXT_SCALE = 1.5


def text_scale(s):
    global TEXT_SCALE
    TEXT_SCALE = s


def fs(pt):
    return pt * TEXT_SCALE


def heading(ov, x, y, text, sub=None, color=NAVY, size=17):
    ov.text(x, y, text, ha="center", va="center", fontsize=fs(size), fontweight="semibold", color=color)
    if sub:
        ov.text(x, y - 0.045 * TEXT_SCALE, sub, ha="center", va="center", fontsize=fs(12), color=GRAY)


def flow_arrow(ov, x0, x1, y, label=None):
    ov.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>,head_length=9,head_width=5",
                                 lw=1.8, color=ORANGE, mutation_scale=1.2, shrinkA=0, shrinkB=0))
    if label:
        ov.text((x0 + x1) / 2, y + 0.04, label, ha="center", va="bottom", fontsize=fs(11), color=GRAY,
                style="italic", linespacing=1.3)


def panel_axes(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return ax


def _box(ax, **kw):
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    return FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                          boxstyle=f"round,pad=0,rounding_size={0.04 * (x1 - x0)}", **kw)


def frame(ax, fc=None, ec="#d9dfe5", lw=1.2, z=-10, clip=True):
    """Rounded panel frame; with clip=True everything already drawn is clipped to it."""
    if clip:
        cp = _box(ax, fc="none", ec="none", transform=ax.transData)
        ax.add_patch(cp); cp.set_visible(False)
        for a in ax.get_children():
            if hasattr(a, "set_clip_path") and a is not cp and a is not ax.patch:
                a.set_clip_path(cp)
    if fc:
        ax.add_patch(_box(ax, fc=fc, ec="none", zorder=-20))
    ax.add_patch(_box(ax, fc="none", ec=ec, lw=lw, zorder=60, clip_on=False))


def electron(ax, x, y, r=0.36, vel=None, z=5):
    """Plain shaded electron (no face) with motion streaks."""
    sphere(ax, x, y, r, BODY, z=z, n=26)
    if vel is not None:
        vx, vy = vel; n = np.hypot(vx, vy); ux, uy = vx / n, vy / n
        for off in (-0.35, 0.0, 0.35):
            px, py = -uy * off * r, ux * off * r
            L = (0.9 - 0.25 * abs(off) / 0.35) * r * 1.8
            ax.plot([x - ux * 1.2 * r + px, x - ux * (1.2 * r + L) + px],
                    [y - uy * 1.2 * r + py, y - uy * (1.2 * r + L) + py],
                    color=STREAK, lw=2.2, solid_capstyle="round", zorder=z - 0.05)


def path(ax, pts, z=4, color=ORANGE, lw=2.0, dashed=True, arrow=True):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=(0, (4, 3)) if dashed else "-",
            zorder=z, solid_capstyle="round", alpha=0.95)
    if arrow:
        ax.add_patch(FancyArrowPatch(tuple(pts[-2]), tuple(pts[-1]), arrowstyle="-|>,head_length=8,head_width=4.5",
                                     lw=0, color=color, zorder=z, mutation_scale=1.3))


def perfect_lattice(ax, nx, ny, a, r_atom):
    xs = (np.arange(nx) + 0.5) * a; ys = (np.arange(ny) + 0.5) * a
    for x in xs:
        ax.plot([x, x], [ys[0] - a, ys[-1] + a], color=BOND, lw=4.2, zorder=-5, solid_capstyle="round")
    for y in ys:
        ax.plot([xs[0] - a, xs[-1] + a], [y, y], color=BOND, lw=4.2, zorder=-5, solid_capstyle="round")
    for x in xs:
        for y in ys:
            sphere(ax, x, y, r_atom, ATOM, z=-4, n=24, rim=False)
            ax.add_patch(Circle((x, y), r_atom, fill=False, lw=1.2, ec="#2c3b4a", zorder=-3.9))
    return xs, ys


def save(fig, name):
    p = os.path.join(OUT, name + ".png")
    fig.savefig(p, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("wrote", p)
