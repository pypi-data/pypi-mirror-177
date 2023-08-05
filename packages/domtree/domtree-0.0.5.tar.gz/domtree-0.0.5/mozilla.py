from typing import List, NamedTuple

import requests
from bs4 import BeautifulSoup


def svg_url(element_name: str) -> str:
    return f"https://developer.mozilla.org/en-US/docs/Web/SVG/Element/{element_name}"


def all_svg_elements() -> List[str]:
    page = requests.get("https://developer.mozilla.org/en-US/docs/Web/SVG/Element")
    soup = BeautifulSoup(page.content, "html.parser")

    links = set()
    for link in soup.select("a"):
        href = link.attrs.get("href", None)
        if (
            href is not None
            and href.startswith("/en-US/docs/Web/SVG/Element/")
            and not href.endswith(".txt")
        ):
            links.add(href.replace("/en-US/docs/Web/SVG/Element/", ""))
    return list(sorted(list(links)))


class SvgPage(NamedTuple):
    examples: List[str]
    attributes: List[str]
    url: str


def look_up_svg_page(element_name: str) -> SvgPage:
    url = svg_url(element_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    examples = [e.text for e in soup.select(".code-example")[1:]]
    attributes = [
        x.text
        for x in soup.select("dt a")
        if "Attribute" in x.attrs["href"] and not " " in x.text
    ]
    return SvgPage(examples=examples, attributes=attributes, url=url)
