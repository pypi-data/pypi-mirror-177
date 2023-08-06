import pathlib
from setuptools import setup, find_packages
from os.path import join, dirname

try:
    long_description = pathlib.Path(join(dirname(__file__), "readme.md")).read_text()

except:
    long_description = (
        "A library for easy use of unsupervised learning algorithms. "
        "It contains both classic solutions and little-known ones."
    )

setup(
    name="ul_lib",
    packages=["ul_lib"],
    version="0.0.1a1",
    license="MIT",
    description="A library for easy use of unsupervised learning algorithms.",
    author="Dmatryus Detry",
    author_email="dmatryus.sqrt49@yandex.ru",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dmatryus.sqrt49/ul_lib",
    keywords=["UL", "unsupervised learning", "ML", "machine learning", "optimization"],
    install_requires=["numpy", "umap-learn", "scikit-learn", "matplotlib", "tqdm"],
)
