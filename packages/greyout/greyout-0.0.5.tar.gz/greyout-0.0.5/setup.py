from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='greyout',
      version='0.0.5',
      description='Getting to grey.',
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      license='MIT',
      packages=['greyout'],
      install_requires=[
          'markdown',
      ],
      entry_points={
          'console_scripts': ['black=greyout.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
