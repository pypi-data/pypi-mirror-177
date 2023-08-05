"""
Setup
"""

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = []
for line in open('requirements.txt', encoding='utf-8'):
    li = line.strip()
    if not li.startswith('#'):
        requirements.append(line.rstrip())

VERSION = (0, 0, 15)  # (1, 0, 7, 'dev0')
__version__ = '.'.join(map(str, VERSION))

setup(
    # Nome (não precisa ser o nome do repositório, nem de qualquer pasta...)
    name='ufesp',
    version=__version__,
    author='Michel Metran',
    author_email='michelmetran@gmail.com',
    description='Série Temporal da Unidade Fiscal do Estado de São Paulo e métodos para recuperar informações da UFESP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gaemapiracicaba/sp_sefaz_ufesp',
    keywords='python, ufesp, finance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese',
        'Intended Audience :: Developers',
    ],
    # Qual python? e packages?
    python_requires='>=3',
    install_requires=requirements,
    # Entry
    # Our packages live under src but src is not a package itself
    # package_dir={'': 'ufesp'},
    # Quando são diversos módulos...
    # packages=find_packages('ufesp', exclude=['test']),
    packages=['ufesp'],
    # Apenas um módulo...
    # py_modules=['decreto_estadual_8468'],  # Quando se trata apenas de um módulo
    # Dados
    include_package_data=True,
    package_data={'': ['data/ufesp.csv']},
)
