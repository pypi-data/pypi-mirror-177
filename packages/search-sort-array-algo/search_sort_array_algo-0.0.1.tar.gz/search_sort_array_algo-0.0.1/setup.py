from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This package includes algorithms such as LinearSearch,BinarySearch, Two pointer , Sliding window. It will get updated every week!!!'

# Setting up
setup(
    name="search_sort_array_algo",
    version=VERSION,
    author="Rumour(Sarthak Samantaray)",
    author_email="<sarthak.samantaraycoding@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'Algorithms', 'Arrays', 'Strings', 'Linked List', 'Stacks'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)