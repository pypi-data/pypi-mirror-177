from setuptools import find_packages, setup

setup(
    name="mytelegrambotlib",
    packages=find_packages(include=['mytelegrambotlib']),
    version='0.1.0',
    description="Library with telegram bot",
    author="Leonid Dubrovin",
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.*'],
    test_suite='tests',
)
