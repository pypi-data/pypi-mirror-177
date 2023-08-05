import os

from sentinelc_appfeed.builder import build_feed

BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_optional_homepage_documentation():
    build_feed(f"{BASEPATH}/optional_homepage_documentation")
