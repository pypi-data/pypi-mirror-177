# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_boost',
 'py_boost.callbacks',
 'py_boost.cv',
 'py_boost.gpu',
 'py_boost.gpu.losses',
 'py_boost.multioutput',
 'py_boost.quantization',
 'py_boost.sampling',
 'py_boost.utils']

package_data = \
{'': ['*']}

install_requires = \
['joblib',
 'numba',
 'numpy',
 'pandas>=1',
 'scikit-learn>=1',
 'tqdm>=4.64.1',
 'treelite>=3',
 'treelite_runtime>=3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'py-boost',
    'version': '0.3.0',
    'description': 'Python based GBDT',
    'long_description': '# Py-boost: a research tool for exploring GBDTs\n\nModern gradient boosting toolkits are very complex and are written in low-level programming languages. As a result,\n\n* It is hard to customize them to suit one’s needs \n* New ideas and methods are not easy to implement\n* It is difficult to understand how they work\n\nPy-boost is a Python-based gradient boosting library which aims at overcoming the aforementioned problems. \n\n**Authors**: [Anton Vakhrushev](https://kaggle.com/btbpanda), [Leonid Iosipoi](http://iosipoi.com/).\n\n\n## Py-boost Key Features\n\n**Simple**. Py-boost is a simplified gradient boosting library but it supports all main features and hyperparameters available in other implementations.\n\n**Fast with GPU**. Despite the fact that Py-boost is written in Python, it works only on GPU and uses Python GPU libraries such as CuPy and Numba.\n\n**Easy to customize**. Py-boost can be easily customized even if one is not familiar with GPU programming (just replace np with cp).  What can be customized? Almost everuthing via custom callbacks. Examples: Row/Col sampling strategy, Training control, Losses/metrics, Multioutput handling strategy, Anything via custom callbacks\n\n\n## SketchBoost [paper](https://openreview.net/forum?id=WSxarC8t-T)\n\n**Multioutput training**. Current state-of-atr boosting toolkits provide very limited support of multioutput training. And even if this option is available, training time for such tasks as multlcass/multilabel classification and multitask regression is quite slow because of the training complexity that scales linarly with the number of outputs. To overcomde the existing limitations we create **SketchBoost** algorithm that uses approximate tree structure search. As we show in [paper](https://openreview.net/forum?id=WSxarC8t-T) that stragegy at least does not lead to performance decrease and often is able to improve the accuracy\n\n**SketchBoost**. You can try our sketching strategies by using `SketchBoost` class or if you want you can implement your own and pass to the `GradientBoosting` constructor as `multioutput_sketch` parameter. For the details please see [Tutorial_2_Advanced_multioutput](https://github.com/AILab-MLTools/Py-Boost/blob/master/tutorials/Tutorial_2_Advanced_multioutput.ipynb)\n\n\n## Installation\n\nBefore installing py-boost via pip you should have cupy installed. You can use:\n\n`pip install -U cupy-cuda110 py-boost`\n\n**Note**: replace with your cuda version! For the details see [this guide](https://docs.cupy.dev/en/stable/install.html)\n\n\n## Quick tour\n\nPy-boost is easy to use since it has similar to scikit-learn interface. For usage example please see:\n\n* [Tutorial_1_Basics](https://github.com/AILab-MLTools/Py-Boost/blob/master/tutorials/Tutorial_1_Basics.ipynb) for simple usage examples\n* [Tutorial_2_Advanced_multioutput](https://github.com/AILab-MLTools/Py-Boost/blob/master/tutorials/Tutorial_2_Advanced_multioutput.ipynb) for advanced multioutput features\n* [Tutorial_3_Custom_features](https://github.com/AILab-MLTools/Py-Boost/blob/master/tutorials/Tutorial_3_Custom_features.ipynb) for examples of customization\n\nMore examples are comming soon\n',
    'author': 'Vakhrushev Anton',
    'author_email': 'btbpanda@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AILab-MLTools/Py-Boost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
