from domtree.node import Node


def test_basic_usage_does_not_crash():
    div = Node("div")
    div(id="parent")(div(id="child1"), div(id="child2"))
