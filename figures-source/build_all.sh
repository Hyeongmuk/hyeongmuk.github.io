#!/usr/bin/env bash
# Rebuild everything.  Usage:
#   ./build_all.sh            # figures only, using the pre-rendered PNGs in assets/
#   ./build_all.sh --assets   # also re-render the intermediate PNGs in assets/ first (slow, ~1-2 min)
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--assets" ]]; then
  tmp=$(mktemp -d)
  python3 generators/bz_torus2.py   "$tmp" round hotspot aniso twisted
  python3 generators/handle_torus.py "$tmp"
  (cd lib && python3 scientist_electron.py "$tmp")
  cp "$tmp"/bz_torus_{round,hotspot,aniso,twisted}_tint.png \
     "$tmp"/handle_torus_{nontrivial,trivial}.png \
     "$tmp"/scientist_electron_transparent.png assets/
  rm -rf "$tmp"
fi
cd figures
python3 figs.py            # fig1 ... fig7   (python3 figs.py 3 5  -> only fig3, fig5)
python3 figs_students.py   # fig2/fig3 student variants + header mascot
echo "done -> out/"
