from setuptools import setup, find_packages


setup(
    name='miyanepp',
    version='0.6',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/miyanyan/miyanepp',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
