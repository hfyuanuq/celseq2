import os
import io

from setuptools import setup, find_packages, Command
from os import path

root = 'celseq2'
name = 'celseq2'

exec(open("celseq2/version.py").read())

here = path.abspath(path.dirname(__file__))
description = ('A Python Package for Processing '
               'CEL-Seq2 RNA-Seq Data.')

install_requires = [
    'snakemake==4.0.0',
    'pyyaml>=3.12, <4',
    'HTSeq>=0.9',
    'pytest==3.2.2',
    'pandas>=0.20.0',
    'numpy>=1.12.0',
    'tables>=3.4.2',
]

# do not require installation if built by ReadTheDocs
# (we mock these modules in docs/source/conf.py)
if 'READTHEDOCS' not in os.environ or \
        os.environ['READTHEDOCS'] != 'True':
    install_requires.extend([
        #'six>=1.10.0, <2',
        #'scipy>=0.14, <1',
        #'plotly>=1.9.6, <3',
    ])
else:
    install_requires.extend([
        #'pandas>=0.13, <1',
    ])

# get long description from file
long_description = ''
with io.open(path.join(here, 'README.md'), encoding='UTF-8') as fh:
    long_description = fh.read()


class CleanCommand(Command):
    """Removes files generated by setuptools.

    """
    # see https://github.com/trigger/trigger/blob/develop/setup.py
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        error_msg = 'You must run this command in the package root!'
        if not os.getcwd() == here:
            raise OSError(error_msg)
        else:
            os.system('rm -rf ./dist ./build ./*.egg-info ')


setup(
    name=name,

    version=__version__,

    description=description,
    long_description=long_description,

    # homepage
    url='https://gitlab.com/Puriney/celseq2',

    author='Yun Yan',
    author_email='yy1533@nyu.edu',

    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='CEL-Seq2 single-cell RNA-seq expression pipeline processing',

    # packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=find_packages(exclude=['docs', 'tests*']),
    # packages=find_packages(root),

    # libraries = [],

    setup_requires=['pytest-runner'],
    install_requires=install_requires,

    tests_require=['pytest'],

    extras_require={
        'docs': [
            # 'sphinx',
            # 'sphinx-rtd-theme',
            # 'sphinx-argparse',
            # 'mock',
            'mkdocs',
            'fontawesome_markdown',
            'mkdocs-bootswatch',
            'pymdown-extensions',
        ],
        'tests': [
            'pytest>=3, <4',
            'pytest-cov>=2.2.1, <3',
        ],
    },

    # data
    package_data={
        'celseq2': [
            'template/*',  # config.yaml, etc
            'workflow/*',  # snakemake workflow
            'demo/*',  # demo data for running dummy analysis
        ]
    },
    # data outside the package
    # data_files=[('my_data', ['data/data_file'])],

    entry_points={
        'console_scripts': [

            ('bc_demultiplex = '
             'celseq2.demultiplex:main'),
            ('cook-annotation = '
             'celseq2.prepare_annotation_model:main'),
            ('count-umi = '
             'celseq2.count_umi:main'),
            ('new-configuration-file = '
             'celseq2.cook_config:main_new_config_file'),
            ('export-workflow = '
             'celseq2.cook_config:main_export_snakemake_workflow'),
            ('new-experiment-table = '
             'celseq2.cook_config:main_new_experiment_table'),
            ('celseq2 = '
             'celseq2.celseq2:main'),
            ('celseq2-slim = '
             'celseq2.slim:main'),
            ('celseq2-dummy-species = '
             'celseq2.dummy_species:main'),
            ('celseq2-simulate = '
             'celseq2.dummy_CELSeq2_reads:main'),
            ('celseq2-test = '
             'celseq2.dummy_celseq2_test:main'),
            ('celseq2-diagnose = '
             'celseq2.diagnose:main'),
            ('celseq2-to-st = '
             'celseq2.support.st_pipeline:main'),
        ],
    },

    cmdclass={
        'clean': CleanCommand,
    },

)
