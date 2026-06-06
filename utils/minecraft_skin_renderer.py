# AI GENERATED

from PIL import Image

PARTS = {
    "head":              (8,  8,  8, 8),
    "head_overlay":      (40, 8,  8, 8),
    "body":              (20, 20, 8, 12),
    "body_overlay":      (20, 36, 8, 12),
    "arm_right":         (43, 20, 4, 12),
    "arm_right_overlay": (43, 36, 4, 12),
    "arm_left":          (36, 52, 4, 12),
    "arm_left_overlay":  (52, 52, 4, 12),
    "leg_right":         (4,  20, 4, 12),
    "leg_right_overlay": (4,  36, 4, 12),
    "leg_left":          (20, 52, 4, 12),
    "leg_left_overlay":  (4,  52, 4, 12),
}

DEST = {
    "head":      (4,  0),
    "body":      (4,  8),
    "arm_right": (0,  8),
    "arm_left":  (12, 8),
    "leg_right": (4,  20),
    "leg_left":  (8,  20),
}

CANVAS_W = 16
CANVAS_H = 32


def skin_to_2d(skin: Image.Image, scale: int = 20) -> Image.Image:
    """
    Convertit un skin Minecraft brut en vue 2D frontale.

    Args:
        skin  : Image PIL du skin (64x32 ou 64x64).
        scale : Facteur de zoom en pixels par unite (defaut 20 -> 320x640 px).

    Returns:
        Image PIL RGBA du personnage vu de face.
    """
    skin = skin.convert("RGBA")
    modern = skin.height == 64

    def crop(key):
        x, y, w, h = PARTS[key]
        return skin.crop((x, y, x + w, y + h))

    def overlay(base, ov):
        result = base.copy()
        ov = ov.convert("RGBA")
        result.paste(ov, (0, 0), mask=ov)
        return result

    head      = overlay(crop("head"),      crop("head_overlay"))
    body      = overlay(crop("body"),      crop("body_overlay"))
    arm_right = overlay(crop("arm_right"), crop("arm_right_overlay"))
    leg_right = overlay(crop("leg_right"), crop("leg_right_overlay") if modern else crop("leg_right"))

    if modern:
        arm_left = overlay(crop("arm_left"), crop("arm_left_overlay"))
        leg_left = overlay(crop("leg_left"), crop("leg_left_overlay"))
    else:
        arm_left = crop("arm_right").transpose(Image.FLIP_LEFT_RIGHT)
        leg_left = crop("leg_right").transpose(Image.FLIP_LEFT_RIGHT)

    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    for part, img in [("head", head), ("body", body), ("arm_right", arm_right),
                      ("arm_left", arm_left), ("leg_right", leg_right), ("leg_left", leg_left)]:
        dx, dy = DEST[part]
        canvas.paste(img, (dx, dy), mask=img)

    return canvas.resize((CANVAS_W * scale, CANVAS_H * scale), resample=Image.NEAREST)