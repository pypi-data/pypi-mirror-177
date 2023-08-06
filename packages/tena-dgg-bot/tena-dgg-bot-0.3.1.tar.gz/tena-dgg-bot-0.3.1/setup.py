from setuptools import setup, find_packages


setup(
    name="tena-dgg-bot",
    version="0.3.1",
    author="tena",
    description="A library for making a bot in Destiny.gg chat. Fork of https://github.com/Fritz-02/dgg-bot",
    long_description_content_type="text/markdown",
    url="https://github.com/tenacious210/tena-dgg-bot/",
    project_urls={
        "Bug Tracker": "https://github.com/tenacious210/tena-dgg-bot/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Chat",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
)
