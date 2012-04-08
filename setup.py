from setuptools import setup, find_packages

version = '0.0.6'

setup(
    name = 'isotoma.recipe.postdeploy',
    version = version,
    description = "Buildout recipes for postdeploy.",
    url = "http://pypi.python.org/pypi/isotoma.recipe.postdeploy",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    classifiers = [
        "Framework :: Buildout",
        "Framework :: Buildout :: Recipe",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "proxy buildout postdeploy",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
    },
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.buildout',
        'Jinja2',
        'missingbits',
    ],
    entry_points = {
        "zc.buildout": [
            "default = isotoma.recipe.postdeploy.recipe:PostDeploy",
        ],
    }
)
