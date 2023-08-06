from distutils.core import setup

setup(
    name="domino_mlflow_client",
    packages=["domino_mlflow_client"],
    version="0.6.9",
    license="MIT",
    description="Domino client wrapper for ml flow",
    author="Sameer Wadkar , Uday Kumar Samala, Pattabi Srinivasan",
    author_email="sammer.wadkar@dominodatalab.com",
    url="https://github.com/cerebrotech/domino-mlflow-utils",
    download_url="https://github.com/cerebrotech/domino-mlflow-utils/archive/pypi-0_1_5.tar.gz",
    keywords=["domino", "mlflow", "client"],
    install_requires=["pyjwt==2.6.0", "kubernetes==17.17.0", "dominodatalab"],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
