from pathlib import Path # a partir de Python 3.6
from setuptools import setup

"""
Para poder exponer nuestra app para instalarla desde PyPi
"""

this_directory = Path(__file__).parent
long_description = (this_directory/'README.md').read_text()

VERSION = '0.0.2'
DESCRIPTION = 'Consume API de codigofacilito.com'
PACKAGE_NAME = 'pack_cfacilito'
AUTHOR = 'Francisco Alejandro Benitez'
EMAIL = 'fabenitez.dev@hotmail.com'
GITHUB_URL = 'https://github.com/fabenitez-dev/codigofacilito_package'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    entry_points={ #cuando alguien instale el paquete podrá ejecutarlo con el nombre cfacilito
        "console_scripts":
            ["cfacilito=pack_cfacilito.__main__:main"]
    },
    version = VERSION,
    license='MIT', #tipo de licencia necesita el archivo LICENSE.txt
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [
        'codigofacilito' # palabras claves para encontrarlo
    ],
    install_requires=[ 
        'requests', #bibiotecas utilizadas
    ],
    classifiers=[ #clasificadores para PyPi
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)