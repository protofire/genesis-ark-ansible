from setuptools import setup, find_packages

setup(
    name="runner",
    version="0.0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "ansible-runner",
        "jsonschema",
        "toml",
        "PyYAML",
        "requests",
        "pymongo[srv]",
        "Flask-PyMongo",
        "click",
        "eth-keys",
        "web3",
        "loguru"
    ],
    entry_points="""
        [console_scripts]
        runner=runner.cli:safe_entrypoint
    """,
)
