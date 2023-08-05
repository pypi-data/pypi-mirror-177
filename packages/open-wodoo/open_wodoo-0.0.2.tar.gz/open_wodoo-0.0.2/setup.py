# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_wodoo',
 'open_wodoo.commands',
 'open_wodoo.commands.rpc',
 'open_wodoo.git',
 'open_wodoo.helpers']

package_data = \
{'': ['*']}

install_requires = \
['gitpython==3.1.27',
 'openupgradelib==3.3.4',
 'python-dotenv==0.20.0',
 'rich==12.6.0',
 'ruamel-yaml==0.17.21',
 'typer[all]>=0.7.0,<0.8.0',
 'wodoo-rpc==0.0.2']

entry_points = \
{'console_scripts': ['wodoo = open_wodoo.cli:launch_cli']}

setup_kwargs = {
    'name': 'open-wodoo',
    'version': '0.0.2',
    'description': 'Wrapper around Odoo-Bin with some convinience RPC functions.',
    'long_description': '# Wodoo Dev Environment\n\n![OdooLogo](assets/odoo_logo.png)\n\n[Vscode Devcontainer](https://code.visualstudio.com/docs/remote/containers) Environment for [Odoo](.odoo.com/)\n\nMade Possible by: [WEMPE Elektronic GmbH](https://wetech.de)\n\n## Devcontainer Features\n\n- Devcontainer workspace [full.code-workspace](full.code-workspace) with Odoo source, Workspace and Thirdparty Source.\n- `wodoo` CLI wrapper around Odoo.\n- `odoo-bin` is added to PATH and can thus be invoked from every folder.\n- Odoo will run in Proxy_Mode behind a Traefik reverse proxy.\n- [Odoo Pylint plugin](https://github.com/OCA/pylint-odoo) preconfigured in vscode\n- Preinstalled vscode Extensions Highlights:\n  - [SQL Tools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) with preconfigured connection for\n    easy Database access in the Sidebar.\n  - [Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) controls\n    container host.\n  - [Odoo Snippets](https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-snippets)\n  - [Odoo Developments](https://marketplace.visualstudio.com/items?itemName=scapigliato.vsc-odoo-development) can Grab\n    Odoo Model information from a running Server\n  - [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)\n\n## Basic Usage\n\n1. For Docker on windows: Clone the repo into the WSL2 Filesystem for better IO performance\n2. Have [Traefik](https://github.com/traefik/traefik) Running on `docker.localhost`\n   [Example](https://github.com/joshkreud/traefik_devproxy)\n3. Create `.env` file (see [.env.sample](.env.sample))\n4. Open Devcontianer:\n   1. If you have the Devcontainer CLI: `devcontainer open .`\n   2. Open the Workspace in vscode, press `Cmd+Shift+P`, select `Rebuild and open in Devcontainer`.\n5. From **within the container** start Odoo using one of the following commands:\n   - `make` -> Loads Odoo + Workspace Addons\n   - `make bare` -> Loads Odoo with ony `web` installed.\n   - `make stg` -> Loads copy of staging Odoo Server\n   - The full init script is available via "`wodoo`". (See --help for Options)\n6. Open Odoo `https://${COMPOSE_PROJECT_NAME}.docker.localhost`\\\n   For example `COMPOSE_PROJECT_NAME=wodoo` --> [https://wodoo.docker.localhost](https://wodoo.docker.localhost)\n7. Login with `admin:admin`\n\n## Access to Odoo and Thirdparty addon Source\n\nYou can access the Odoo source by opening the VsCode workspace [full.code-workspace](full.code-workspace) from within\nthe Container.\n\n## Reset Devcontainer Data\n\n### Automatic Reset\n\nThere are 3 Options to reset the Dev Env.\n\n1. From **Outside** the Container run `make reset` in the project root to delete docker volumes and restart the\n   container. (Vscode will prompt to reconnect if still open)\n2. From **Outside** the Container run `make reset-hard` in the project root to force rebuild the main Odoo container and\n   then do the same as `make reset`\n3. From **Inside** the Container run `make reset` to drop the DB and delete varlib and the bootstrap flag.\n\n### Manual Reset\n\n1. Close vscode\n2. Remove app and db container.\n3. Remove volumes: db, odoo_thirdparty, odoo_web, vscode_extensions\n4. Restart Devcontainer\n\n## Debugging\n\nDebugging doesn\'t reliably work in\n[Odoo Multiprocess](https://www.odoo.com/documentation/14.0/developer/misc/other/cmdline.html#multiprocessing) mode. The\ncontainer ships with a Vscode Debug profile, that sets `--workers 0` to enable Debugging Breakpoints.\n\nUse `wodoo shell` to enter an interactive shell.\n\n## Odoo Modules\n\n### Third Party Modules\n\nThe `wodoo` bootstrap function, will download some modules using git. \\\nWhich Repos to download is specified in `odoo_repospec.yml` \\\nNot all of the cloned addons are automatically installed. \\\nInstall them via the Apps Page in Odoo or using `odoo-bin`.\\\nOthers can be dropped as a `.zip` archive in [./thirdparty](./thirdparty)\n',
    'author': 'Joshua Kreuder',
    'author_email': 'Joshua_Kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
