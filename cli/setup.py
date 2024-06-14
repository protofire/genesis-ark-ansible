from setuptools import setup, find_packages

setup(
    name="runner",
    version="0.0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "jsonschema",
        "loguru",
    ],
    entry_points="""
        [console_scripts]
        runner=runner.cli:safe_entrypoint
    """,
)
