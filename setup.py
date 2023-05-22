from setuptools import setup, find_packages


with open("README.md") as file:
    long_desc = file.read()

setup(
    name="pyhdl1",
    desc="尝试制作python的verilog生成器",
    long_desc=long_desc,
    version="0.0.1",
    packages=find_packages(exclude=["tests"])
)
