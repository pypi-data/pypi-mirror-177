from setuptools import setup, find_packages
readme = open('README.txt', encoding="utf8")

setup(
    name='quicksqlconnector',
    version='1.4.3',
    license='MIT',
    license_files='LICENSE',
    author="Anas Raza",
    author_email='anasraza1@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://quicksqlconnector.web.app/',
    keywords='quicksqlconnector, sql, database, mysql',
    install_requires=[
          'mysql-connector-python',
          'prettytable'
      ],
    description='Run SQL queries with just one line in python. Use MySQL like a layman.',
    long_description=readme.read(),
    long_description_content_type='text/markdown'
)