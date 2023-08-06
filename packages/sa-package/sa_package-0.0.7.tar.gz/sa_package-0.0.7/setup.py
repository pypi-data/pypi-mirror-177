from setuptools import setup, find_packages

# print(["lib"] + [f"lib.{item}" for item in find_packages(where="lib")])

setup(
    name="sa_package",
    version="0.0.7",
    
    url="https://github.com/tmddk2709/sa_package",
    author="Seunga Shin",
    author_email="seungashin9275@gmail.com",

    package_dir={"": "sa_package"},
    packages=find_packages("sa_package"),

    install_requires=[
        "bs4",
        "pandas",
        "gspread",
        "oauth2client",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "selenium",
        "webdriver-manager",
        "packaging"
    ]
)