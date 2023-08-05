# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omegacli']

package_data = \
{'': ['*']}

install_requires = \
['omegaconf>=2.0.6,<3.0.0']

setup_kwargs = {
    'name': 'omegaconf-argparse',
    'version': '0.1.0',
    'description': 'Integration between Omegaconf and argparse for mixed config file and CLI arguments',
    'long_description': '# omegaconf-argparse\nIntegration between Omegaconf and argparse for mixed config file and CLI arguments\n\nFlexible configuration management is important during experimentation, e.g. when training machine learning models.\n\nIdeally, we want both a configuration file to hold more "stable" hyperparameter values and the flexibility to\nchange values through command line arguments for rapid experimentation.\n\n## How it works\n\nThis package provides a barebones solution based on the excellent [OmegaConf](https://github.com/omry/omegaconf) package.\n\nSpecifically, we extend the `OmegaConf` class with a static `from_argparse` method to parse arguments provided using argparse,\nand provide utility functions to merge the default CLI values, YAML configuration file values and user provided CLI arguments.\n\n\n## Usage\n\nWe provide a high-level utility function `parse_config` that merges a YAML configuration file with an `argparse.ArgumentParser`:\n\n```\nimport io\nfrom omegacli import parse_config\nmock_config_file = io.StringIO(\'\'\'\nmodel:\n  hidden: 100\n\'\'\')\nparser = argparse.ArgumentParser("My cool model")\nparser.add_argument("--hidden", dest="model.hidden", type=int, default=20)\ncfg = parse_config(parser, mock_config_file)\n>>> {\'model\': {\'hidden\': 100}}\ntype(cfg)\n>>> <class \'omegaconf.dictconfig.DictConfig\'>\ncfg = parse_config(parser, mock_config_file, args=["--hidden", "200"])\n>>> {\'model\': {\'hidden\': 200}}\nmock_config_file = io.StringIO(\'\'\'\nrandom_value: hello\n\'\'\')\ncfg = parse_config(parser, mock_config_file)\n>>> {\'model\': {\'hidden\': 20}, \'random_value\': \'hello\'}\n```\n\nYou can also use the patched `OmegaConf` class directly:\n\n```\nimport argparse\nfrom omegacli import OmegaConf\nparser = argparse.ArgumentParser("My cool model")\nparser.add_argument("--hidden", dest="model.hidden", type=int, default=20)\nuser_provided_args, default_args = OmegaConf.from_argparse(parser, args=["--hidden", "100"])\nuser_provided_args\n>>> {\'model\': {\'hidden\': 100}}\ndefault_args\n>>> {}\nuser_provided_args, default_args = OmegaConf.from_argparse(parser)\nuser_provided_args\n>>> {}\ndefault_args\n>>> {\'model\': {\'hidden\': 20}}\n```\n\n**NOTE**: the `from_argparse` method calls the `parser.parse_args()`.\n\n## Merging of provided values\n\nThe precedence for merging is as follows\n* default cli args values < config file values < user provided cli args\n\nE.g.:\n* if you don\'t include a value in your configuration it will take the default value from the argparse arguments\n* if you provide a cli arg (e.g. run the script with --bsz 64) it will override the value in the config file\n\n\n## Generate a configuration file based on an argument parser\n\nRun:\n\n```\nfrom omegacli import generate_config_template\ngenerate_config_template(parser, "example-config.yaml")\n```\n\nThis will initialize a configuration file, that is consistent with the argument parser.\nYou can use this as a starting point for saving and editing your configuration.\n\n## Similar solutions\n\n* [Hydra](https://hydra.cc/docs/intro/): A more feature-rich, but more complex solution. If you are willing to introduce the dependency you can use it\n* [Pytorch-Lightning](https://pytorch-lightning.readthedocs.io/en/1.6.2/common/lightning_cli.html): PL introduced a similar functionality. You can use it if you are in the PL ecosystem.\n\n## Why create a separate package?\n\n`OmegaConf` plans to remain agnostic to the command line argument parser, therefore we cannot merge this solution upstream. [See related issue](https://github.com/omry/omegaconf/issues/569).\n',
    'author': 'Giorgos Paraskevopoulos',
    'author_email': 'georgepar.91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
