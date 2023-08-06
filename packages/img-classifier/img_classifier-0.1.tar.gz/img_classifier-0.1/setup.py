# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['img_classifier',
 'img_classifier.dataloader',
 'img_classifier.loss',
 'img_classifier.model',
 'img_classifier.optimizer',
 'img_classifier.scheduler',
 'img_classifier.trainer']

package_data = \
{'': ['*'],
 'img_classifier': ['data/Chess/Bishop/*',
                    'data/Chess/King/*',
                    'data/Chess/Knight/*',
                    'data/Chess/Pawn/*',
                    'data/Chess/Queen/*',
                    'data/Chess/Rook/*',
                    'data/test_images/*']}

install_requires = \
['pandas>=1.5.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.12.1,<2.0.0',
 'torchinfo>=1.7.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.23.1,<5.0.0',
 'wandb>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'img-classifier',
    'version': '0.1',
    'description': '',
    'long_description': None,
    'author': 'jy-choi',
    'author_email': 'jy.choi@toss.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
