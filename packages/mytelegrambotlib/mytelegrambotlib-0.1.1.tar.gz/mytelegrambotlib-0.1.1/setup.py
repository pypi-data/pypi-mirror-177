from setuptools import find_packages, setup
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mytelegrambotlib",
    packages=find_packages(include=['mytelegrambotlib']),
    version='0.1.1',
    description="Library with telegram bot for homework",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Leonid Dubrovin",
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.*'],
    test_suite='tests',
)
