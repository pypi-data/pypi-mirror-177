from setuptools import setup

setup(
    name="Aida-first-package",
    version="0.1.0",
    author="Aida",
    author_email="radu.aida@yahoo.com",
    packages=["my_own_package"],
    package_dir={"":"src\\"},
    include_package_data=True,
    description="This is my first package."
)