from setuptools import setup, find_packages

setup(name='redhat_tar_xz_extractor',
      version='1.0.0',
      description='tarfile.xz file extractor use case for redhat feature',
      author='Aryanshu verma',
      author_email='aryanshu.verma@dell.com',
      packages=find_packages(exclude=['tests', 'venv']),
      install_requires=["tarfile"]
      )