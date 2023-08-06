import setuptools

with open("README.md", 'r') as f:
  long_description = f.read()

setuptools.setup(
  include_package_data = True,
  name = "algo-beast-protocols",
  version = "0.1.1",
  description = "AlgoBeast Protocols",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/krunaldodiya/algo-beast-protocols",
  author = "Krunal Dodiya",
  author_email = "kunal.dodiya1@gmail.com",
  packages = setuptools.find_packages(),
  install_requires = [
    "requests",
  ],
  classifiers =[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent"
  ]
)
