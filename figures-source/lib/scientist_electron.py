"""'Scientist electron' character: a shaded-sphere electron in a lab coat with
round glasses, a spin-arrow antenna, a magnifying glass (showing a magnified
lattice) and a clipboard with a Brillouin-zone torus doodle.

Usage: python3 scientist_electron.py OUTDIR
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import (Circle, Ellipse, Polygon, FancyBboxPatch, Arc,
                                FancyArrowPatch)
from matplotlib.transforms import Affine2D


BODY = "#3d9be0"
INK = "#24303b"
COAT = "#fbfcfd"
COAT_SHADE = "#dfe6ec"
ATOM = "#6f8fb0"


def sphere(ax, x, y, r, color, z=3, n=40, rim=True, clip=None):
    base = np.array(to_rgb(color))
    patches = []
    for i in range(n):
        f = i / (n - 1)
        rr = r * (1 - 0.8 * f)
        off = 0.30 * r * f
        col = np.clip(base * (0.66 + 0.34 * f) + (1 - base) * 0.78 * f ** 2.4, 0, 1)
        p = Circle((x - off, y + off), rr, color=col, lw=0, zorder=z + i * 1e-4)
        ax.add_patch(p)
        if clip is not None:
            p.set_clip_path(clip)
        patches.append(p)
    if rim:
        ax.add_patch(Circle((x, y), r, fill=False, lw=2.2, ec=INK, zorder=z + 0.05))
    return patches


def character(ax, lens="lattice", shadow=True, spin="up"):
    """Draw the character in data coordinates of ax (body: unit circle at the origin;
    overall extent about x in [-2.2, 2.3], y in [-1.6, 2.1])."""
    # ground shadow
    if shadow:
        ax.add_patch(Ellipse((0.05, -1.42), 2.1, 0.28, color="#000000", alpha=0.10, lw=0, zorder=0))

    # legs + shoes
    for sx in (-0.38, 0.38):
        ax.plot([sx, sx * 1.08], [-0.85, -1.30], color=INK, lw=4, solid_capstyle="round", zorder=1)
        ax.add_patch(Ellipse((sx * 1.08 + np.sign(sx) * 0.07, -1.33), 0.38, 0.17,
                             color=INK, zorder=1.1))

    # body
    body_clip = Circle((0, 0), 1.0, transform=ax.transData)
    sphere(ax, 0, 0, 1.0, BODY, z=2)

    # lab coat (clipped to the body), V-neck showing the body
    coat = Polygon([(-1.3, 0.05), (-0.30, 0.05), (0, -0.52), (0.30, 0.05), (1.3, 0.05),
                    (1.3, -1.3), (-1.3, -1.3)], closed=True, fc=COAT, ec="none", zorder=2.5)
    ax.add_patch(coat); coat.set_clip_path(Circle((0, 0), 1.0, transform=ax.transData))
    shade = Ellipse((0.42, -0.62), 1.3, 1.1, fc=COAT_SHADE, ec="none", zorder=2.55)
    ax.add_patch(shade); shade.set_clip_path(Polygon([(-1.3, 0.05), (-0.30, 0.05), (0, -0.52),
        (0.30, 0.05), (1.3, 0.05), (1.3, -1.3), (-1.3, -1.3)], transform=ax.transData))
    shade.set_clip_path(Circle((0, 0), 1.0, transform=ax.transData))
    # collar / lapels
    for sgn in (-1, 1):
        lap = Polygon([(sgn * 0.30, 0.05), (sgn * 0.62, 0.0), (sgn * 0.20, -0.28), (0, -0.52)],
                      closed=True, fc=COAT, ec=INK, lw=1.6, zorder=2.7)
        ax.add_patch(lap)
    ax.plot([0, 0], [-0.52, -0.98], color=INK, lw=1.4, zorder=2.7)
    for by in (-0.66, -0.84):
        ax.add_patch(Circle((0.09, by), 0.035, color=INK, zorder=2.8))
    # coat outline along the body edge
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=2.2, ec=INK, zorder=2.9))
    ax.plot([-0.998, -0.62], [0.05, 0.0], color=INK, lw=1.6, zorder=2.7)
    ax.plot([0.998, 0.62], [0.05, 0.0], color=INK, lw=1.6, zorder=2.7)

    # breast pocket with pens and an e^- badge
    ax.add_patch(FancyBboxPatch((0.36, -0.52), 0.34, 0.26, boxstyle="round,pad=0.01,rounding_size=0.04",
                                fc=COAT, ec=INK, lw=1.4, zorder=3.0))
    for px, col in ((0.44, "#e07a3c"), (0.53, "#3b8f5e")):
        ax.plot([px, px + 0.02], [-0.30, -0.14], color=col, lw=3.2, solid_capstyle="round", zorder=2.95)
    ax.add_patch(FancyBboxPatch((-0.66, -0.50), 0.36, 0.22, boxstyle="round,pad=0.01,rounding_size=0.05",
                                fc="#ffffff", ec=INK, lw=1.3, zorder=3.0))
    ax.text(-0.48, -0.39, r"$e^{-}$", ha="center", va="center", fontsize=15, color=INK, zorder=3.1)

    # face: cheeks, eyes behind round glasses, smile
    for cx in (-0.55, 0.55):
        ax.add_patch(Ellipse((cx, 0.20), 0.22, 0.12, color="#f2a0a6", alpha=0.55, lw=0, zorder=3.0))
    eye_dx, eye_y = 0.30, 0.45
    look = np.array([0.05, 0.035])               # glancing toward the lens
    for sx in (-1, 1):
        ex = sx * eye_dx
        ax.add_patch(Ellipse((ex, eye_y), 0.21, 0.25, fc="white", ec=INK, lw=1.2, zorder=3.2))
        ax.add_patch(Circle((ex + look[0], eye_y + look[1] - 0.02), 0.075, color=INK, zorder=3.3))
        ax.add_patch(Circle((ex + look[0] + 0.03, eye_y + look[1] + 0.015), 0.025, color="white", zorder=3.4))
        ax.add_patch(Circle((ex, eye_y), 0.215, fill=True, fc="#dff1ff", alpha=0.22, ec=INK,
                            lw=2.6, zorder=3.5))
    ax.add_patch(Arc((0, eye_y + 0.02), 0.20, 0.14, theta1=20, theta2=160, lw=2.4, color=INK, zorder=3.5))
    ax.add_patch(Arc((0.02, 0.17), 0.30, 0.20, theta1=200, theta2=340, lw=2.4, color=INK, zorder=3.3))
    # eyebrows (curious)
    ax.plot([-0.40, -0.20], [0.75, 0.79], color=INK, lw=2.2, solid_capstyle="round", zorder=3.3)
    ax.plot([0.20, 0.42], [0.80, 0.84], color=INK, lw=2.2, solid_capstyle="round", zorder=3.3)

    # spin-up antenna
    t = np.linspace(0, 1, 60)
    ax.plot(0.06 * np.sin(np.pi * t), 0.98 + 0.52 * t, color=INK, lw=2.6, solid_capstyle="round", zorder=1.5)
    tri = [(-0.13, 1.47), (0.13, 1.47), (0.0, 1.70)] if spin == "up" else [(-0.13, 1.70), (0.13, 1.70), (0.0, 1.47)]
    ax.add_patch(Polygon(tri, closed=True,
                         fc="#e07a3c" if spin == "up" else "#3d9be0", ec=INK, lw=1.6, joinstyle="round", zorder=1.6))
    # little rotation arc around the antenna (spin)
    ax.add_patch(FancyArrowPatch(*(((-0.26, 1.24), (0.24, 1.30)) if spin == "up" else ((0.24, 1.30), (-0.26, 1.24))), connectionstyle="arc3,rad=0.55" if spin == "up" else "arc3,rad=-0.55",
                                 arrowstyle="-|>,head_length=6,head_width=3.5", lw=1.6,
                                 color="#e07a3c", zorder=1.7))

    # right arm + magnifying glass with magnified lattice inside
    hx, hy = 1.28, 0.10
    ax.plot([0.88, 1.12, hx], [-0.30, -0.12, hy], color=INK, lw=3.2, solid_capstyle="round",
            solid_joinstyle="round", zorder=4)
    lc, lr = np.array([1.70, 0.88]), 0.40
    d = (lc - np.array([hx, hy])); d /= np.linalg.norm(d)
    h0 = np.array([hx, hy]) - d * 0.06; h1 = lc - d * lr
    ax.plot([h0[0], h1[0]], [h0[1], h1[1]], color="#8a5a35", lw=7, solid_capstyle="round", zorder=4.1)
    sphere(ax, hx, hy, 0.12, BODY, z=4.2, n=12)
    lens_clip = Circle(tuple(lc), lr, transform=ax.transData)
    ax.add_patch(Circle(tuple(lc), lr, fc="#eaf6ff", ec="none", zorder=4.3))
    for i in (range(-2, 3) if lens == "lattice" else ()):
        for j in range(-2, 3):
            px, py = lc[0] + i * 0.30 + 0.07, lc[1] + j * 0.30 - 0.05
            for (qx, qy) in ((px + 0.30, py), (px, py + 0.30)):
                ln, = ax.plot([px, qx], [py, qy], color="#9aa8b5", lw=2.5, zorder=4.35)
                ln.set_clip_path(lens_clip)
            for p in sphere(ax, px, py, 0.085, ATOM, z=4.4, n=10, rim=False, clip=lens_clip):
                pass
    ax.add_patch(Arc(tuple(lc), 2 * lr * 0.78, 2 * lr * 0.78, theta1=105, theta2=165,
                     lw=3, color="white", alpha=0.9, zorder=4.6))
    ax.add_patch(Circle(tuple(lc), lr, fill=False, ec=INK, lw=4.5, zorder=4.7))
    ax.add_patch(Circle(tuple(lc), lr + 0.03, fill=False, ec="#c0c8d0", lw=1.2, zorder=4.65))

    # left arm + clipboard with a BZ-torus doodle
    cbx, cby, ang = -1.62, -0.28, 8
    tr = Affine2D().rotate_deg_around(cbx, cby, ang) + ax.transData
    ax.add_patch(FancyBboxPatch((cbx - 0.42, cby - 0.58), 0.84, 1.10,
                                boxstyle="round,pad=0.01,rounding_size=0.06",
                                fc="#c99a62", ec=INK, lw=1.8, zorder=3.6, transform=tr))
    ax.add_patch(FancyBboxPatch((cbx - 0.34, cby - 0.50), 0.68, 0.90,
                                boxstyle="square,pad=0", fc="white", ec="#b8c2cc", lw=0.8,
                                zorder=3.65, transform=tr))
    ax.add_patch(FancyBboxPatch((cbx - 0.16, cby + 0.42), 0.32, 0.13,
                                boxstyle="round,pad=0.01,rounding_size=0.03",
                                fc="#9aa3ab", ec=INK, lw=1.4, zorder=3.7, transform=tr))
    # torus doodle
    ty = cby + 0.16
    ax.add_patch(Ellipse((cbx, ty), 0.58, 0.32, fill=False, ec="#3d4750", lw=1.7,
                         zorder=3.75, transform=tr))
    ax.add_patch(Arc((cbx, ty + 0.025), 0.28, 0.12, theta1=195, theta2=345, ec="#3d4750", lw=1.6,
                     zorder=3.75, transform=tr))
    ax.add_patch(Arc((cbx, ty - 0.005), 0.20, 0.08, theta1=25, theta2=155, ec="#3d4750", lw=1.6,
                     zorder=3.75, transform=tr))
    ax.add_patch(Arc((cbx - 0.21, ty - 0.01), 0.09, 0.22, theta1=90, theta2=270, ec="#e07a3c", lw=1.5,
                     zorder=3.76, transform=tr))
    ax.add_patch(Ellipse((cbx, ty - 0.005), 0.44, 0.215, fill=False, ec="#e07a3c", lw=1.2,
                         ls=(0, (2, 1.6)), zorder=3.76, transform=tr))
    for k, w in enumerate((0.48, 0.38, 0.44)):
        ax.plot([cbx - 0.24, cbx - 0.24 + w], [cby - 0.15 - 0.10 * k] * 2, color="#9aa8b5",
                lw=1.6, solid_capstyle="round", zorder=3.75, transform=tr)
    ax.text(cbx + 0.12, cby - 0.43, "?!", fontsize=11, color="#e07a3c", ha="center", va="center",
            fontweight="bold", zorder=3.8, transform=tr)
    # arm holding the board edge
    ax.plot([-0.90, -1.10, -1.24], [-0.30, -0.40, -0.30], color=INK, lw=3.2, solid_capstyle="round",
            solid_joinstyle="round", zorder=3.9)
    sphere(ax, -1.25, -0.29, 0.12, BODY, z=3.95, n=12)



def draw(OUT, fname, transparent):
    fig, ax = plt.subplots(figsize=(7, 7.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.25, 2.35); ax.set_ylim(-1.75, 2.15)
    character(ax)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{fname}.{ext}"), dpi=300, bbox_inches="tight",
                    pad_inches=0.05, transparent=transparent,
                    facecolor="none" if transparent else "white")
    plt.close(fig)


if __name__ == "__main__":
    OUT = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(OUT, exist_ok=True)
    draw(OUT, "scientist_electron", transparent=False)
    draw(OUT, "scientist_electron_transparent", transparent=True)
    print("done")
