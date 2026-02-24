import sys
from PIL import Image, ImageSequence

def rgb_to_braille(pixels, width, height):
    # Braille dots mapping:
    # 1 4
    # 2 5
    # 3 6
    # 7 8
    output = []
    for y in range(0, height, 4):
        line = ""
        for x in range(0, width, 2):
            byte = 0
            # Check 2x4 block
            dots = [
                (0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08),
                (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80)
            ]
            for dx, dy, bit in dots:
                if x + dx < width and y + dy < height:
                    # Threshold for dot (brightness)
                    p = pixels[x + dx, y + dy]
                    if isinstance(p, tuple):
                        brightness = sum(p[:3]) / 3
                    else:
                        brightness = p
                    if brightness > 128:
                        byte |= bit
            line += chr(0x2800 + byte)
        output.append(line)
    return "\n".join(output)

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_frames.py <input> <output>")
        return

    img = Image.open(sys.argv[1])
    frames = []
    
    # Target width for terminal
    target_width = 80 
    
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("L") # Grayscale
        # Resize to fit terminal width (2 dots per char width, 4 per char height)
        w, h = frame.size
        # scale = target_width * 2 / w
        # new_w = int(w * scale)
        # new_h = int(h * scale)
        # Actually just resize to target_width * 2
        new_w = target_width * 2
        new_h = int((h * new_w) / w / 2) # Adjust for terminal aspect ratio (approx)
        frame = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        pixels = frame.load()
        braille = rgb_to_braille(pixels, new_w, new_h)
        frames.append(braille)
    
    with open(sys.argv[2], "w") as f:
        f.write("---FRAME---\n".join(frames))

if __name__ == "__main__":
    main()
