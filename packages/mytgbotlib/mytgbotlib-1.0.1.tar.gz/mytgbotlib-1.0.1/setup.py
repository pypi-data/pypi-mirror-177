from setuptools import find_packages, setup

setup(
    name="mytgbotlib",
    packages=find_packages(include=["mytgbotlib", "mytgbotlib.*"]),
    version="1.0.1",
    description="A simple Telegram bot library",
    author="Aleksander Radovsky",
    license="MIT",
    install_requires=["requests"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "requests-mock"],
    test_suite="tests",
)
