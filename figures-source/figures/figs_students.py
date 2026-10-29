"""'For Students' variants of Fig 2 and Fig 3 (scientist electron as the protagonist)
and a square section-header mascot."""
import numpy as np
from PIL import Image
import figs
from common import SE, OUT, STREAK, ASSETS


def mascot(ax, x, y, r, lens, vel=(1, 0), z=6):
    """Scientist electron with body radius r centred at (x, y) in data coords of ax."""
    x0, x1, y0, y1 = -2.25, 2.35, -1.75, 2.15
    ins = ax.inset_axes([x + x0 * r, y + y0 * r, (x1 - x0) * r, (y1 - y0) * r], transform=ax.transData,
                        zorder=z)
    ins.set_xlim(x0, x1); ins.set_ylim(y0, y1); ins.set_aspect("equal"); ins.axis("off")
    ins.patch.set_alpha(0)
    SE.character(ins, lens=lens, shadow=False)
    ux, uy = vel
    for off in (-0.35, 0.0, 0.35):
        L = (0.9 - 0.25 * abs(off) / 0.35) * r * 1.6
        ax.plot([x - 1.15 * r, x - 1.15 * r - L], [y + off * r, y + off * r], color=STREAK, lw=2.4,
                solid_capstyle="round", zorder=z - 0.1)


def run(fn, name, sizes):
    calls = iter(sizes)
    orig_e, orig_s = figs.electron, figs.save

    def e(ax, x, y, r=0.36, vel=None, z=5):
        lens, rr = next(calls)
        mascot(ax, x, y, rr, lens)

    figs.electron = e
    figs.save = lambda fig, _n: orig_s(fig, name)
    try:
        fn()
    finally:
        figs.electron, figs.save = orig_e, orig_s


def header():
    im = Image.open(f"{ASSETS}/scientist_electron_transparent.png").convert("RGBA")
    bb = im.getbbox(); im = im.crop(bb)
    S = int(max(im.size) * 1.12)
    sq = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sq.paste(im, ((S - im.width) // 2, (S - im.height) // 2), im)
    sq = sq.resize((1600, 1600), Image.LANCZOS)
    sq.save(f"{OUT}/header_scientist_electron_transparent.png")
    bg = Image.new("RGBA", sq.size, (255, 255, 255, 255)); bg.alpha_composite(sq)
    bg.convert("RGB").save(f"{OUT}/header_scientist_electron_white.png")
    print("wrote header")


if __name__ == "__main__":
    run(figs.fig2, "fig2_perfect_crystal_students", [("lattice", 0.95), ("empty", 0.95)])
    run(figs.fig3, "fig3_imperfect_crystal_students", [("empty", 0.95)])
    header()
