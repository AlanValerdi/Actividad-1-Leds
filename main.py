import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk, ImageFilter, ImageOps

def make_glow(base_img, glow_color=(0, 255, 0), core_boost=1.9, glow_opacity=190, blur_radius=26, pad=32):
    """Build a glow behind the LED using its alpha mask."""
    img = base_img.convert("RGBA")
    core = ImageEnhance.Brightness(img).enhance(core_boost)

    alpha = img.split()[-1]
    glow_color_img = Image.new("RGBA", img.size, glow_color + (0,))
    glow_color_img.putalpha(alpha)

    glow_padded = ImageOps.expand(glow_color_img, border=pad, fill=(0, 0, 0, 0))
    halo = glow_padded.filter(ImageFilter.GaussianBlur(blur_radius))

    r, g, b, a = halo.split()
    a = a.point(lambda v: int(v * (glow_opacity / 255.0)))
    halo = Image.merge("RGBA", (r, g, b, a))

    out = Image.new("RGBA", halo.size, (0, 0, 0, 0))
    out.alpha_composite(halo, (0, 0))
    out.alpha_composite(core, (pad, pad))
    return out

def main():
    window = tk.Tk()
    window.title("LEDs con Glow (Vertical)")

    # --- Function to prepare LED image states ---
    def load_led(path, size=(100, 100), glow_color=(0, 255, 0)):
        base = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        pad = 32
        off_canvas = Image.new("RGBA", (base.width + 2*pad, base.height + 2*pad), (0, 0, 0, 0))
        off_canvas.alpha_composite(base, (pad, pad))
        img_off = ImageTk.PhotoImage(off_canvas)
        img_on = ImageTk.PhotoImage(make_glow(base, glow_color=glow_color, pad=pad))
        return img_off, img_on

    # --- Load both LEDs ---
    led1_off, led1_on = load_led("Foco.png", glow_color=(0, 255, 0))   # green glow
    led2_off, led2_on = load_led("Led.png",  glow_color=(0, 255, 0))   # red glow

    # --- Create labels (vertical stack) ---
    led1_label = tk.Label(window, image=led1_off, bd=0)
    led1_label.image_off, led1_label.image_on = led1_off, led1_on
    led1_label.pack(side="top", padx=20, pady=(20, 10))

    led2_label = tk.Label(window, image=led2_off, bd=0)
    led2_label.image_off, led2_label.image_on = led2_off, led2_on
    led2_label.pack(side="top", padx=20, pady=(10, 20))

    # Track shared state for both LEDs
    leds_on = {"value": False}

    # --- Single toggle for both ---
    def toggle_both():
        leds_on["value"] = not leds_on["value"]
        state_img1 = led1_label.image_on if leds_on["value"] else led1_label.image_off
        state_img2 = led2_label.image_on if leds_on["value"] else led2_label.image_off
        led1_label.config(image=state_img1)
        led2_label.config(image=state_img2)
        btn.config(text="Apagar ambos" if leds_on["value"] else "Encender ambos")

    # --- One button to rule them all ---
    btn = tk.Button(window, text="Encender ambos", command=toggle_both)
    btn.pack(side="top", pady=(0, 20))

    window.mainloop()

if __name__ == "__main__":
    main()
