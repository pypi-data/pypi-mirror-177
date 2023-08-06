from setuptools import setup

setup(
    name="Luci-first-package",
    version="0.2.0",
    author= "Lucian",
    author_email="stardust0010@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first package,get pwnd noobs."
)