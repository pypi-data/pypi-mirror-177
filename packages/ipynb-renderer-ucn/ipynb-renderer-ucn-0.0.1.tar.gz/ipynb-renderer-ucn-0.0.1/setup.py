from setuptools import setup, find_packages


setup(
    name="ipynb-renderer-ucn",
    version="0.0.1",
    author="muchsin",
    description="IPython Notebooks Renderer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmuchsin/ipynb_renderer",
    project_urls={"Bug Tracker": "https://github.com/mmuchsin/ipynb_renderer/issues"},
    package_dir={"": "src"},
    packages=find_packages("src"),
)
