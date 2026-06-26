#!/usr/bin/env python3
"""
verify_alpha.py  -  Prove an exported video actually has a working alpha channel.

WHY THIS EXISTS:
  A render can exit 0, have correct metadata, and STILL have its transparency
  silently flattened to opaque. The only trustworthy check is reading real
  pixel alpha values. This script does that.

USAGE:
  python3 tools/verify_alpha.py renders/my-clip.mov
  python3 tools/verify_alpha.py renders/my-clip.webm 60      # check frame 60

EXIT CODE: 0 = PASS, 1 = FAIL (so it can gate a pipeline).
"""
import subprocess, sys, tempfile, os, json
from PIL import Image

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe_frames(path):
    r = run(["ffprobe","-v","error","-select_streams","v:0",
             "-show_entries","stream=nb_frames,r_frame_rate","-show_entries","format=duration",
             "-of","json", path])
    try:
        d = json.loads(r.stdout); s = d["stream"][0] if "stream" in d else d["streams"][0]
    except Exception:
        return None
    return s

def extract_rgba(path, frame):
    """Extract one frame as an RGBA PNG, forcing the VP9 decoder for .webm
    so the alpha side-channel is not silently dropped."""
    tmp = os.path.join(tempfile.gettempdir(), f"_verify_f{frame}.png")
    pre = ["-c:v","libvpx-vp9"] if path.lower().endswith(".webm") else []
    cmd = ["ffmpeg","-y","-v","error"] + pre + ["-i", path,
           "-vf", f"select=eq(n\\,{frame}),format=rgba", "-vframes","1","-update","1", tmp]
    run(cmd)
    return tmp if os.path.exists(tmp) else None

def main():
    if len(sys.argv) < 2:
        print("usage: python3 tools/verify_alpha.py <video> [frame]"); return 2
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"FAIL: file not found: {path}"); return 1

    # default to the middle frame (most likely to be mid-animation)
    frame = int(sys.argv[2]) if len(sys.argv) > 2 else None
    info = probe_frames(path)
    if frame is None:
        try:
            n = int((info or {}).get("nb_frames") or 0)
        except Exception:
            n = 0
        frame = max(0, n // 2) if n else 30

    png = extract_rgba(path, frame)
    if not png:
        print(f"FAIL: could not extract frame {frame} from {path}"); return 1

    im = Image.open(png).convert("RGBA")
    w, h = im.size
    a = im.split()[3]
    hist = a.histogram()
    total = w * h
    transparent = hist[0]                # alpha == 0
    opaque      = hist[255]              # alpha == 255
    partial     = total - transparent - opaque
    pct_t = 100*transparent/total
    pct_o = 100*opaque/total
    pct_p = 100*partial/total

    corners = {f"({x},{y})": im.getpixel((x,y))[3]
               for (x,y) in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]}

    print(f"File   : {path}")
    print(f"Frame  : {frame}  ({w}x{h})")
    print(f"Alpha  : transparent(0)={pct_t:6.2f}%   opaque(255)={pct_o:6.2f}%   partial={pct_p:6.2f}%")
    print(f"Corners: " + "  ".join(f"{k}={v}" for k,v in corners.items()))

    # PASS = the frame contains BOTH transparent and opaque regions (real alpha,
    # not flattened to fully-opaque and not an empty/blank frame).
    if pct_t < 0.5:
        print("RESULT : [FAIL] almost no transparent pixels. Alpha looks FLATTENED to opaque.")
        return 1
    if pct_o + pct_p < 0.2:
        print("RESULT : [FAIL] frame is essentially empty (nothing drawn). Check timing / data-duration.")
        return 1
    print("RESULT : [PASS] real alpha (mix of transparent + drawn pixels).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
