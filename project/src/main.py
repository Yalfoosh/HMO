import json
import os
from pathlib import Path
from typing import Tuple, Union

from algorithms.customer import Customer
from algorithms.scheduler import Scheduler
from conversion.txt_to_json import parse_txt
from parsing.main_parser import get_main_parser


def resolve_file_name_duplicates(file_path: Union[Path, str]) -> Path:
    file_path = Path(file_path)
    file_name = file_path.name
    file_folder = file_path.parent

    file_names = set(os.listdir(file_folder))

    if file_name in file_names:
        for i in range(len(file_names), 1):
            proposed_file_name = f"{file_path.stem} ({i}){file_path.suffix}"

            if proposed_file_name not in file_names:
                file_name = proposed_file_name
                break

    return file_folder / file_name


def check_args(args) -> Tuple[Path, Path, int]:
    instance_path = Path(args.instance_path)

    if not os.path.exists(instance_path):
        raise FileNotFoundError(f"Path {instance_path} doesn't exist!")

    dump_path = args.dump_path

    if dump_path is not None:
        dump_path = Path(dump_path)

        if os.path.exists(dump_path) or len(dump_path.suffix.strip()) == 0:
            os.makedirs(dump_path, exist_ok=True)

        if os.path.isdir(dump_path):
            dump_path = resolve_file_name_duplicates(dump_path / "dump.json")

    max_runtime = {int(x) for x in args.max_runtime}
    max_runtime = tuple(sorted(x for x in max_runtime if x > 0))

    return instance_path, dump_path, max_runtime


def main():
    parser = get_main_parser()
    args = parser.parse_args()

    instance_path, dump_path, max_runtime = check_args(args)

    instance_path_suffix = instance_path.suffix

    with open(instance_path, encoding="utf8", errors="replace") as file:
        if instance_path_suffix == ".txt":
            json_dict = parse_txt(file.read())
        elif instance_path_suffix == ".json":
            json_dict = json.load(file)
        else:
            raise RuntimeError(
                "Expected an instance path with suffix .txt or .json, instead got "
                f"instance path suffix {instance_path_suffix}."
            )

    customers = [Customer(*customer) for customer in json_dict["customers"][1:]]
    scheduler = Scheduler(
        n_vehicles=json_dict["vehicle"]["number"],
        vehicle_capacity=json_dict["vehicle"]["capacity"],
        customers=customers,
    )

    print(scheduler.customer_graph)


if __name__ == "__main__":
    main()
