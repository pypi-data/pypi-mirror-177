from domtree import Node
from domtree.svg import *


def main():
    c = circle(x=10, y=10).add(x=10).mul(y=2)
    print(c)


if __name__ == "__main__":
    main()
