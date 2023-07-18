import logging

name = "gitmate"
__version__ = "0.1.0"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="gitmate.log",
)


