from setuptools import setup

setup(
    name="huddu",

    version="1.0.2",

    packages=["huddu", "huddu.utils"],

    url="https://github.com/hudduapp/huddu-python",

    requires=["json", "requests"],

    license="MIT",

    author="Joshua3212",

    author_email="hello@huddu.io",

    description="Python SDK for Huddu",
)
