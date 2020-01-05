from setuptools import setup, find_packages

# Traverses through the project and builds the modules setup based on 
# where the __init__.py files are located
setup(name='graphqlGenerator', version='1.0', packages=find_packages())