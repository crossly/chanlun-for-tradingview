from argparse import ArgumentParser
from pathlib import Path

from PIL import Image


SEGMENT_BLUE = (33, 150, 243)


def count_near_color(image: Image.Image, target: tuple[int, int, int], tolerance: int) -> int:
    return sum(
        max(abs(red - target[0]), abs(green - target[1]), abs(blue - target[2]))
        <= tolerance
        for red, green, blue in image.convert("RGB").getdata()
    )


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("screenshot", type=Path)
    parser.add_argument("--minimum-blue-pixels", type=int, default=20)
    args = parser.parse_args()

    image = Image.open(args.screenshot).convert("RGB")
    width, height = image.size
    plot = image.crop(
        (
            int(width * 0.08),
            int(height * 0.09),
            int(width * 0.92),
            int(height * 0.93),
        )
    )
    blue_pixels = count_near_color(plot, SEGMENT_BLUE, tolerance=35)
    print(f"segment_blue_pixels={blue_pixels}")
    if blue_pixels < args.minimum_blue_pixels:
        raise SystemExit(
            f"expected at least {args.minimum_blue_pixels} visible segment-blue pixels"
        )


if __name__ == "__main__":
    main()
