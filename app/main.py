import asyncio
import argparse
from datetime import datetime

from pipeline import generate_tale
from file_utils import save_to_file
from setup import SHARED_PATH, setup_logging


def get_args():
    parser = argparse.ArgumentParser(
        description="Process city, genre, and length inputs."
    )

    parser.add_argument("city", type=str, help="City name")
    parser.add_argument(
        "genre",
        type=str,
        choices=["Drama", "Comedy", "Musical", "Detective", "Action", "Horror"],
        help="Genre of the movie",
    )
    parser.add_argument("length", type=int, help="Length of the text in characters")

    args = parser.parse_args()

    return args


async def main():
    args = get_args()
    yandex_tale, giga_tale = await asyncio.gather(
        generate_tale("yandex", args.city, args.genre, args.length),
        generate_tale("giga", args.city, args.genre, args.length),
    )
    postfix = f"{args.city}_{args.genre}_{args.length}_{datetime.now()}"
    yandex_tale_path = SHARED_PATH / f"tales/yandex_tale_{postfix}.txt"
    giga_tale_path = SHARED_PATH / f"tales/giga_tale_{postfix}.txt"
    save_to_file(yandex_tale_path, yandex_tale)
    print(f"Yandex tale have been saved: {yandex_tale_path}")
    save_to_file(giga_tale_path, giga_tale)
    print(f"Giga tale have been saved: {giga_tale_path}")


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
