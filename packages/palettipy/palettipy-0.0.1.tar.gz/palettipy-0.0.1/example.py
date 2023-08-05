import os
import sys
import time

from PIL import Image

from palettipy import palettes_loader, palettipy_image
from palettipy.palette import Palette


def main(args: list[str], palettes_path: str = "palettes"):
    if len(args) <= 0 or len(args) >= 3:
        print("Usage: example.py path/to/image [palette name]")
        sys.exit(1)

    print(args)

    image_path = args[0]
    if not os.path.exists(image_path):
        print(f'Image "{image_path}" does not exist')
        sys.exit(1)

    palettes = palettes_loader.load_palettes(palettes_path)

    palette_name = palettes[0].name
    if len(args) > 1:
        palette_name = args[1]
        if palette_name not in [_p.name for _p in palettes]:
            print(f'Palette "{palette_name}" does not exist')
            sys.exit(1)

    start = time.time()

    palette: Palette = list(filter(lambda p: (p.name == palette_name), palettes))[0]
    image = Image.open(image_path)

    image_result = Image.fromarray(palettipy_image(palette, image))
    image_result.save("output.png")

    palette.log(f"Done in {(time.time() - start):.3f}s")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
