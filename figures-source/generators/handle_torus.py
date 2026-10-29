"""BZ torus mapped into a 'classifying space' drawn as a sheet with a handle.

  nontrivial : the torus encircles one pillar of the handle; its winding
               cycle (orange) goes around the pillar (hidden part dashed)
  trivial    : the torus sits on the flat part; ghost copies shrink it to a point

Usage: python3 handle_torus.py OUTDIR
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from scipy.ndimage import minimum_filter, median_filter

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
TWO_PI = 2 * np.pi

AZ, EL = np.deg2rad(-62), np.deg2rad(24)
CP = np.array([np.cos(EL) * np.cos(AZ), np.cos(EL) * np.sin(AZ), np.sin(EL)])   # toward camera
RIGHT = np.array([-np.sin(AZ), np.cos(AZ), 0.0])
UP = np.cross(CP, RIGHT)
LIGHT = np.array([-0.4, -0.6, 0.9]); LIGHT /= np.linalg.norm(LIGHT)

INK = "#24303b"
SPACE = "#b9c9d8"      # background space
SPACE_LINE = "#7d8fa0"
TORUS = "#fbe3c4"
ORANGE = "#e07a3c"


def view(P):
    return P @ RIGHT, P @ UP, -(P @ CP)


# ------------------------------------------------------------------ geometry
A_SH, B_SH, NSE = 3.9, 2.7, 5.0          # superellipse sheet
ARCH_R, ARCH_Y = 1.6, 0.35               # handle: semicircle in the x-z plane


def sheet_z(x, y):
    s = (np.abs(x / A_SH) ** NSE + np.abs(y / B_SH) ** NSE) ** (1 / NSE)
    return -0.35 * np.clip(s - 0.72, 0, None) ** 2 / 0.28 ** 2 * 0.28


def sheet_inside(x, y):
    return np.abs(x / A_SH) ** NSE + np.abs(y / B_SH) ** NSE <= 1


def arch(s, th):
    """Tube around c(s) = (-R cos s, Y, R sin s); flared where it meets the sheet."""
    r = 0.36 + 0.30 * np.exp(-(s / 0.28) ** 2) + 0.30 * np.exp(-((s - np.pi) / 0.28) ** 2)
    c = np.stack([-ARCH_R * np.cos(s), ARCH_Y + 0 * s, ARCH_R * np.sin(s)], -1)
    n1 = np.stack([np.cos(s), 0 * s, -np.sin(s)], -1)
    n2 = np.stack([0 * s, 1 + 0 * s, 0 * s], -1)
    return c + r[..., None] * (np.cos(th)[..., None] * n1 + np.sin(th)[..., None] * n2)


def make_torus(center, axis, R=0.72, r=0.19):
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis)
    e1 = np.cross(axis, [0, 1, 0]) if abs(axis[1]) < 0.9 else np.cross(axis, [1, 0, 0])
    e1 /= np.linalg.norm(e1); e2 = np.cross(axis, e1)
    center = np.asarray(center, float)

    def fn(phi, th):     # phi: around the axis (the big cycle), th: around the tube
        rad = R + r * np.cos(th)
        return (center + rad[..., None] * (np.cos(phi)[..., None] * e1 + np.sin(phi)[..., None] * e2)
                + (r * np.sin(th))[..., None] * axis)
    return fn


def arch_frame(s0):
    c = np.array([-ARCH_R * np.cos(s0), ARCH_Y, ARCH_R * np.sin(s0)])
    t = np.array([np.sin(s0), 0, np.cos(s0)])
    return c, t


# ------------------------------------------------------------------ renderer
def normals(P, a, b):
    N = np.cross(np.gradient(P, a, axis=0), np.gradient(P, b, axis=1))
    return N / np.maximum(np.linalg.norm(N, axis=-1, keepdims=True), 1e-12)


def shade(N, base, amb=0.62):
    lam = np.abs(N @ LIGHT)
    spec = np.clip(N @ ((LIGHT + CP) / np.linalg.norm(LIGHT + CP)), 0, 1) ** 30
    base = np.array(to_rgb(base))
    return np.clip(base * (amb + (1 - amb) * lam)[..., None] + 0.35 * spec[..., None], 0, 1)


def scene(torus_fn, ghosts=()):
    """Return dense samples (P, rgb) of all surfaces and the line drawings."""
    samples = []
    # sheet
    xs = np.linspace(-A_SH, A_SH, 1900); ys = np.linspace(-B_SH, B_SH, 1300)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    P = np.stack([X, Y, sheet_z(X, Y)], -1)
    m = sheet_inside(X, Y)
    samples.append((P[m], shade(normals(P, xs, ys), SPACE)[m]))
    # handle
    ss = np.linspace(-0.45, np.pi + 0.45, 1900); tt = np.linspace(0, TWO_PI, 520)
    S, T = np.meshgrid(ss, tt, indexing="ij")
    P = arch(S, T)
    keep = P[..., 2] > -0.6
    samples.append((P[keep], shade(normals(P, ss, tt), SPACE)[keep]))
    # torus (optional: torus_fn=None draws the space alone)
    if torus_fn is not None:
        pp = np.linspace(0, TWO_PI, 1300); qq = np.linspace(0, TWO_PI, 420)
        PH, TH = np.meshgrid(pp, qq, indexing="ij")
        P = torus_fn(PH, TH)
        samples.append((P.reshape(-1, 3), shade(normals(P, pp, qq), TORUS, amb=0.72).reshape(-1, 3)))

    lines = []   # (points, visible-style, hidden-style, eps)
    faint = dict(color=SPACE_LINE, lw=0.7, zorder=2)
    # sheet grid
    t = np.linspace(-1, 1, 900)
    for x0 in np.arange(-3.5, 3.51, 0.5):
        y = t * B_SH; x = np.full_like(y, x0); ok = sheet_inside(x, y)
        if ok.sum() > 2:
            lines.append((np.stack([x[ok], y[ok], sheet_z(x[ok], y[ok])], -1), faint, None, 0.03))
    for y0 in np.arange(-2.5, 2.51, 0.5):
        x = t * A_SH; y = np.full_like(x, y0); ok = sheet_inside(x, y)
        if ok.sum() > 2:
            lines.append((np.stack([x[ok], y[ok], sheet_z(x[ok], y[ok])], -1), faint, None, 0.03))
    # handle grid
    s = np.linspace(-0.3, np.pi + 0.3, 900)
    for th0 in np.linspace(0, TWO_PI, 12, endpoint=False):
        P = arch(s, np.full_like(s, th0)); P = P[P[:, 2] > -0.05]
        lines.append((P, faint, None, 0.03))
    th = np.linspace(0, TWO_PI, 400)
    for s0 in np.linspace(0.25, np.pi - 0.25, 11):
        lines.append((arch(np.full_like(th, s0), th), faint, None, 0.03))
    # torus grid
    u = np.linspace(0, TWO_PI, 1200)
    if torus_fn is None:
        u = None
    blk = dict(color=INK, lw=0.9, zorder=5)
    if u is not None:
        for k in np.linspace(0, TWO_PI, 28, endpoint=False):
            lines.append((torus_fn(np.full_like(u, k), u), blk, None, 0.02))
        for k in np.linspace(0, TWO_PI, 10, endpoint=False):
            lines.append((torus_fn(u, np.full_like(u, k)), blk, None, 0.02))
        # highlighted cycle (the one that winds around the pillar)
        cyc = torus_fn(u, np.full_like(u, np.pi / 2))
        lines.append((cyc, dict(color=ORANGE, lw=3.0, zorder=7, solid_capstyle="round"),
                      dict(color=ORANGE, lw=1.8, zorder=1.5, ls=(0, (3, 2.5)), alpha=0.9), 0.02))
    # sheet boundary
    a = np.linspace(0, TWO_PI, 2000)
    bx = A_SH * np.sign(np.cos(a)) * np.abs(np.cos(a)) ** (2 / NSE) * 0.9995
    by = B_SH * np.sign(np.sin(a)) * np.abs(np.sin(a)) ** (2 / NSE) * 0.9995
    lines.append((np.stack([bx, by, sheet_z(bx, by)], -1), dict(color=INK, lw=1.8, zorder=6), None, 0.05))

    sil = [(arch, np.linspace(-0.3, np.pi + 0.3, 1200), np.linspace(0, TWO_PI, 500), 1.8, INK)]
    if torus_fn is not None:
        sil.append((torus_fn, np.linspace(0, TWO_PI, 1200), np.linspace(0, TWO_PI, 500), 1.7, INK))
    return samples, lines, sil, ghosts


def render(fname, torus_fn, ghosts=(), dot=None):
    samples, lines, sil, ghosts = scene(torus_fn, ghosts)
    P = np.concatenate([s[0] for s in samples]); C = np.concatenate([s[1] for s in samples])
    u, v, d = view(P)
    umin, umax, vmin, vmax = u.min() - 0.05, u.max() + 0.05, v.min() - 0.05, v.max() + 0.05
    W = 1200; pix = (umax - umin) / (W - 1); H = int((vmax - vmin) / pix) + 1
    iu = np.clip(((u - umin) / pix).astype(int), 0, W - 1)
    iv = np.clip(((v - vmin) / pix).astype(int), 0, H - 1)
    flat = iv * W + iu
    zb = np.full(H * W, np.inf); np.minimum.at(zb, flat, d); zb = zb.reshape(H, W)
    for _ in range(3):
        holes = ~np.isfinite(zb)
        zb = np.where(holes, minimum_filter(zb, size=3), zb)

    fig = plt.figure(figsize=(11, 11 * (vmax - vmin) / (umax - umin)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(umin, umax); ax.set_ylim(vmin, vmax)

    # shaded image of the front-most surface
    q = 2 * pix
    Wc, Hc = int((umax - umin) / q) + 1, int((vmax - vmin) / q) + 1
    cf = np.clip(((v - vmin) / q).astype(int), 0, Hc - 1) * Wc + np.clip(((u - umin) / q).astype(int), 0, Wc - 1)
    order = np.lexsort((d, cf))
    first = order[np.r_[True, cf[order][1:] != cf[order][:-1]]]
    img = np.zeros((Hc * Wc, 4)); img[cf[first], :3] = C[first]; img[cf[first], 3] = 1
    ax.imshow(img.reshape(Hc, Wc, 4), origin="lower", interpolation="bilinear", zorder=0,
              extent=(umin - q / 2, umin + (Wc - .5) * q, vmin - q / 2, vmin + (Hc - .5) * q))

    def visible(Q, e):
        uu, vv, dd = view(Q)
        i = np.clip(((uu - umin) / pix).astype(int), 0, W - 1)
        j = np.clip(((vv - vmin) / pix).astype(int), 0, H - 1)
        vis = dd <= zb[j, i] + e
        return uu, vv, median_filter(vis.astype(np.uint8), size=15, mode="nearest").astype(bool)

    def draw(Q, vs, hs, e):
        uu, vv, vis = visible(Q, e)
        for mask, st in ((vis, vs), (~vis, hs)):
            if st is not None:
                ax.plot(np.where(mask, uu, np.nan), np.where(mask, vv, np.nan), **st)

    for Q, vs, hs, e in lines:
        draw(Q, vs, hs, e)

    for fn, a, b, lw, col in sil:
        A2, B2 = np.meshgrid(a, b, indexing="ij")
        X = fn(A2, B2)
        g = np.cross(np.gradient(X, a, axis=0), np.gradient(X, b, axis=1)) @ CP
        cs = plt.figure().add_subplot().contour(b, a, g, levels=[0]); plt.close()
        for seg in cs.allsegs[0]:
            if len(seg) >= 5:
                Q = fn(seg[:, 1], seg[:, 0])
                if fn is arch:
                    Q = Q[Q[:, 2] > -0.02]
                    if len(Q) < 5:
                        continue
                draw(Q, dict(color=col, lw=lw, zorder=6), None, 0.15)

    # ghost tori (contraction to a point) and the final point
    for gfn in ghosts:
        a = np.linspace(0, TWO_PI, 600); b = np.linspace(0, TWO_PI, 300)
        A2, B2 = np.meshgrid(a, b, indexing="ij"); X = gfn(A2, B2)
        g = np.cross(np.gradient(X, a, axis=0), np.gradient(X, b, axis=1)) @ CP
        cs = plt.figure().add_subplot().contour(b, a, g, levels=[0]); plt.close()
        for seg in cs.allsegs[0]:
            if len(seg) >= 5:
                uu, vv, _ = view(gfn(seg[:, 1], seg[:, 0]))
                ax.plot(uu, vv, color=INK, lw=1.0, ls=(0, (3, 2.5)), alpha=0.55, zorder=6)
        uu, vv, _ = view(gfn(a, np.full_like(a, np.pi / 2)))
        ax.plot(uu, vv, color=ORANGE, lw=1.4, ls=(0, (3, 2.5)), alpha=0.8, zorder=6)
    if dot is not None:
        du, dv, _ = view(np.array(dot))
        ax.plot(du, dv, "o", ms=7, color=ORANGE, mec=INK, mew=1.2, zorder=8)

    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{fname}.{ext}"), dpi=300, bbox_inches="tight",
                    pad_inches=0.05, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    s0 = 0.62
    c, t = arch_frame(s0)
    render("handle_torus_nontrivial", make_torus(c, t))

    r_t = 0.19
    base = np.array([-0.15, -1.45, 0.0])
    tor = make_torus(base + [0, 0, r_t + 0.01], [0, 0, 1])
    ghosts, path = [], [(-1.65, -1.62, 0.55), (-2.45, -1.75, 0.28)]
    for gx, gy, sc in path:
        ghosts.append(make_torus([gx, gy, sheet_z(gx, gy) + r_t * sc + 0.01], [0, 0, 1],
                                 R=0.72 * sc, r=r_t * sc))
    dx, dy = -3.2, -1.85
    render("handle_torus_trivial", tor, ghosts, dot=(dx, dy, sheet_z(dx, dy) + 0.01))
    render("handle_space", None)
    print("done")
