#!/usr/bin/env bash
set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
# Official v86 repository: https://github.com/copy/v86
# Engine builds are published as GitHub release assets.
# BIOS files ship in the repo's bios/ directory.
# Buildroot Linux images are hosted at https://i.copy.sh/
V86_RELEASE="https://github.com/copy/v86/releases/download/latest"
V86_RAW="https://raw.githubusercontent.com/copy/v86/master"
V86_IMAGES="https://i.copy.sh"
PUBLIC_DIR="$(cd "$(dirname "$0")/.." && pwd)/public"

# ─── Helpers ─────────────────────────────────────────────────────────────────
info()  { printf '\033[1;34m[INFO]\033[0m  %s\n' "$*"; }
ok()    { printf '\033[1;32m[OK]\033[0m    %s\n' "$*"; }
fail()  { printf '\033[1;31m[FAIL]\033[0m  %s\n' "$*" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "'$1' is required but not installed."
}

download() {
  local url="$1" dest="$2"
  if [[ -f "$dest" ]]; then
    info "Already exists, skipping: $(basename "$dest")"
    return 0
  fi
  info "Downloading $(basename "$dest") from $url ..."
  if curl -fSL --progress-bar -o "$dest" "$url"; then
    ok "$(basename "$dest")"
    return 0
  else
    rm -f "$dest"
    return 1
  fi
}

# ─── Preflight ───────────────────────────────────────────────────────────────
require_cmd curl

mkdir -p "$PUBLIC_DIR"
info "Assets will be saved to: $PUBLIC_DIR"

# ─── 1. BIOS files (from v86 repo raw content) ──────────────────────────────
info "Fetching BIOS files …"
download "$V86_RAW/bios/seabios.bin"  "$PUBLIC_DIR/seabios.bin"  || fail "Could not download seabios.bin"
download "$V86_RAW/bios/vgabios.bin"  "$PUBLIC_DIR/vgabios.bin"  || fail "Could not download vgabios.bin"

# ─── 2. v86 engine (from GitHub release assets) ─────────────────────────────
info "Fetching v86 engine files …"
download "$V86_RELEASE/libv86.js"  "$PUBLIC_DIR/libv86.js"  || fail "Could not download libv86.js"
download "$V86_RELEASE/v86.wasm"   "$PUBLIC_DIR/v86.wasm"   || fail "Could not download v86.wasm"

# ─── 3. Linux kernel + root filesystem (from i.copy.sh) ─────────────────────
# buildroot-bzimage68.bin is a minimal Buildroot Linux with serial console.
# It does NOT require a separate rootfs — the initramfs is embedded in the kernel.
info "Fetching Linux images …"
download "$V86_IMAGES/buildroot-bzimage68.bin"  "$PUBLIC_DIR/buildroot-bzimage68.bin" \
  || fail "Could not download buildroot-bzimage68.bin"

# ─── 5. Verify all files ────────────────────────────────────────────────────
info ""
info "=== Asset verification ==="
all_ok=true
for f in libv86.js v86.wasm seabios.bin vgabios.bin buildroot-bzimage68.bin; do
  if [[ -f "$PUBLIC_DIR/$f" ]]; then
    size=$(du -h "$PUBLIC_DIR/$f" | cut -f1)
    ok "$f  ($size)"
  else
    fail "$f  MISSING"
    all_ok=false
  fi
done

echo ""
if $all_ok; then
  ok "All assets are in place at: $PUBLIC_DIR"
  info "You can now run:  pnpm slidev slides-terminal.md"
else
  fail "Some assets are missing — see errors above."
fi
