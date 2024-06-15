import argparse
import io
import os
import sys

from funny_json_explorer import FunnyJsonExplorer


def main():
    args = parse_args()
    explorer = FunnyJsonExplorer(args.f, args.s, args.i)
    explorer.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, default='test/fixture/fruit.json', help='json file.')
    parser.add_argument('--s', type=str, choices=['tree', 'rectangle'], default='tree', help='style')
    parser.add_argument('--i', type=str, default='none', help='icon family')
    return parser.parse_args()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    sys.path.append(parent_dir)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
