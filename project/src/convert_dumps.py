import json
import os
from pathlib import Path

from parsing.convert_dumps_parser import get_convert_dumps_parser


def main():
    parser = get_convert_dumps_parser()
    args = parser.parse_args()

    src = args.dump_path
    dest_folder = args.destination_path

    if os.path.exists(src):
        with open(src, encoding="utf8", errors="replace") as file:
            json_dict = json.load(file)

        keys = sorted([int(x) for x in json_dict.keys()])
        keys = [str(x) for x in keys]
        times = [f"{x}m" for x in keys[:-1]]
        times.append("un")
        instance_number = int(Path(src).stem[-1])

        os.makedirs(dest_folder, exist_ok=True)

        for key, time in zip(keys, times):
            file_path = os.path.join(dest_folder, f"res-{time}-i{instance_number}.txt")
            result = json_dict[key]

            if result is None:
                continue

            with open(file_path, mode="w+", encoding="utf8", errors="replace") as file:
                file.write(result["result"])


if __name__ == "__main__":
    main()
