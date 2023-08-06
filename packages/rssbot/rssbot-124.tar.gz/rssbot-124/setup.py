# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="rssbot",
    version="124",
    url="https://github.com/bthate/rssbot",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="feeding rss into your irc channel",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["rssbot"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
                ("share/rssbot", ["files/rssbot.service",]),
                ("share/doc/rssbot", ["README.rst",])
               ],
    scripts=["bin/rssbot",  "bin/rsscmd", "bin/rssctl"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
