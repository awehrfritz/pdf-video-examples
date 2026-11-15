"""Generate the synthetic media files for the examples.

clip.mp4:  160x90, 2 s, 10 fps H.264: a bar sweeping from left to right across
           a grey background, changing colour every frame (red, green, blue).
clip2.mp4: 160x90, 2 s, 10 fps H.264: a black dot moving from top to bottom on
           a yellow background; easy to tell apart from clip.mp4, e.g. to see
           which page is shown in presentation mode.
tone.wav:  1 s, 440 Hz sine, 8 kHz mono 8-bit (standard library only).

Run:  uv run --no-project --with av --with numpy python make-media.py
"""
import math
import wave

import av
import numpy as np

W, H, N, FPS = 160, 90, 20, 10


def write_clip(filename, frame):
    """Write N frames, frame(i) returning an RGB array, as H.264 MP4."""
    with av.open(filename, "w") as c:
        s = c.add_stream("libx264", rate=FPS)
        s.width, s.height, s.pix_fmt = W, H, "yuv420p"
        s.options = {"preset": "veryslow", "crf": "30"}
        for i in range(N):
            for p in s.encode(av.VideoFrame.from_ndarray(frame(i), format="rgb24")):
                c.mux(p)
        for p in s.encode():
            c.mux(p)


def bar(i):
    img = np.full((H, W, 3), 128, np.uint8)
    x = i * (W - 16) // (N - 1)
    img[:, x:x + 16] = [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i % 3]
    return img


def dot(i, r=12):
    img = np.full((H, W, 3), (255, 220, 0), np.uint8)
    cy = r + i * (H - 2 * r) // (N - 1)
    y, x = np.ogrid[:H, :W]
    img[(x - W // 2) ** 2 + (y - cy) ** 2 <= r * r] = 0
    return img


write_clip("clip.mp4", bar)
write_clip("clip2.mp4", dot)

RATE = 8000
with wave.open("tone.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(1)
    w.setframerate(RATE)
    w.writeframes(bytes(int(128 + 100 * math.sin(2 * math.pi * 440 * t / RATE))
                        for t in range(RATE)))
