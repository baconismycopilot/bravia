import json
from typing import Any

from bravia import Bravia


def pretty_dump(data: Any):
    print(json.dumps(data, indent=2, default=str))


def main():
    b: Bravia = Bravia(ip="192.168.50.190")
    pretty_dump(b.api_info())


if __name__ == "__main__":
    main()
