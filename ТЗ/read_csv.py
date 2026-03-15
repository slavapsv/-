import csv
import argparse
from tabulate import tabulate
from statistics import median


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Обработка списка файлов")

    parser.add_argument(
        "--files", "-f",
        nargs="+",
        type=argparse.FileType("r", encoding="utf-8"),
        help="CSV файлы"
    )

    parser.add_argument(
        "--report",
        help="Тип отчета"
    )

    return parser.parse_args(args)


def calculate_median(files):
    answer = {}

    for file in files:
        reader = csv.DictReader(file)
        for row in reader:
            answer.setdefault(row["student"], []).append(float(row["coffee_spent"]))

    result = []
    for student, values in sorted(answer.items(), key=lambda x: median(x[1]), reverse=True):
        result.append([student, median(values)])

    return result


def main(cli_args=None):
    args = parse_args(cli_args)

    if not args.files:
        print("Ошибка: файлы не выбраны")
        return

    if args.report != "median-coffee":
        print("Ошибка: неправильно указан отчёт. Используйте: median-coffee")
        return

    table = calculate_median(args.files)
    print(tabulate(table, headers=["student", "median_coffee"], tablefmt="grid"))


if __name__ == "__main__":
    main()