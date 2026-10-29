"""The scientist electron inside a crystal WITH defects: the lattice itself is
invisible to it (vacuum), but each defect appears as a localized obstacle.

Background: strained square lattice with a vacancy, a substitutional impurity
and an interstitial. Thought bubble: empty space containing only the three
obstacles (same types, same relative layout); a small free electron scatters
off one of them.  H = p^2/2m* + sum_i V(r - R_i).

Usage: python3 electron_obstacles.py OUTDIR   (needs scientist_electron.py and
electron_vacuum.py next to it)
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scientist_electron import character, sphere, INK, BODY, ATOM
from electron_vacuum import cloud, VAC_BG

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

A_LAT, R_ATOM = 2.25, 0.34
XL, XR, YB, YT = -5.9, 8.4, -3.5, 6.4
IMP = "#e07a3c"
INT = "#4a5560"
BOND = "#9aa8b5"

# defects, in lattice-index coordinates (site (i, j) sits at ((i+0.5)a, (j+0.5)a))
VAC = (-2, 1)                 # -> (-3.375, 3.375)
SUB = (2, -1)                 # -> ( 5.625, -1.125)
INTER = (-1.5, -1.5)          # cell centre -> (-2.25, -2.25)


def site(ij):
    return (np.asarray(ij, float) + 0.5) * A_LAT


def strain(P, defects):
    U = np.zeros_like(P)
    for c, s in defects:
        d = P - c
        rho = np.linalg.norm(d, axis=-1, keepdims=True) / A_LAT
        rho = np.where(rho < 1e-9, 1, rho)
        U += A_LAT * s * d / (rho * A_LAT) * np.exp(-(rho - 1) ** 2 / 0.9) / rho
    return U


def lattice(ax):
    I, J = np.meshgrid(np.arange(-4, 5), np.arange(-3, 4), indexing="ij")
    P0 = (np.stack([I, J], -1) + 0.5) * A_LAT
    P = P0 + strain(P0, [(site(VAC), -0.05), (site(SUB), 0.05), (site(INTER), 0.065)])
    idx = {(int(I[a, b]), int(J[a, b])): P[a, b] for a in range(I.shape[0]) for b in range(I.shape[1])}
    for (i, j), p in idx.items():
        for q in ((i + 1, j), (i, j + 1)):
            if q in idx and VAC not in ((i, j), q):
                ax.plot([p[0], idx[q][0]], [p[1], idx[q][1]], color=BOND, lw=5, zorder=-5,
                        solid_capstyle="round")
    for (i, j), p in idx.items():
        if (i, j) == VAC:
            ax.add_patch(Circle(tuple(site(VAC)), R_ATOM, fill=False, ls=(0, (3, 2.2)), lw=1.8,
                                ec="#7d8a96", zorder=-3.9))
        elif (i, j) == SUB:
            sphere(ax, *p, R_ATOM * 1.25, IMP, z=-4, n=26, rim=False)
            ax.add_patch(Circle(tuple(p), R_ATOM * 1.25, fill=False, lw=1.4, ec="#5a2f14", zorder=-3.9))
        else:
            sphere(ax, *p, R_ATOM, ATOM, z=-4, n=26, rim=False)
            ax.add_patch(Circle(tuple(p), R_ATOM, fill=False, lw=1.4, ec="#2c3b4a", zorder=-3.9))
    c = site(INTER)
    sphere(ax, *c, R_ATOM * 0.62, INT, z=-3.8, n=20, rim=False)
    ax.add_patch(Circle(tuple(c), R_ATOM * 0.62, fill=False, lw=1.3, ec="#1b2128", zorder=-3.7))


def halo(ax, x, y, r, color, z, n=7, a0=0.20):
    """Soft potential range around an obstacle."""
    for k in range(n):
        rr = r * (1 - k / n)
        ax.add_patch(Circle((x, y), rr, color=color, alpha=a0 / n * 2.2, lw=0, zorder=z + k * 1e-3))


def scene():
    fig = plt.figure(figsize=(12, 12 * (YT - YB) / (XR - XL)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(XL, XR); ax.set_ylim(YB, YT)
    lattice(ax)
    character(ax, lens="empty", shadow=False)

    # thought bubble
    cx, cy, w, h = 4.45, 3.62, 5.95, 3.5
    cloud(ax, cx, cy, w, h)
    ax.add_patch(Ellipse((cx, cy - 0.05), w * 0.93, h * 0.88, fc=VAC_BG, ec="none", zorder=6.02))
    for (x, y, r) in ((0.75, 1.95, 0.11), (1.20, 2.30, 0.17), (1.78, 2.64, 0.24)):
        ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=2.2, zorder=6))

    ax.text(cx, cy + 1.18, "vacuum  +  obstacles", ha="center", va="center", fontsize=25,
            family="DejaVu Serif", style="italic", color="#2f4a63", zorder=7)

    # obstacles at the defect positions (same relative layout as in the crystal)
    ov = (cx - 1.55, cy + 0.38)      # vacancy  -> a pit
    oi = (cx - 1.95, cy - 0.70)      # interstitial -> small hard bump
    osb = (cx + 1.30, cy - 0.10)     # substitutional -> large bump
    halo(ax, *ov, 0.50, "#7d8a96", 7.0)
    ax.add_patch(Circle(ov, 0.22, fc="#dde5ec", ec="#7d8a96", lw=1.8, ls=(0, (3, 2.2)), zorder=7.05))
    halo(ax, *oi, 0.36, INT, 7.0)
    sphere(ax, *oi, 0.13, INT, z=7.05, n=16)
    halo(ax, *osb, 0.62, IMP, 7.0)
    sphere(ax, *osb, 0.27, IMP, z=7.05, n=22)

    # a free electron scattering off the substitutional obstacle
    ex, ey = cx - 0.55, cy - 0.32
    t = np.linspace(0, 1, 60)
    ax.plot(cx - 1.1 + (ex + 0.05 - (cx - 1.1)) * t, np.full_like(t, ey) + 0 * t,
            color="#9fb6cb", lw=2.0, ls=(0, (3, 2.5)), zorder=7.1)
    for k, dy in enumerate((-0.10, 0.0, 0.10)):
        ax.plot([ex - 0.62 + 0.10 * abs(k - 1), ex - 0.30], [ey + dy] * 2, color="#9fb6cb",
                lw=2.2, solid_capstyle="round", zorder=7.15)
    sphere(ax, ex, ey, 0.21, BODY, z=7.2, n=20)
    ax.add_patch(Circle((ex - 0.06, ey + 0.04), 0.032, color=INK, zorder=7.4))
    ax.add_patch(Circle((ex + 0.07, ey + 0.04), 0.032, color=INK, zorder=7.4))
    ax.add_patch(FancyArrowPatch((ex + 0.28, ey), (osb[0] - 0.42, osb[1] - 0.18),
                                 connectionstyle="arc3,rad=0.0",
                                 arrowstyle="-", lw=2.2, color=IMP, zorder=7.2))
    ax.add_patch(FancyArrowPatch((osb[0] - 0.42, osb[1] - 0.18), (osb[0] - 0.05, osb[1] + 0.85),
                                 connectionstyle="arc3,rad=-0.35",
                                 arrowstyle="-|>,head_length=8,head_width=4.5", lw=2.2,
                                 color=IMP, zorder=7.2))
    # outgoing scattered-wave arcs
    for rr in (0.75, 0.95):
        from matplotlib.patches import Arc
        ax.add_patch(Arc(osb, 2 * rr, 2 * rr, theta1=-60, theta2=40, lw=1.3, color=IMP,
                         alpha=0.55, zorder=7.0))

    ax.text(cx + 0.1, cy - 1.12, r"$H=\dfrac{p^2}{2m^{*}}+\sum_i V(\mathbf{r}-\mathbf{R}_i)$",
            ha="center", va="center", fontsize=17, color="#2f4a63", zorder=7.3)
    return fig


if __name__ == "__main__":
    fig = scene()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"electron_obstacles.{ext}"), dpi=300,
                    bbox_inches="tight", pad_inches=0.0, facecolor="white")
    print("done")
