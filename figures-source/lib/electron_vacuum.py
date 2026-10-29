"""The scientist electron inside a perfect crystal, perceiving its universe as
'vacuum': the lattice is everywhere around it, but its thought bubble (and its
magnifying glass) show empty space with a free particle of effective mass m*.

Usage: python3 electron_vacuum.py OUTDIR
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Ellipse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scientist_electron import character, sphere, INK, BODY, ATOM

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

A_LAT, R_ATOM = 2.25, 0.34
XL, XR, YB, YT = -5.9, 8.4, -3.5, 6.1
VAC_BG = "#f2f8fd"
ORANGE = "#e07a3c"


def lattice(ax):
    xs = (np.arange(-4, 6) + 0.5) * A_LAT
    ys = (np.arange(-3, 4) + 0.5) * A_LAT
    for x in xs:
        ax.plot([x, x], [ys[0], ys[-1]], color="#9aa8b5", lw=5, zorder=-5, solid_capstyle="round")
    for y in ys:
        ax.plot([xs[0], xs[-1]], [y, y], color="#9aa8b5", lw=5, zorder=-5, solid_capstyle="round")
    for x in xs:
        for y in ys:
            sphere(ax, x, y, R_ATOM, ATOM, z=-4, n=26, rim=False)
            ax.add_patch(Circle((x, y), R_ATOM, fill=False, lw=1.4, ec="#2c3b4a", zorder=-3.9))


def cloud(ax, cx, cy, w, h, n=13, z=6, fc="white"):
    """Thought-bubble cloud: union of bumps around an ellipse, outlined once."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.2
    bumps = [(cx + 0.5 * w * np.cos(a), cy + 0.5 * h * np.sin(a),
              0.62 * min(w, h) * (0.36 + 0.06 * np.cos(3 * a))) for a in t]
    for x, y, r in bumps:
        ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=5.0, zorder=z))
    ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec="none", zorder=z + 0.01))
    for x, y, r in bumps:
        ax.add_patch(Circle((x, y), r, fc=fc, ec="none", zorder=z + 0.01))
    return bumps


def scene():
    fig = plt.figure(figsize=(12, 12 * (YT - YB) / (XR - XL)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(XL, XR); ax.set_ylim(YB, YT)
    lattice(ax)
    character(ax, lens="empty", shadow=False)

    # thought bubble
    cx, cy, w, h = 4.55, 3.45, 5.7, 3.1
    cloud(ax, cx, cy, w, h)
    ax.add_patch(Ellipse((cx, cy - 0.05), w * 0.92, h * 0.86, fc=VAC_BG, ec="none", zorder=6.02))
    for (x, y, r) in ((0.75, 1.95, 0.11), (1.20, 2.30, 0.17), (1.80, 2.62, 0.24)):
        ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=2.2, zorder=6))

    # inside: empty space, a free particle gliding with effective mass m*
    ax.text(cx, cy + 0.92, "vacuum", ha="center", va="center", fontsize=30,
            family="DejaVu Serif", style="italic", color="#2f4a63", zorder=7)
    ex, ey = cx - 1.5, cy - 0.3
    for k, dy in enumerate((-0.12, 0.0, 0.12)):
        ax.plot([ex - 1.15 + 0.15 * abs(k - 1), ex - 0.42], [ey + dy * 1.6] * 2, color="#9fb6cb",
                lw=2.2, solid_capstyle="round", zorder=7)
    sphere(ax, ex, ey, 0.30, BODY, z=7.1, n=24)
    ax.add_patch(Circle((ex - 0.08, ey + 0.05), 0.045, color=INK, zorder=7.3))
    ax.add_patch(Circle((ex + 0.10, ey + 0.05), 0.045, color=INK, zorder=7.3))
    ax.add_patch(FancyArrowPatch((ex + 0.42, ey), (ex + 1.35, ey), arrowstyle="-|>,head_length=9,head_width=5",
                                 lw=2.4, color=ORANGE, zorder=7.2))
    ax.text(ex + 0.88, ey + 0.32, r"$\hbar k$", ha="center", va="center", fontsize=17,
            color=ORANGE, zorder=7.3)
    ax.text(cx + 1.4, cy - 0.32, r"$E=\dfrac{\hbar^2k^2}{2m^{*}}$", ha="center", va="center",
            fontsize=22, color="#2f4a63", zorder=7.3)

    # a little "?" from the scientist: does it see the atoms through the lens?  (it does not)
    return fig


if __name__ == "__main__":
    fig = scene()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"electron_vacuum.{ext}"), dpi=300,
                    bbox_inches="tight", pad_inches=0.0, facecolor="white")
    print("done")
