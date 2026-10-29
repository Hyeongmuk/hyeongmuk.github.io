"""Website figure series (Physics Stories). Usage: python3 figs.py [1 2 ...]"""
import sys
import numpy as np
from PIL import Image
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse, Arc, FancyArrowPatch, Polygon
from common import *   # noqa

T2 = ASSETS      # bz_torus_*_tint.png  (generators/bz_torus2.py)
IMG = ASSETS     # handle_torus_*.png   (generators/handle_torus.py)


def place(fig, path, cx, cy, w, crop=None):
    """Put an image centred at figure-fraction (cx, cy) with figure-fraction width w."""
    im = Image.open(path).convert("RGBA")
    if crop:
        im = im.crop(crop)
    W, H = fig.get_size_inches()
    h = w * (im.height / im.width) * (W / H)
    ax = fig.add_axes([cx - w / 2, cy - h / 2, w, h]); ax.axis("off")
    ax.imshow(np.asarray(im), interpolation="lanczos")
    return ax, h


def zoom(fig, ov, path, src_xy, src_r, cx, cy, rad, anchor):
    """Circular magnifier of a local patch, connected to an anchor point."""
    im = Image.open(path).convert("RGBA")
    x, y = src_xy
    patch = np.asarray(im.crop((x - src_r, y - src_r, x + src_r, y + src_r)))
    W, H = fig.get_size_inches()
    ax = fig.add_axes([cx - rad, cy - rad * W / H, 2 * rad, 2 * rad * W / H]); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    img = ax.imshow(patch, extent=(0, 1, 0, 1), interpolation="lanczos")
    c = Circle((0.5, 0.5), 0.5, transform=ax.transData); img.set_clip_path(c)
    ax.add_patch(Circle((0.5, 0.5), 0.497, fill=False, ec=NAVY, lw=1.6))
    ov.plot([anchor[0], cx], [anchor[1], cy + rad * W / H], color=NAVY, lw=1.0, ls=(0, (2, 2)))
    ov.add_patch(Circle(anchor, 0.006, fc="white", ec=NAVY, lw=1.2, transform=ov.transData))


# ---------------------------------------------------------------- Figure 1
def fig1():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(); ov = canvas(fig)
    heading(ov, 0.25, 0.90, "Topology", "global structure")
    heading(ov, 0.75, 0.90, "Geometry", "local shape")
    ov.plot([0.5, 0.5], [0.16, 0.92], color="#e3e7eb", lw=1.2)
    # topology: round torus = twisted torus (same number of holes)
    place(fig, f"{T2}/bz_torus_round_tint.png", 0.135, 0.62, 0.20)
    place(fig, f"{T2}/bz_torus_twisted_tint.png", 0.365, 0.62, 0.20)
    ov.text(0.25, 0.62, "=", ha="center", va="center", fontsize=30, color=NAVY)
    ov.text(0.25, 0.42, "same number of holes", ha="center", fontsize=fs(12.5), color=GRAY)
    # geometry: same objects, different local patches
    place(fig, f"{T2}/bz_torus_round_tint.png", 0.635, 0.62, 0.20)
    place(fig, f"{T2}/bz_torus_hotspot_tint.png", 0.865, 0.62, 0.20)
    ov.text(0.75, 0.62, "≠", ha="center", va="center", fontsize=30, color=NAVY)
    # anchors in figure fraction: image width 0.20 centred; pixel -> fraction
    def frac(cx, cy, px, py, w=0.20, iw=2923, ih=1610):
        W, H = fig.get_size_inches(); h = w * ih / iw * W / H
        return cx - w / 2 + w * px / iw, cy + h / 2 - h * py / ih
    zoom(fig, ov, f"{T2}/bz_torus_round_tint.png", (1460, 1020), 300, 0.635, 0.30, 0.045,
         frac(0.635, 0.62, 1460, 1020))
    zoom(fig, ov, f"{T2}/bz_torus_hotspot_tint.png", (2400, 900), 280, 0.865, 0.30, 0.045,
         frac(0.865, 0.62, 2400, 900))
    ov.text(0.75, 0.30, "local\npatches", ha="center", va="center", fontsize=fs(11.5), color=GRAY, linespacing=1.3)
    ov.text(0.5, 0.075, "Same energy band  ε(k)  —  different wave-function structure",
            ha="center", va="center", fontsize=fs(13.5), color=NAVY)
    save(fig, "fig1_topology_vs_geometry")


# ---------------------------------------------------------------- Figure 2
A, RA = 2.0, 0.30


def fig2():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(); ov = canvas(fig)
    heading(ov, 0.255, 0.82, "Perfect crystal")
    heading(ov, 0.745, 0.82, "Effective vacuum", "as seen by the Bloch electron")
    # left: lattice with an unobstructed electron
    H = 5 * A
    axL = panel_axes(fig, [0.04, 0.17, 0.43, 0.43 * 12 / 6.75 * H / (7 * A)], (0, 7 * A), (0, H))
    y0, y1 = axL.get_ylim()
    perfect_lattice(axL, 7, 5, A, RA)
    yy = 3 * A
    path(axL, [(0.35 * A, yy), (6.85 * A, yy)])
    electron(axL, 3.0 * A, yy, r=0.42, vel=(1, 0), z=6)
    axL.text(3.5 * A, 2 * A, "Bloch electron", ha="center", va="center", fontsize=fs(12), color=NAVY, zorder=8,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.95))
    frame(axL)
    # right: the same electron in an empty medium
    axR = panel_axes(fig, [0.53, 0.17, 0.43, 0.43 * 12 / 6.75 * H / (7 * A)], (0, 7 * A), (y0, y1))
    path(axR, [(0.35 * A, yy), (6.85 * A, yy)])
    electron(axR, 3.0 * A, yy, r=0.42, vel=(1, 0), z=6)
    axR.text(3.5 * A, 2 * A, "effective mass  m*", ha="center", va="center", fontsize=fs(12), color=NAVY)
    frame(axR, fc=VAC_BG)
    ov.text(0.745, 0.10, "no scattering · crystal momentum conserved", ha="center", fontsize=fs(12), color=GRAY)
    flow_arrow(ov, 0.478, 0.522, 0.17 + 0.43 * 12 / 6.75 * 5 / 14 / 2)
    save(fig, "fig2_perfect_crystal")


# ---------------------------------------------------------------- Figure 3
def defect_lattice(ax):
    EO.lattice(ax)                         # strained lattice with vacancy / impurity / interstitial


def fig3():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(); ov = canvas(fig)
    heading(ov, 0.255, 0.93, "Imperfect crystal")
    heading(ov, 0.745, 0.93, "Effective medium", "vacuum + localized obstacles")
    xl, xr = -6.3, 8.4
    yl = -5.4; yr = yl + (xr - xl) * (0.70 / 0.43) * (6.75 / 12)
    axL = panel_axes(fig, [0.04, 0.12, 0.43, 0.70], (xl, xr), (yl, yr))
    defect_lattice(axL)
    vac, sub, inter = EO.site(EO.VAC), EO.site(EO.SUB), EO.site(EO.INTER)
    # labels sit halfway between atom rows (spacing EO.A_LAT) so their white boxes never cover atoms
    lab = dict(fontsize=fs(11.5), color=NAVY, zorder=9, va="center",
               bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.92))
    axL.annotate("vacancy", xy=tuple(vac), xytext=(vac[0] + 0.2, vac[1] + EO.A_LAT / 2), ha="center",
                 arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9, shrinkB=9), **lab)
    axL.annotate("impurity", xy=tuple(sub), xytext=(sub[0] - 0.2, sub[1] - EO.A_LAT / 2), ha="center",
                 arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9, shrinkB=11), **lab)
    axL.annotate("interstitial", xy=tuple(inter), xytext=(inter[0] + 0.3, inter[1] - EO.A_LAT), ha="center",
                 arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9, shrinkB=6), **lab)
    frame(axL)
    # right: obstacles at the defect positions, electron scattering off the impurity
    axR = panel_axes(fig, [0.53, 0.12, 0.43, 0.70], (xl, xr), (yl, yr))
    EO.halo(axR, *vac, 1.0, "#7d8a96", 1.0)
    axR.add_patch(Circle(tuple(vac), 0.42, fc="#dde5ec", ec="#7d8a96", lw=1.6, ls=(0, (3, 2.2)), zorder=1.1))
    EO.halo(axR, *inter, 0.75, INK, 1.0)
    sphere(axR, *inter, 0.22, "#4a5560", z=1.1, n=16)
    EO.halo(axR, *sub, 1.3, ORANGE, 1.0)
    sphere(axR, *sub, 0.45, ORANGE, z=1.1, n=22)
    # trajectory: comes in from the left, deflects at the impurity
    yin = sub[1] + 0.15
    t = np.linspace(0, 1, 60)
    p_in = np.stack([xl + 0.8 + (sub[0] - 0.95 - xl - 0.8) * t, np.full_like(t, yin)], -1)
    ang = np.deg2rad(52)
    p_out = np.stack([sub[0] - 0.95 + 0.35 * np.sin(np.pi * t / 2) + t * 3.6 * np.cos(ang),
                      yin + t * 3.6 * np.sin(ang)], -1)
    path(axR, p_in, arrow=False)
    path(axR, np.concatenate([p_in[-1:], p_out]))
    electron(axR, p_in[30, 0], yin, r=0.36, vel=(1, 0), z=6)
    for rr in (1.65, 2.05):
        axR.add_patch(Arc(tuple(sub), 2 * rr, 2 * rr, theta1=-70, theta2=40, lw=1.3, color=ORANGE, alpha=0.5))
    axR.text(sub[0] + 0.2, sub[1] + 3.6, "scattering", ha="center", fontsize=fs(12), color=ORANGE)
    frame(axR, fc=VAC_BG)
    flow_arrow(ov, 0.478, 0.522, 0.47)
    save(fig, "fig3_imperfect_crystal")


# ---------------------------------------------------------------- Figure 4
def fig4():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(w=12, h=5.0); ov = canvas(fig)
    ov.text(0.5, 0.88, "Same topology", ha="center", fontsize=fs(17), fontweight="semibold", color=NAVY)
    ov.text(0.5, 0.80, "one hole · one Brillouin-zone torus", ha="center", fontsize=fs(12), color=GRAY)
    for k, n in enumerate(["round", "aniso", "hotspot", "twisted"]):
        place(fig, f"{T2}/bz_torus_{n}_tint.png", 0.13 + 0.248 * k, 0.47, 0.235)
    ov.add_patch(FancyArrowPatch((0.06, 0.17), (0.94, 0.17), arrowstyle="<|-|>,head_length=8,head_width=4",
                                 lw=1.4, color=ORANGE))
    ov.text(0.5, 0.10, "different geometry  —  quantum metric varies from point to point",
            ha="center", va="center", fontsize=fs(13), color=NAVY)
    save(fig, "fig4_same_topology_different_geometry")


# ---------------------------------------------------------------- Figure 5
def wavy(ax, p, q, z, amp=0.09, n_wav=4, color="#c98793", lw=1.7, t0=0.22, t1=0.78):
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p; L = np.linalg.norm(d); u = d / L; nr = np.array([-u[1], u[0]])
    t = np.linspace(t0, t1, 160)
    pts = p[None] + t[:, None] * d[None] + (amp * np.sin(2 * np.pi * n_wav * (t - t0)))[:, None] * nr[None]
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, alpha=0.9, zorder=z, solid_capstyle="round")


def fig5():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(); ov = canvas(fig)
    heading(ov, 0.255, 0.93, "Single electron", "band structure")
    heading(ov, 0.745, 0.93, "Many electrons", "correlated quantum matter")
    ylim = (0, 0.7 / 0.43 * 6.75 / 12 * 7 * A)
    axL = panel_axes(fig, [0.04, 0.12, 0.43, 0.70], (0, 7 * A), ylim)
    perfect_lattice(axL, 7, int(ylim[1] / A) + 1, A, RA)
    path(axL, [(0.35 * A, 3 * A), (6.4 * A, 3 * A)])
    electron(axL, 3.5 * A, 3 * A, r=0.42, vel=(1, 0), z=6)
    frame(axL)
    axR = panel_axes(fig, [0.53, 0.12, 0.43, 0.70], (0, 7 * A), ylim)
    perfect_lattice(axR, 7, int(ylim[1] / A) + 1, A, RA)
    # electrons sit in cell centres; soft collective pattern (triangular-ish) with interactions
    cells = [(1, 1), (3, 1), (5, 1), (2, 3), (4, 3), (6, 3), (1, 5), (3, 5), (5, 5)]
    P = [((i) * A, (j) * A) for i, j in cells]
    P = [(x + 0.12 * np.sin(1.7 * k), y + 0.12 * np.cos(1.3 * k)) for k, (x, y) in enumerate(P)]
    vel = [(np.cos(2.1 * k), np.sin(2.1 * k)) for k in range(len(P))]
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if np.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1]) < 2.4 * A:
                wavy(axR, P[i], P[j], z=1.5)
    for (x, y) in P:
        axR.add_patch(Circle((x, y), 0.95, fc=ORANGE, alpha=0.07, lw=0, zorder=1.2))
    for (x, y), v in zip(P, vel):
        electron(axR, x, y, r=0.36, vel=v, z=6)
    frame(axR)
    flow_arrow(ov, 0.478, 0.522, 0.47)
    ov.text(0.5, 0.065, "other electrons become part of each electron's world", ha="center",
            fontsize=fs(12), color=GRAY)
    save(fig, "fig5_many_electrons")


# ---------------------------------------------------------------- Figure 6
def fig6():
    text_scale(WEB_TEXT_SCALE)
    fig = figure(w=12, h=5.2); ov = canvas(fig)
    heading(ov, 0.5, 0.91, "State space with a hole", size=17)
    _, h = place(fig, f"{IMG}/handle_torus_nontrivial.png", 0.265, 0.50, 0.45)
    place(fig, f"{IMG}/handle_torus_trivial.png", 0.735, 0.50, 0.45)
    ov.text(0.265, 0.50 + h / 2 + 0.02, "topological", ha="center", fontsize=fs(15), fontweight="semibold", color=ORANGE)
    ov.text(0.735, 0.50 + h / 2 + 0.02, "trivial", ha="center", fontsize=fs(15), fontweight="semibold", color=NAVY)
    ov.text(0.265, 0.50 - h / 2 - 0.035, "winding around the hole — cannot be undone", ha="center",
            fontsize=fs(12), color=GRAY)
    ov.text(0.735, 0.50 - h / 2 - 0.035, "no winding — shrinks to a point", ha="center", fontsize=fs(12), color=GRAY)
    ov.plot([0.5, 0.5], [0.18, 0.80], color="#e3e7eb", lw=1.2)
    save(fig, "fig6_real_hopf_winding")


# ---------------------------------------------------------------- Figure 7
def curl(ax, c, r, th0, color, lw=2.2, z=6, span=290, asp=1.0, head=7):
    """Circular arrow; asp = (data-y units per data-x unit) correction for non-square axes."""
    ax.add_patch(Arc(c, 2 * r, 2 * r * asp, theta1=th0, theta2=th0 + span, lw=lw, color=color, zorder=z))
    t = np.deg2rad(th0 + span)
    p = (c[0] + r * np.cos(t), c[1] + r * asp * np.sin(t))
    d = np.array([-np.sin(t), np.cos(t) * asp])
    e = 0.3 * r
    ax.add_patch(FancyArrowPatch((p[0] - 0.05 * e * d[0], p[1] - 0.05 * e * d[1]), (p[0] + e * d[0], p[1] + e * d[1]),
                                 arrowstyle=f"-|>,head_length={head},head_width={head * 0.6}", lw=0, color=color,
                                 zorder=z, mutation_scale=1.0, shrinkA=0, shrinkB=0))


def metric_glyph(ax, c, a, b, ang, z=7, asp=1.0):
    t = np.deg2rad(ang)
    th = np.linspace(0, 2 * np.pi, 120)
    x = c[0] + a * np.cos(th) * np.cos(t) - b * np.sin(th) * np.sin(t)
    y = c[1] + (a * np.cos(th) * np.sin(t) + b * np.sin(th) * np.cos(t)) * asp
    ax.fill(x, y, fc="white", ec=NAVY, lw=1.8, alpha=0.95, zorder=z)
    for L, (dx, dy) in ((a, (np.cos(t), np.sin(t))), (b, (-np.sin(t), np.cos(t)))):
        ax.plot([c[0] - L * dx, c[0] + L * dx], [c[1] - L * dy * asp, c[1] + L * dy * asp], color=NAVY, lw=1.0,
                zorder=z + 0.1)


def tesseract(ax, c, s_out, s_in, z=2):
    """Cube-in-cube projection of the 4-cube; back edges light, front edges dark."""
    def cube(s, off):
        ox, oy = off
        f = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * s + np.array(c)
        b = f + np.array([ox, oy])
        return f, b
    of, ob = cube(s_out, (0.34 * s_out, 0.30 * s_out))
    inf, inb = cube(s_in, (0.34 * s_in, 0.30 * s_in))
    for poly, fc in ((ob, None), (of, "#fbe9d2")):
        if fc:
            ax.add_patch(Polygon(poly, closed=True, fc=fc, ec="none", alpha=0.55, zorder=z - 1))
    def edges(f, b, col_f, col_b, lw):
        for i in range(4):
            j = (i + 1) % 4
            ax.plot(*zip(b[i], b[j]), color=col_b, lw=lw * 0.8, zorder=z)
            ax.plot(*zip(f[i], b[i]), color=col_b if i in (0, 3) else col_f, lw=lw * 0.9, zorder=z + 0.1)
        for i in range(4):
            j = (i + 1) % 4
            ax.plot(*zip(f[i], f[j]), color=col_f, lw=lw, zorder=z + 0.2)
    edges(inf, inb, "#8f6a45", "#e0cdb8", 1.3)
    for P, Q in ((of, inf), (ob, inb)):
        for i in range(4):
            ax.plot(*zip(P[i], Q[i]), color="#d4c2ad", lw=1.0, zorder=z - 0.5)
    edges(of, ob, INK, LIGHT, 1.7)


def fig7():
    text_scale(1.0)
    fig = figure(); ov = canvas(fig)
    heading(ov, 0.255, 0.92, "Chern band", "Kähler geometry")
    heading(ov, 0.745, 0.92, "Kramers pair", "quaternion-Kähler geometry")
    ov.plot([0.5, 0.5], [0.12, 0.86], color="#e3e7eb", lw=1.2)
    # left: 2D BZ torus with one curvature and the metric
    _, h = place(fig, f"{T2}/bz_torus_round_tint.png", 0.255, 0.54, 0.36)
    axL = fig.add_axes([0.075, 0.54 - h / 2, 0.36, h]); axL.set_xlim(0, 1); axL.set_ylim(0, 1); axL.axis("off")
    axL.patch.set_alpha(0)
    W, Hh = fig.get_size_inches()
    aL = (0.36 * W) / (h * Hh)
    aO = W / Hh
    metric_glyph(axL, (0.5, 0.26), 0.06, 0.035, 8, asp=aL * 0.55)
    curl(axL, (0.5, 0.26), 0.12, 200, ORANGE, asp=aL * 0.55)
    ov.text(0.255, 0.54 - h / 2 - 0.03, "2D Brillouin zone", ha="center", fontsize=12.5, color=NAVY)
    lg = 0.54 - h / 2 - 0.10
    metric_glyph(ov, (0.13, lg), 0.011, 0.007, 0, asp=aO)
    ov.text(0.147, lg, "quantum metric g", va="center", fontsize=12, color=NAVY)
    curl(ov, (0.30, lg), 0.009, 200, ORANGE, lw=1.8, asp=aO, head=6)
    ov.text(0.317, lg, "Berry curvature", va="center", fontsize=12, color=NAVY)
    ov.text(0.255, 0.07, "→ fractional Chern insulators", ha="center", fontsize=12.5, color=GRAY)
    # right: 4D BZ (tesseract) with three coupled curvatures
    axR = fig.add_axes([0.56, 0.24, 0.37, 0.58]); axR.axis("off")
    asp = (0.58 * Hh) / (0.37 * W)
    axR.set_xlim(0, 1); axR.set_ylim(0, asp); axR.set_aspect("equal")
    cc = (0.43, 0.43 * asp + 0.02)
    tesseract(axR, cc, 0.30, 0.14)
    ctr = (cc[0] + 0.024, cc[1] + 0.021)
    metric_glyph(axR, ctr, 0.055, 0.034, 8, z=9)
    for r, th, col in ((0.105, 200, ORANGE), (0.145, 80, GREEN), (0.185, -40, BODY)):
        curl(axR, ctr, r, th, col, z=8, span=250)
    ov.text(0.745, 0.215, "4D Brillouin zone", ha="center", fontsize=12.5, color=NAVY)
    metric_glyph(ov, (0.60, 0.145), 0.011, 0.007, 0, asp=aO)
    ov.text(0.617, 0.145, "quantum metric g", va="center", fontsize=12, color=NAVY)
    for k, col in enumerate((ORANGE, GREEN, BODY)):
        curl(ov, (0.762 + 0.024 * k, 0.145), 0.009, 200, col, lw=1.6, asp=aO, head=6)
    ov.text(0.835, 0.145, "three coupled\nBerry curvatures", va="center", fontsize=12, color=NAVY, linespacing=1.15)
    ov.text(0.745, 0.07, "→ time-reversal-symmetric correlated phases", ha="center", fontsize=12.5, color=GRAY)
    flow_arrow(ov, 0.478, 0.522, 0.54)
    save(fig, "fig7_quaternion_kahler")


FIGS = {"1": fig1, "2": fig2, "3": fig3, "4": fig4, "5": fig5, "6": fig6, "7": fig7}
if __name__ == "__main__":
    for k in (sys.argv[1:] or list(FIGS)):
        FIGS[k]()
