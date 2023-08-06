# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['ambrosia',
 'ambrosia.designer',
 'ambrosia.preprocessing',
 'ambrosia.spark_tools',
 'ambrosia.splitter',
 'ambrosia.tester',
 'ambrosia.tools',
 'ambrosia.tools._lib']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'catboost>=1.0.4,<2.0.0',
 'hyperopt>=0.2.7,<0.3.0',
 'jinja2>=3.0.0,<4.0.0',
 'joblib>=1.1.0,<2.0.0',
 'nmslib>=2.0.4,<3.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=0.25.3,<2.0.0',
 'pyspark>=3.2,<4.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0',
 'tqdm>=4.27.0,<5.0.0']

setup_kwargs = {
    'name': 'ambrosia',
    'version': '0.2.0',
    'description': 'A Python library for working with A/B tests.',
    'long_description': ".. shields start\n\nAmbrosia\n========\n\n|PyPI| |PyPI License| |ReadTheDocs| |Tests| |Coverage| |Black| |Python Versions|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/ambrosia\n    :target: https://pypi.org/project/ambrosia\n.. |PyPI License| image:: https://img.shields.io/pypi/l/ambrosia.svg\n    :target: https://github.com/MobileTeleSystems/Ambrosia/blob/main/LICENSE\n.. |ReadTheDocs| image:: https://img.shields.io/readthedocs/ambrosia.svg\n    :target: https://ambrosia.readthedocs.io\n.. |Tests| image:: https://img.shields.io/github/workflow/status/MobileTeleSystems/RecTools/Test/main?label=tests\n    :target: https://github.com/MobileTeleSystems/Ambrosia/actions/workflows/test.yaml?query=branch%3Amain+\n.. |Coverage| image:: https://codecov.io/gh/MobileTeleSystems/Ambrosia/branch/main/graph/badge.svg\n    :target: https://codecov.io/gh/MobileTeleSystems/Ambrosia\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/ambrosia.svg\n    :target: https://pypi.org/project/ambrosia  \n\n.. shields end\n\n.. image:: https://raw.githubusercontent.com/MobileTeleSystems/Ambrosia/main/docs/source/_static/ambrosia.png\n\n.. title\n\n**Ambrosia** is a Python library for A/B tests design, split and effect \nmeasurement. It provides rich set of methods for conducting full \nA/B test pipeline. \n\nAn experiment design stage is performed using metrics historical data \nwhich could be processed in both forms of pandas and spark dataframes \nwith either theoretical or empirical approach. \n\nGroup split methods support different strategies and multi-group split, \nwhich allows to quickly create control and test groups of interest. \n\nFinal effect measurement stage is conducted via testing tools that \nare able to return relative and absolute effects and construct corresponding \nconfidence intervalsfor continious and binary variables. \nTesting tools as well as design ones support significant number of \nstatistical criteria, like t-test, non-parametric, and bootstrap. \n\nFor additional A/B tests support library provides features and tools \nfor data preproccesing and experiment acceleration.\n\n.. functional\n\nKey functionality\n-----------------\n\n* Pilots design ✈\n* Multi-group split 🎳\n* Matching of new control group to the existing pilot 🎏\n* Getting the experiments result evaluation as p-value, point estimate of effect and confidence interval 🎞\n* Experiments acceleration 🎢\n\n.. documentation\n\nDocumentation\n-------------\n\nFor more details, see the `Documentation <https://ambrosia.readthedocs.io/>`_ \nand `Tutorials <https://github.com/MobileTeleSystems/Ambrosia/tree/main/examples>`_.\n\n.. install\n\nInstallation\n------------\n\nStable version is released on every tag to ``main`` branch. \n\n.. code:: bash\n    \n    pip install ambrosia \n\n**Ambrosia requires Python 3.7+**\n\n.. usage\n\nUsage\n-----\n\nDesigner \n~~~~~~~~\n\n.. code:: python\n\n    from ambrosia.designer import Designer\n    designer = Designer(dataframe=df, effects=1.2, metrics='portfel_clc') # 20% effect, and loaded data frame df\n    designer.run('size') \n\n\nSplitter\n~~~~~~~~\n\n.. code:: python\n\n    from ambrosia.splitter import Splitter\n    splitter = Splitter(dataframe=df, id_column='id') # loaded data frame df with column with id - 'id'\n    splitter.run(groups_size=500, method='simple') \n\n\nTester \n~~~~~~\n\n.. code:: python\n\n    from ambrosia.tester import Tester\n    tester = Tester(dataframe=df, column_groups='group') # loaded data frame df with groups info 'group'\n    tester.run(metrics='retention', method='theory', criterion='ttest')\n\n.. develop\n\nDevelopment\n-----------\n\nTo install all requirements run\n\n.. code:: bash\n\n    make install\n\nYou must have ``python3`` and ``poetry`` installed.\n\nFor autoformatting run\n\n.. code:: bash\n\n    make autoformat\n\nFor linters check run\n\n.. code:: bash\n\n    make lint\n\nFor tests run\n\n.. code:: bash\n\n    make test\n\nFor coverage run\n\n.. code:: bash\n\n    make coverage\n\nTo remove virtual environment run\n\n.. code:: bash\n\n    make clean\n\n.. contributors\n\nCommunication\n-------------\n\n**Developers and evangelists**:\n\n* `Bayramkulov Aslan <https://github.com/aslanbm>`_\n* `Khakimov Artem <https://github.com/xandaau>`_\n* `Vasin Artem <https://github.com/VictorFromChoback>`_\n",
    'author': 'Aslan Bayramkulov',
    'author_email': 'aslan.bayramkulov96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MobileTeleSystems/Ambrosia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.10.4',
}


setup(**setup_kwargs)
