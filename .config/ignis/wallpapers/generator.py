#!/usr/bin/env python3
import math
import json
import sys
from PIL import Image
from materialyoucolor.quantize import QuantizeCelebi
from materialyoucolor.score.score import Score
from materialyoucolor.hct import Hct
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.utils.color_utils import rgba_from_argb, argb_from_rgb
from materialyoucolor.utils.math_utils import sanitize_degrees_double, difference_degrees, rotation_direction
# from materialyoucolor.scheme.scheme_vibrant import SchemeTonalSpot as Scheme

# from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot as Scheme


scheme = sys.argv[3]

if scheme == 'fruitsalad':
    from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad as Scheme
elif scheme == 'expressive':
    from materialyoucolor.scheme.scheme_expressive import SchemeExpressive as Scheme
elif scheme == 'monochrome':
    from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome as Scheme
elif scheme == 'rainbow':
    from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow as Scheme
elif scheme == 'tonalspot':
    from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot as Scheme
elif scheme == 'neutral':
    from materialyoucolor.scheme.scheme_neutral import SchemeNeutral as Scheme
elif scheme == 'fidelity':
    from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity as Scheme
elif scheme == 'content':
    from materialyoucolor.scheme.scheme_content import SchemeContent as Scheme
elif scheme == 'vibrant':
    from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant as Scheme
else:
    from schemes.scheme_morevibrant import SchemeMoreVibrant as Scheme




# Constants
# IMAGE_PATH = "/home/jawadhc/Pictures/Wallpapers/Birds/toucan-another.jpg"
IMAGE_PATH = sys.argv[1]
BITMAP_SIZE = int(sys.argv[2])
DARK_MODE = True
TRANSPARENT = False

# Helper functions
rgba_to_hex = lambda rgba: "#{:02X}{:02X}{:02X}".format(rgba[0], rgba[1], rgba[2])
argb_to_hex = lambda argb: "#{:02X}{:02X}{:02X}".format(*map(round, rgba_from_argb(argb)))

def calculate_optimal_size(width, height, bitmap_size):
    scale = min(1, math.sqrt((bitmap_size ** 2) / (width * height)))
    return max(1, round(width * scale)), max(1, round(height * scale))

# Process image
image = Image.open(IMAGE_PATH)
if image.format == "GIF":
    image.seek(1)

wsize, hsize = image.size
wsize_new, hsize_new = calculate_optimal_size(wsize, hsize, BITMAP_SIZE)
if wsize_new < wsize or hsize_new < hsize:
    image = image.resize((wsize_new, hsize_new), Image.Resampling.BICUBIC)

colors = QuantizeCelebi(list(image.getdata()), 128)
argb = Score.score(colors)[0]
hct = Hct.from_int(argb)

# Generate color scheme
scheme = Scheme(hct, DARK_MODE, 0.0)
material_colors = {color: rgba_to_hex(getattr(MaterialDynamicColors, color).get_hct(scheme).to_rgba())
                   for color in vars(MaterialDynamicColors).keys() if hasattr(getattr(MaterialDynamicColors, color), "get_hct")}

# Print colors
# print(f"$darkmode: {DARK_MODE};")
# print(f"$transparent: {TRANSPARENT};")
for color, code in material_colors.items():
    print(f"${color}: {code};")
print(f"$main: $primary")
# print()
