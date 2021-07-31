import skbuild

skbuild.setup(
    name="pyDOOM",
    version="0.1",
    author="mephi42",
    author_email="mephi42@gmail.com",
    description="Python-controlled vanilla DOOM",
    url="https://github.com/mephi42/pyDOOM",
    packages=["_pyDOOM"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
