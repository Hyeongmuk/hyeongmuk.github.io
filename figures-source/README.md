# Website figure series — editable source

Source code for the illustration series on Hyeongmuk Lim's research website
(topology vs. geometry of Bloch bands, the "scientist electron" mascot, real Hopf
insulator, quaternion-Kähler geometry). Everything is plain Python + matplotlib.
No image is hand-edited, so every figure can be changed by editing code and re-running it.

> 이 폴더만 있으면 어디서든 재생성됩니다. 그림을 고칠 때는 PNG를 직접 편집하지 말고 아래 스크립트를 수정한 뒤 다시 실행하세요.

## Quick start

```bash
pip install -r requirements.txt          # numpy scipy matplotlib pillow
# the Inter font must be installed (fonts-inter on Debian/Ubuntu, or https://rsms.me/inter)
./build_all.sh                           # ~1 min: figures from the pre-rendered assets/
./build_all.sh --assets                  # ~2.5 min: also re-render assets/ from scratch
cd figures && python3 figs.py 3 5        # rebuild only fig3 and fig5
FIG_OUT=/some/dir python3 figs.py        # write somewhere other than out/
```

Builds are deterministic. Running `./build_all.sh --assets` on a clean copy reproduces
the delivered PNGs exactly (pixel-identical).

## Layout and dependency graph

```
lib/                      character + crystal drawing primitives (2-D matplotlib patches)
  scientist_electron.py   sphere(), character(ax, lens="lattice"|"empty", shadow, spin)
  electron_vacuum.py      lattice(), cloud(), VAC_BG          (imports scientist_electron)
  electron_obstacles.py   site(), strain(), lattice(), halo() (imports both above)
generators/               3-D surfaces rendered to PNG (custom z-buffer renderer)
  bz_torus2.py            Brillouin-zone tori: SHAPES = round / hotspot / aniso / twisted
  handle_torus.py         background space with a handle + torus (nontrivial / trivial)
assets/                   pre-rendered outputs of generators/ and lib/ (inputs to figures/)
figures/
  common.py               shared style: palette, fonts, canvas, heading(), frame(), electron(), save()
  figs.py                 fig1() ... fig7()   -> out/figN_*.png
  figs_students.py        variants of fig2/fig3 with the mascot + square section header
out/                      final PNGs (the current delivered versions are already here)
build_all.sh, requirements.txt
```

Data flow:

```
generators/bz_torus2.py   --> assets/bz_torus_{round,hotspot,aniso,twisted}_tint.png --> fig1, fig4, fig7
generators/handle_torus.py --> assets/handle_torus_{nontrivial,trivial}.png           --> fig6
lib/scientist_electron.py  --> assets/scientist_electron_transparent.png              --> header mascot
lib/*  (imported live by figures/common.py as SE, EV, EO)                            --> fig2, fig3, fig5, students
```

If you change a generator (e.g. a torus shape), run `./build_all.sh --assets` so the
change reaches the figures. Changes to `lib/` take effect on the next `figs.py` run.

## Figures

| output | function | content |
|---|---|---|
| fig1_topology_vs_geometry | `fig1` | left: round torus → twisted torus (same topology); right: round vs. hotspot torus with circular magnifiers (`zoom`) showing different local geometry |
| fig2_perfect_crystal | `fig2` | perfect lattice → "effective vacuum as seen by the Bloch electron" |
| fig3_imperfect_crystal | `fig3` | crystal with vacancy/substitution/interstitial → "vacuum + localized obstacles" (`defect_lattice`) |
| fig4_same_topology_different_geometry | `fig4` | the four BZ tori in a row (2400×1000) |
| fig5_many_electrons | `fig5` | single electron (band) → many electrons (correlated); interaction lines from `wavy` |
| fig6_real_hopf_winding | `fig6` | handle-space figures, nontrivial vs. trivial winding (2400×1040) |
| fig7_quaternion_kahler | `fig7` | Chern band (Kähler) vs. Kramers pair (quaternion-Kähler); helpers `curl`, `metric_glyph`, `tesseract` |
| fig2/fig3_*_students | `figs_students.run` | same as fig2/fig3, but each `electron()` call is replaced by the mascot; the list `[(lens, radius), ...]` gives one entry per electron, in call order |
| header_scientist_electron_{transparent,white} | `figs_students.header` | 1600×1600 square crop of the mascot |

All are 2400×1350 px (12 × 6.75 in at 200 dpi) unless noted.

### Where to edit what

- **Text, headings, labels:** `heading(ov, x, y, title, subtitle)` calls at the top of each `figN()`. Coordinates are figure fractions (0–1).
- **Layout:** `place(fig, png, cx, cy, w)` places an asset image (centre and width as figure fractions). `panel_axes(fig, rect, xlim, ylim)` creates a drawing panel. `frame()` draws the rounded panel border and clips to it.
- **Palette / fonts / canvas size:** top of `figures/common.py`.
- **Torus shapes:** `shape_*` in `generators/bz_torus2.py`. Each one maps (kx, ky) to a point on a tube around a core curve (`tube()`). The `_tint` variants colour by local area distortion with the `dens` colormap.
- **Mascot appearance:** `character()` in `lib/scientist_electron.py` (body, glasses, lab coat, magnifying-glass lens content, spin arrow).
- **Defect positions:** `figs.defect_lattice` and `lib/electron_obstacles.py` (`strain()` displaces neighbouring atoms).

## Style guide (keep the series consistent)

- Palette:
  - ink `#24303b` (text, outlines)
  - navy `#2f4a63` (headings)
  - gray `#7d8a96` (subtitles)
  - light `#b9c8d6`
  - bond `#9aa8b5`
  - accent orange `#e07a3c` (paths, emphasis)
  - green `#3f7d62`
  - torus beige `#fbe3c4`
  - electron body blue `#3d9be0`
  - vacuum background `#f2f6fa`
  - motion streaks `#9fb6cb`
- Font: Inter for text. Math uses mathtext `dejavuserif`.
- Atoms are shaded spheres drawn as stacked circles (`sphere()`), never flat dots.
- 3-D surfaces:
  - Lambert shading plus a weak specular highlight
  - thin ink grid lines with hidden-line removal
  - bold silhouette
  - no matplotlib 3-D axes
- Panels are rounded frames with light border `#d9dfe5`; flow between panels uses `flow_arrow`.
- Two-panel figures use the "left concept → right interpretation" composition, with headings at y ≈ 0.82–0.92.
- No speech bubbles; the mascot stays understated.

## Caveats for editors

- `lib/electron_vacuum.py` and `lib/electron_obstacles.py` read `sys.argv[1]` at import time (they are also stand-alone scripts). `common.py` therefore blanks `sys.argv` while importing them. Keep that guard if you restructure the imports.
- `figs_students.py` works by temporarily monkey-patching `figs.electron` and `figs.save`. If you add or remove `electron()` calls in fig2/fig3, update the size lists in its `__main__` block to match.
- The 3-D renderers sample surfaces densely. If you change camera or size and see speckles or holes, raise the sampling density or the z-buffer bin factor (the `2.5 * ... / (W-1)` line). If hidden grid lines leak through, enlarge the `median_filter` size.
- The `.pdf` files that generators also write are not used by the figures and can be ignored.

## Website export (Physics Stories essay)

The essay uses six of these figures as WebP files in `public/students/`:
`fig1_topology_vs_geometry`, `fig2_perfect_crystal_students`, `fig3_imperfect_crystal_students`,
`fig4_same_topology_different_geometry`, `fig5_many_electrons`, `fig6_real_hopf_winding`.

- The essay shows these 2400 px images only ~590 px wide (~350 px on phones), so fig1–fig6 draw all
  text at `WEB_TEXT_SCALE` (1.5×, set in `figures/common.py`; every size goes through `fs()`).
  fig7 keeps the original scale.
- `out/` is not committed. Build into a scratch folder, then convert to WebP with the same names:

```bash
cd figures
FIG_OUT=/tmp/figs python3 figs.py 1 4 5 6
FIG_OUT=/tmp/figs python3 figs_students.py
python3 -c "from PIL import Image; import sys
for n in sys.argv[1:]: Image.open(f'/tmp/figs/{n}.png').convert('RGB').save(f'../../public/students/{n}.webp', quality=90, method=6)" \
  fig1_topology_vs_geometry fig2_perfect_crystal_students fig3_imperfect_crystal_students \
  fig4_same_topology_different_geometry fig5_many_electrons fig6_real_hopf_winding
```

Never edit the WebP/PNG files directly (an earlier hand edit left ghost text above the FIG. 05 title).
