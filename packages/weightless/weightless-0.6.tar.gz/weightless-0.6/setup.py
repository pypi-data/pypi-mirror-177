from setuptools import setup, find_packages


setup(
    name='weightless',
    version='0.6',
    license='MIT',
    author="Alan T. L. Bacellar",
    author_email='alanbacellar@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/alantlb/weightless',
    keywords='example project',
    install_requires=[
          'numpy',
      ],

)