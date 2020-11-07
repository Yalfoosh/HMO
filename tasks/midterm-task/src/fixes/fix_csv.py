import os
from pathlib import Path

from parsing import fix_csv_parser
import utils


def main():
    parser = fix_csv_parser.get_parser()
    args = parser.parse_args()

    extension = "tsv" if args.tsv else "csv" if args.csv else None
    delimiter = "\t" if args.tsv else "," if args.csv else None
    quotechar = '"'

    for csv_path in args.csv_paths:
        csv_path = Path(csv_path)

        destination_folder = (
            csv_path.parent
            if args.destination_folder is None
            else args.destination_folder
        )
        destination_folder = Path(destination_folder)

        os.makedirs(destination_folder, exist_ok=True)

        new_name = f"{utils.get_filename_without_extension(csv_path)}.{extension}"
        destination_path = destination_folder / new_name

        rows = utils.load_csv(csv_path=csv_path)
        utils.save_rows(
            rows=rows,
            destination_path=destination_path,
            delimiter=delimiter,
            quotechar=quotechar,
        )


if __name__ == "__main__":
    main()
