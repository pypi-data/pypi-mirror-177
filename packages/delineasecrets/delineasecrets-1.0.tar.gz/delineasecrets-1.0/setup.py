from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'Secrets Generator'
LONG_DESCRIPTION = 'Pacote para consumo de secrets do Delinea Vault'

# Setting up
setup(
       
        name="delineasecrets", 
        version=VERSION,
        author="Humberto Machado, Bruna Paiva",  
        author_email="humberto.machado@ssys.com.br, bruna.paiva@ssys.com.br",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        keywords=['python', 'secrets'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)