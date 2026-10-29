"""Same topology (T^2 Brillouin zone), very different local geometry.

Every grid line is a line of constant k_x or k_y on a uniform k-grid, so the
size and shape of each cell shows the pulled-back metric g_ij(k) at that point.
Optional tint: area density sqrt(det g)(k) relative to its mean.

Shapes
  round    : standard torus of revolution (reference)
  hotspot  : metric concentrated near one k-point (big bulge, big cells),
             tube pinched and cells shrunk elsewhere
  aniso    : strongly anisotropic metric: elongated major circle, flattened
             tube; cells long in one direction, short in the other
  twisted  : saddle-shaped core curve, three-lobed tube whose elliptic cross
             section rotates once around the torus; cells sheared (g_xy != 0)

Usage: python3 bz_torus2.py OUTDIR
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import minimum_filter, median_filter

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
ELEV, AZIM = np.deg2rad(28), np.deg2rad(-90)
TWO_PI = 2 * np.pi


def tube(th, ph, cx, cy, cz, nx, ny, a, b, psi):
    """Point on a tube around core curve (cx,cy,cz)(ph) with horizontal
    in-plane normal (nx,ny), elliptic cross-section (a,b) rotated by psi."""
    u0, w0 = a * np.cos(th), b * np.sin(th)
    u = u0 * np.cos(psi) - w0 * np.sin(psi)
    w = u0 * np.sin(psi) + w0 * np.cos(psi)
    return np.stack([cx + u * nx, cy + u * ny, cz + w], -1)


def shape_round(kx, ky):
    th, ph = kx, ky
    return tube(th, ph, np.cos(ph), np.sin(ph), 0 * ph, np.cos(ph), np.sin(ph),
                0.52, 0.52, 0 * ph)


def shape_hotspot(kx, ky):
    # reparametrisation: dk -> large angle near the hot spot (th0, ph0)
    th0, ph0 = 0.35, 1.5 * np.pi - 0.45   # right side, upper outer flank
    th = kx + 0.6 * np.sin(kx - th0)
    ph = ky + 0.6 * np.sin(ky - ph0)
    G = np.exp((np.cos(th - th0) - 1) / 0.6 ** 2 + (np.cos(ph - ph0) - 1) / 0.45 ** 2)
    R = 1.0 + 0.15 * G
    r = 0.28 + 0.62 * G
    return tube(th, ph, R * np.cos(ph), R * np.sin(ph), 0.12 * G,
                np.cos(ph), np.sin(ph), r, r, 0 * ph)


def shape_aniso(kx, ky):
    th, ph = kx, ky
    A, B = 0.70, 1.55                       # elliptic core curve (long axis across the view)
    cx, cy = A * np.cos(ph), B * np.sin(ph)
    nx, ny = B * np.cos(ph), A * np.sin(ph)
    nn = np.hypot(nx, ny)
    return tube(th, ph, cx, cy, 0 * ph, nx / nn, ny / nn, 0.50, 0.20, 0 * ph)


def shape_twisted(kx, ky):
    th, ph = kx, ky + 0.25 * np.sin(2 * ky)
    R = 1.05 + 0.10 * np.cos(3 * ph)
    cz = 0.36 * np.sin(2 * ph)              # saddle ("potato chip") core
    lobe = 1 + 0.30 * np.cos(3 * ph + 0.8)  # three-lobed tube thickness
    return tube(th, ph, R * np.cos(ph), R * np.sin(ph), cz,
                np.cos(ph), np.sin(ph), 0.46 * lobe, 0.26 * lobe, ph)


SHAPES = {"round": shape_round, "hotspot": shape_hotspot,
          "aniso": shape_aniso, "twisted": shape_twisted}


def view(P):
    ca, sa, ce, se = np.cos(AZIM), np.sin(AZIM), np.cos(ELEV), np.sin(ELEV)
    x, y, z = P[..., 0], P[..., 1], P[..., 2]
    xr = ca * x + sa * y
    yr = -sa * x + ca * y
    return xr, yr * se + z * ce, yr * ce - z * se   # u, v (screen), depth


def frame_of(fn):
    k1, k2 = np.meshgrid(np.linspace(0, TWO_PI, 500), np.linspace(0, TWO_PI, 900))
    u, v, _ = view(fn(k1, k2))
    return u.min(), u.max(), v.min(), v.max()


CMAP = LinearSegmentedColormap.from_list(
    "dens", ["#e8f1f8", "#ffffff", "#fde9c9", "#f6b26b", "#e06c3c"])


def render(name, fn, frame, tint):
    umin, umax, vmin, vmax = frame
    nth, nph = 2000, 4200
    k1 = np.linspace(0, TWO_PI, nth, endpoint=False)
    k2 = np.linspace(0, TWO_PI, nph, endpoint=False)
    K1, K2 = np.meshgrid(k1, k2, indexing="ij")
    S = fn(K1, K2)
    u, v, d = view(S)
    W = 1000
    pix = (umax - umin) / (W - 1)
    H = int((vmax - vmin) / pix) + 1
    iu = np.clip(((u - umin) / pix).astype(int), 0, W - 1).ravel()
    iv = np.clip(((v - vmin) / pix).astype(int), 0, H - 1).ravel()
    flat = iv * W + iu
    zb = np.full(H * W, np.inf)
    np.minimum.at(zb, flat, d.ravel())
    zb = zb.reshape(H, W)
    holes = ~np.isfinite(zb)
    for _ in range(3):                      # close sampling holes
        holes = ~np.isfinite(zb)
        zb = np.where(holes, minimum_filter(zb, size=3), zb)

    def visible(P, e=0.035):
        uu, vv, dd = view(P)
        i = np.clip(((uu - umin) / pix).astype(int), 0, W - 1)
        j = np.clip(((vv - vmin) / pix).astype(int), 0, H - 1)
        vis = dd <= zb[j, i] + e
        return uu, vv, median_filter(vis.astype(np.uint8), size=21, mode="wrap").astype(bool)

    fw = 8 * (umax - umin + 0.2) / 3.6
    fig = plt.figure(figsize=(fw, fw * (vmax - vmin + 0.2) / (umax - umin + 0.2)))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(umin - 0.1, umax + 0.1); ax.set_ylim(vmin - 0.1, vmax + 0.1)

    if tint:
        # area density sqrt(det g) on the k-grid, plus soft Lambert shading
        X1 = np.gradient(S, k1, axis=0); X2 = np.gradient(S, k2, axis=1)
        N = np.cross(X1, X2)
        dens = np.linalg.norm(N, axis=-1)
        logd = np.log(dens / dens.mean())
        c = np.clip(0.5 + logd / 4.0, 0, 1)            # log scale, mean -> 0.5
        n_hat = N / np.linalg.norm(N, axis=-1, keepdims=True)
        light = np.array([-0.35, -0.55, 0.75]); light /= np.linalg.norm(light)
        shade = 0.80 + 0.20 * np.abs(n_hat @ light)
        rgb = CMAP(c.ravel())[:, :3] * shade.ravel()[:, None]
        # pick the front-most sample in each (coarser) bin
        q = 2.5 * pix
        Wc, Hc = int((umax - umin) / q) + 1, int((vmax - vmin) / q) + 1
        cu = np.clip(((u - umin) / q).astype(int), 0, Wc - 1).ravel()
        cv = np.clip(((v - vmin) / q).astype(int), 0, Hc - 1).ravel()
        cf = cv * Wc + cu
        order = np.lexsort((d.ravel(), cf))
        first = order[np.r_[True, cf[order][1:] != cf[order][:-1]]]
        img = np.ones((Hc * Wc, 4)); img[:, 3] = 0
        img[cf[first], :3] = rgb[first]; img[cf[first], 3] = 1
        img = img.reshape(Hc, Wc, 4)
        ax.imshow(img, origin="lower", extent=(umin - q / 2, umin + (Wc - .5) * q,
                  vmin - q / 2, vmin + (Hc - .5) * q), interpolation="bilinear", zorder=0)

    s = np.linspace(0, TWO_PI, 1600)
    lines = [fn(s, np.full_like(s, k)) for k in np.linspace(0, TWO_PI, 26, endpoint=False)]
    lines += [fn(np.full_like(s, k), s) for k in np.linspace(0, TWO_PI, 18, endpoint=False)]

    def draw(P, vs, hs, e=0.035):
        uu, vv, vis = visible(P, e)
        for mask, st in ((~vis, hs), (vis, vs)):
            if st is not None:
                ax.plot(np.where(mask, uu, np.nan), np.where(mask, vv, np.nan),
                        solid_capstyle="round", **st)

    hid = None if tint else dict(color="#b9c8d6", lw=0.55, zorder=1)
    for P in lines:
        draw(P, dict(color="black", lw=1.1, zorder=3), hid)

    # silhouette
    t2 = np.linspace(0, TWO_PI, 800); p2 = np.linspace(0, TWO_PI, 1600)
    T2, P2 = np.meshgrid(t2, p2, indexing="ij")
    X = fn(T2, P2)
    Nn = np.cross(np.gradient(X, t2, axis=0), np.gradient(X, p2, axis=1))
    ca, sa, ce, se = np.cos(AZIM), np.sin(AZIM), np.cos(ELEV), np.sin(ELEV)
    g = Nn @ np.array([-sa * ce, ca * ce, -se])
    cs = plt.figure().add_subplot().contour(p2, t2, g, levels=[0]); plt.close()
    for seg in cs.allsegs[0]:
        if len(seg) >= 5:
            draw(fn(seg[:, 1], seg[:, 0]), dict(color="black", lw=1.9, zorder=4), None, e=0.18)

    tag = "_tint" if tint else ""
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"bz_torus_{name}{tag}.{ext}"), dpi=300,
                    facecolor="white", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    which = sys.argv[2:] or list(SHAPES)
    b = np.array([frame_of(f) for f in SHAPES.values()])
    FRAME = (b[:, 0].min() - .02, b[:, 1].max() + .02, b[:, 2].min() - .02, b[:, 3].max() + .02)
    for nm in which:
        for tint in (False, True):
            render(nm, SHAPES[nm], FRAME, tint)
        print("wrote", nm)
