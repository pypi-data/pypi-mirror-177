from setuptools import setup, find_packages


setup(
    name='anita',
    version='0.1.4',
    license='MIT',
    author="Davi Romero de Vasconcelos",
    author_email='daviromero@ufc.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/daviromero/anita',
    description='''ANITA is a proof assistant for teaching analytic tableaux to computer science students. 
    ANITA allows students to write their proofs and automatically checks whether the proofs are correct and, if not, displays any errors found.''',
    keywords='Analytic Tableaux, Teaching Logic, Educational Software', 
    install_requires=[
          'rply',
      ],

)
