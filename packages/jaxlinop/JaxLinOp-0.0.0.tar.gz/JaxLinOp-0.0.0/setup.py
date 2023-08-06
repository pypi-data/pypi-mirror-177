from setuptools import find_packages, setup

setup(
    name="JaxLinOp",
    version="0.0.0",
    author="Daniel Dodd",
    author_email="d.dodd1@lancaster.ac.uk",
    packages=find_packages(".", exclude=["tests"]),
    license="LICENSE",
    description="A JAX linear operator library.",
    keywords=["jax linear-operator low-rank linear-algebra"],
)
