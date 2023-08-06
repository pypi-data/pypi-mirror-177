# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrarity',
 'openrarity.cli',
 'openrarity.collection',
 'openrarity.io',
 'openrarity.metrics',
 'openrarity.providers',
 'openrarity.providers.opensea',
 'openrarity.token',
 'openrarity.token.metadata',
 'openrarity.token.metadata.dtypes',
 'openrarity.utils',
 'openrarity.validators']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['aiolimiter>=1.0.0,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'numpy>=1.23.4,<2.0.0',
 'pysatchel>=0.3.1,<0.4.0',
 'tabulate>=0.9.0,<0.10.0',
 'tenacity>=8.1.0,<9.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['openrarity = openrarity.cli.main:app']}

setup_kwargs = {
    'name': 'open-rarity',
    'version': '1.0.0a1',
    'description': 'Open-Rarity library is an open standard that provides an easy, explanable and reproducible computation for NFT rarity',
    'long_description': "![OpenRarity](img/OR_Github_banner.jpg)\n\n[![Version][version-badge]][version-link]\n[![Test CI][ci-badge]][ci-link]\n[![License][license-badge]][license-link]\n\n\n# OpenRarity\n\nWe’re excited to announce OpenRarity, a new rarity protocol we’re building for the NFT community. Our objective is to provide a transparent rarity calculation that is entirely open-source, objective, and reproducible.\n\nWith the explosion of new collections, marketplaces and tooling in the NFT ecosystem, we realized that rarity ranks often differed across platforms which could lead to confusion for buyers, sellers and creators. We believe it’s important to find a way to provide a unified and consistent set of rarity rankings across all platforms to help build more trust and transparency in the industry.\n\nWe are releasing the OpenRarity library in a Beta preview to crowdsource feedback from the community and incorporate it into the library evolution.\n\nSee the full announcement in the [blog post](https://mirror.xyz/openrarity.eth/LUoJnybWuNYedIQHD6RRdX1SS9MiowdI6a69X-lefGM).\n\n## CLI Usage\n\n\nIf you already have a json file containing the metadata for the tokens you want to rank you can run the following which will print ranks to stdout.\n\n```\n❯ openrarity rank data/boredapeyachtclub/tokens.json | head -n 10\n  token_id    unique_traits       ic    rank\n----------  ---------------  -------  ------\n      7495                0  42.0592       1\n      4873                0  40.4554       2\n      8854                0  40.2091       3\n       446                0  40.017        4\n        73                0  39.6501       5\n      8135                0  39.5842       6\n      8976                0  39.5072       7\n      4980                0  39.4849       8\n```\n\nLikewise you can write to a json file\n```\n❯ openrarity rank data/boredapeyachtclub/tokens.json -o boredapeyachtclub_ranks.json\n```\n\n\nIf you don't have metadata available you can fetch it from OpenSea first\n```\n❯ openrarity opensea fetch-assets --slug boredapeyachtclub --start-token-id 0 --end-token-id 9999 --rank | head -n 10\n100%|████████████████████████████████████████| 334/334 [01:40<00:00,  3.33it/s]\n  token_id    unique_traits       ic    rank\n----------  ---------------  -------  ------\n      7495                0  42.0592       1\n      4873                0  40.4554       2\n      8854                0  40.2091       3\n       446                0  40.017        4\n        73                0  39.6501       5\n      8135                0  39.5842       6\n      8976                0  39.5072       7\n      4980                0  39.4849       8\n```\n\n# Developer documentation\n\nRead [developer documentation](https://openrarity.gitbook.io/developers/) on how to integrate with OpenRarity.\n\n# Setup and run tests locally\n\n```\npoetry install # install dependencies locally\npoetry run pytest # run tests\n```\n\n# Library usage\nRead [developer documentation](https://openrarity.gitbook.io/developers/) for advanced library usage\n\n\n# Contributions guide and governance\n\nOpenRarity is a community effort to improve rarity computation for NFTs (Non-Fungible Tokens). The core collaboration group consists of four primary contributors: [Curio](https://curio.tools), [icy.tools](https://icy.tools), [OpenSea](https://opensea.io) and [Proof](https://www.proof.xyz/)\n\nOpenRarity is an open-source project and all contributions are welcome. Consider following steps when you request/propose contribution:\n\n- Have a question? Submit it on OpenRarity GitHub  [discussions](https://github.com/ProjectOpenSea/open-rarity/discussions) page\n- Create GitHub issue/bug with description of the problem [link](https://github.com/ProjectOpenSea/open-rarity/issues/new?assignees=impreso&labels=bug&template=bug_report.md&title=)\n- Submit Pull Request with proposed changes\n- To merge the change in the `main` branch you required to get at least 2 approvals from the project maintainer list\n- Always add a unit test with your changes\n\nWe use git-precommit hooks in OpenRarity repo. Install it with the following command\n```\npoetry run pre-commit install\n```\n\n# Project Setup and Core technologies\n\nWe used the following core technologies in OpenRarity:\n\n- Python ≥ 3.10.x\n- Poetry for dependency management\n- PyTest for unit tests\n\n# License\n\nApache 2.0 , OpenSea, ICY, Curio, PROOF\n\n\n\n[license-badge]: https://img.shields.io/github/license/ProjectOpenSea/open-rarity\n[license-link]: https://github.com/ProjectOpenSea/open-rarity/blob/main/LICENSE\n[ci-badge]: https://github.com/ProjectOpenSea/open-rarity/actions/workflows/tests.yaml/badge.svg\n[ci-link]: https://github.com/ProjectOpenSea/open-rarity/actions/workflows/tests.yaml\n[version-badge]: https://img.shields.io/github/v/release/ProjectOpenSea/open-rarity\n[version-link]: https://github.com/ProjectOpenSea/open-rarity/releases?display_name=tag\n",
    'author': 'Dan Meshkov',
    'author_email': 'daniil.meshkov@opensea.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
