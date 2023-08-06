# from apps.context import BASEDIR
from source.excel import Excel
import argparse, json
from functools import reduce
from termcolor import colored
from utils.utils import append_ext
from apps.config import (
    console,
    error_style,
    success_style,
    show_error,
    show_exception,
    show_warning,
)


def main():
    args = get_args()
    args = add_ext(args)
    protection = False if args.protection_off else True

    if args.add:
        if len(args.add) < 2:
            raise ValueError("Must more than two excel files after -a ")
        output_fn = args.to or args.add[0]
        try:
            excel_objs = list(map(lambda x: Excel(x), args.add))
            e = reduce(lambda a, b: a + b, excel_objs)
            e.makeExcel(output_fn, protection=protection)
            console.print(f"{output_fn} saved", "green", style=success_style)
            if args.json:
                print(e.json)
            if args.dict:
                print(e.dict)
        except Exception as e:
            console.print(f"{str(e)}", "red", style=error_style)

        return

    if args.sub:
        if len(args.sub) < 2:
            raise ValueError("Must more than two excel files after -a ")
        output_fn = args.to or args.sub[0]
        try:
            excel_objs = list(map(lambda x: Excel(x), args.sub))
            e = reduce(lambda a, b: a - b, excel_objs)
            e.makeExcel(output_fn, protection=protection)
            console.print("{output_fn} saved", style=success_style)
            if args.json:
                print(e.json)
            if args.dict:
                print(e.dict)

        except Exception as e:
            console.print("{str(e)}", style=error_style)
        return

    if args.copy:
        target_name = (
            args.to or args.copy[0]
        )  # if without -t filename, use first file as the target file name
        if len(args.copy) < 2:
            raise ValueError("Must  more than two excel files after -c ")
        try:
            excel_objs = list(map(lambda x: Excel(x), args.copy))
            e = reduce(lambda a, b: a.copy(b), excel_objs)
            e.makeExcel(target_name, protection=protection)
            console.print(f"{target_name} saved", style=success_style)
            if args.json:
                print(e.json)
            if args.dict:
                print(e.dict)

        except Exception as e:
            console.print(f"{str(e)}", style=error_style)

        return

    if args.excel and args.to and args.json:
        excel = Excel(args.excel)
        with open(args.to, "w") as fp:
            json.dump(excel.dict, fp, indent=3, default=str)
        console.print("{args.to} is saved", style=success_style)
        return

    if args.excel and args.json:
        excel = Excel(args.excel)
        print(excel.json)


def add_ext(args):
    if args.excel:
        args.excel = append_ext(args.excel, ".xlsx")
    if args.add:
        args.add = append_ext(args.add, ".xlsx")
    if args.sub:
        args.sub = append_ext(args.sub, ".xlsx")
    if args.copy:
        args.copy = append_ext(args.copy, ".xlsx")
    if args.to and args.json:
        args.to = append_ext(args.to, ".json")
    elif args.to:
        args.to = append_ext(args.to, ".xlsx")

    return args


def get_args():
    parser = argparse.ArgumentParser(
        description="For munipulate excel and get data source..."
    )

    parser.add_argument("-e", "--excel", help="Input excel name")
    parser.add_argument(
        "-a",
        "--add",
        help="add up excels(can be more than 2), and output to another excel",
        nargs="+",
    )
    parser.add_argument(
        "-s",
        "--sub",
        help="sub excels(can be more than 2), and output to another excel",
        nargs="+",
    )
    parser.add_argument(
        "-c",
        "--copy",
        help="copy later excels' common contents to first excel(can be more than 2), and output to another excel",
        nargs="+",
    )
    parser.add_argument(
        "-t",
        "--to",
        help="Output file name, if not input, the add, sub,or copy's first filename will be used as default",
    )
    parser.add_argument(
        "-po",
        "--protection_off",
        help="Protection off. default is On",
        action="store_true",
    )
    parser.add_argument("-j", "--json", help="need json output", action="store_true")
    parser.add_argument("-d", "--dict", help="need dict output", action="store_true")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
