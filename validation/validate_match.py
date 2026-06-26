#!/usr/bin/env python3
"""
validate_match.py  -  Pixel-match our render against the ground-truth reference.

One-time acceptance test: extracts the same frames from both videos, composites
each over an identical black background (so transparent areas are equal by
definition and we only measure VISIBLE differences), and reports per-frame diff
stats + point/alpha/timing checks.

USAGE:
  python3 validation/validate_match.py <ours.mov> <reference.mov>

EXIT: 0 = PASS, 1 = FAIL.
"""
import subprocess, sys, os, tempfile
from PIL import Image, ImageChops

FRAMES = [5, 30, 60, 90]          # timing + content sample points
WITHIN = 16                       # per-pixel channel diff considered "identical"
MIN_PCT_WITHIN = 95.0             # at least this % of pixels must be within WITHIN

def extract(path, frame):
    tmp = os.path.join(tempfile.gettempdir(), f"_vm_{os.path.basename(path)}_{frame}.png")
    cmd = ["ffmpeg","-y","-v","error","-i",path,
           "-vf", f"select=eq(n\\,{frame}),format=rgba","-vframes","1","-update","1",tmp]
    subprocess.run(cmd, capture_output=True, text=True)
    return Image.open(tmp).convert("RGBA") if os.path.exists(tmp) else None

def over_black(rgba):
    bg = Image.new("RGBA", rgba.size, (0,0,0,255))
    return Image.alpha_composite(bg, rgba).convert("RGB")

def pct_within(diff_rgb, thr):
    r,g,b = diff_rgb.split()
    mx = ImageChops.lighter(ImageChops.lighter(r,g), b)   # per-pixel max channel diff
    h = mx.histogram()
    total = sum(h)
    within = sum(h[:thr+1])
    return 100.0*within/total, max(i for i,c in enumerate(h) if c>0)

def opaque_pct(rgba):
    a = rgba.split()[3].histogram()
    return 100.0*a[255]/sum(a)

def main():
    if len(sys.argv) < 3:
        print("usage: validate_match.py <ours.mov> <reference.mov>"); return 2
    ours, ref = sys.argv[1], sys.argv[2]
    for p in (ours, ref):
        if not os.path.exists(p): print(f"FAIL: missing {p}"); return 1

    print(f"OURS : {ours}")
    print(f"REF  : {ref}\n")
    ok = True

    print(f"{'frame':>5} | {'%<=16 (match)':>14} | {'maxdiff':>7} | {'opaque% ours':>12} | {'opaque% ref':>11} | timing")
    print("-"*78)
    for f in FRAMES:
        a = extract(ours, f); b = extract(ref, f)
        if a is None or b is None: print(f"{f:>5} | FAIL extract"); ok=False; continue
        if a.size != b.size: print(f"{f:>5} | FAIL size {a.size} vs {b.size}"); ok=False; continue
        diff = ImageChops.difference(over_black(a), over_black(b))
        pw, mx = pct_within(diff, WITHIN)
        oa, ob = opaque_pct(a), opaque_pct(b)
        timing_ok = abs(oa-ob) < 1.0      # both files agree on how much strip is on-screen
        frame_ok = pw >= MIN_PCT_WITHIN
        if not (frame_ok and timing_ok): ok = False
        print(f"{f:>5} | {pw:>13.2f}% | {mx:>7} | {oa:>11.2f}% | {ob:>10.2f}% | {'OK' if timing_ok else 'MISMATCH'}")

    # Point + alpha checks at the hold frame (60)
    print("\nPoint checks @ frame 60:")
    a = extract(ours, 60); b = extract(ref, 60)
    tr_o = a.getpixel((1900,20))[3]; tr_r = b.getpixel((1900,20))[3]
    in_o = a.getpixel((100,1050));   in_r = b.getpixel((100,1050))
    print(f"  top-right (1900,20) alpha   ours={tr_o}  ref={tr_r}   (want 0 / 0)")
    print(f"  inside    (100,1050) RGBA   ours={in_o}  ref={in_r}   (want alpha 255, cream RGB)")
    corner_ok = (tr_o == 0 and tr_r == 0)
    rgb_close = all(abs(in_o[i]-in_r[i]) <= 12 for i in range(3))
    alpha_ok  = (in_o[3] == 255 and in_r[3] == 255)
    if not (corner_ok and rgb_close and alpha_ok): ok = False
    print(f"  corner transparent: {'OK' if corner_ok else 'FAIL'} | strip opaque: {'OK' if alpha_ok else 'FAIL'} | cream RGB match(<=12): {'OK' if rgb_close else 'FAIL'}")

    # Save a side-by-side record over gray
    def gray(rgba):
        bg = Image.new("RGBA", rgba.size, (85,96,112,255))
        return Image.alpha_composite(bg, rgba).convert("RGB")
    canvas = Image.new("RGB", (a.size[0], a.size[1]*2+20), (30,30,30))
    canvas.paste(gray(a), (0,0)); canvas.paste(gray(b), (0,a.size[1]+20))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "match_frame60_ours_vs_ref.png")
    canvas.save(out)
    print(f"\nSaved visual record: {out}")

    print("\n==================  " + ("[PASS] VIDEO MATCHES REFERENCE" if ok else "[FAIL] MISMATCH") + "  ==================")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
