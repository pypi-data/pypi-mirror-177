# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elastic', 'elastic.thrunting_tools', 'elastic.thrunting_tools.common']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'elasticsearch>=8.5.0,<9.0.0',
 'prompt-toolkit>=3.0.32,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pygments>=2.13.0,<3.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'scalpl>=0.4.2,<0.5.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['eql-query = elastic.thrunting_tools.eql_query:app',
                     'lucene-query = elastic.thrunting_tools.lucene_query:app']}

setup_kwargs = {
    'name': 'thrunting-tools',
    'version': '8.5.1',
    'description': 'A collection of utilities to help with threat hunting on the command line.',
    'long_description': '# Elastic Security Labs thrunting-tools\n\nHave you ever been threat hunting (hereafter known as "thrunting") in Kibana and thought\n"Gee! I wish I could take these results and do some automation on the command line!".\nWell look no further, fellow thrunter! This repo has just what you need to make your\nautomation adventures a bit easier.\n\nthrunting-tools is a collection of command line utilities for working with data.\n\nThe current list of tools are:\n\n- `eql-query`, a tool to let you perform EQL searches from your shell!\n- `lucene-query`, a tool to let you perform Lucene searches against Elasticsearch in your\n  comfort zone, the command line.\n\n## Installation\n\nThe easiest way to install thrunting-tools is with [pipx](https://pypa.github.io/pipx/). Once\nyou have pipx installed, to install these tools on your path, simply install the latest release\nwith:\n\n```shell\npipx install thrunting-tools\n```\n\nAlternatively, if you\'d like to install with pip and you have your own Python environment, you can\ndo that too.\n\n```shell\npip3 install thrunting-tools\n```\n\nYou can now check that each command was installed.\n\n```shell\neql-query --version\nlucene-query --version\n```\n\n### Docker Usage\n\nLastly, if you want to use a container runtime environment, you can use the latest release from\nthe repository GitHub Container Repository. Currently, we\'re publishing AMD64 and ARM64 images.\n\n```shell\ndocker pull ghcr.io/elastic/securitylabs-thrunting-tools:main\n```\n\nThen, you can run the container and pass your local configuration in to the default\nlocation used by the container, `/config.yml`. (NOTE: the `:z` part of the volume\nspecification is only needed if you use SELinux)\n\n```shell\ndocker run -ti -v "${HOME}/.config/thrunting-tools/config.yml":/config.yml:ro,z \\\n    --rm ghcr.io/elastic/securitylabs-thrunting-tools:latest eql-query --help\n```\n\n## Usage\n\nEach of the commands provide a usage when called with `--help`.\n\n```shell\n$ eql-query --help\n\n Usage: eql-query [OPTIONS] QUERY\n\n╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────╮\n│ *    query      TEXT  Query specified using EQL (See https://ela.st/eql) [required]         │\n╰─────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮\n│ --index        -i      TEXT     Index pattern to search. Defaults to                        │\n│                                 \'.alerts-security.alerts-default,apm-*-transaction*,logs-*\' │\n│ --since        -s      TEXT     Earliest time filter using datemath or datetime             │\n│                                 [default: now-30d/d]                                        │\n│ --before       -b      TEXT     Latest time filter using datemath or datetime               │\n│                                 [default: now]                                              │\n│ --compact      -c               Output one event/sequence per line                          │\n│ --fields       -f      TEXT     Comma separated list of fields to display [default: None]   │\n│ --size         -s      INTEGER  Specify maximum size of result set [default: 100]           │\n│ --config               PATH     Optional path to YAML configuration with settings for       │\n│                                 Elasticsearch                                               │\n│                                 [default:                                                   │\n│                                 /home/user/.config/thrunting-tools/config.yml]           │\n│ --environment  -e      TEXT     Environment name to use from config file (if present)       │\n│                                 [default: default]                                          │\n│ --help                          Show this message and exit.                                 │\n╰─────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\n## Configuration\n\nThere are two ways to pass configuration to the tools: environment variables and configuration files.\n\nThe tools default to looking for the YAML configuration file in the platform-specific\nconfiguration directory (see the `--help` output). If present, configuration groups are\ntop-level keys (e.g. `elasticsearch`), which contain a list of environments. All scripts will\ncheck for the first environment with the name attribute set to `default`  if none is specified\non the command line.\n\nExample configuration file:\n\n```yaml\nelasticsearch:\n  - name: default\n    cloud_id: "security-cluster:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvJGFiY2R="\n    cloud_auth: "elastic:changeme"\n```\n\n## Examples\n\nRun query using `devel` environment configuration\n\n```shell\neql-query -e devel \'malware where event.kind: "alert"\'\n```\n\nUsing `jq` and `wc` to get the number of alert events where `EXCEL.EXE` was the parent process.\n\n```shell\neql-query \'any where event.kind: "alert"\' -c | \\\n    jq \'select(._source.process.parent.name == "EXCEL.EXE")\' -c | wc -l\n```\n\nFind the unique event categories of all events in the last day that triggered based upon a\nrule using the \'sandbox\' environment\n\n```shell\n$ lucene-query --since \'now-1d\' \'rule: *\' -e sandbox -c | \\\n    jq \'._source.event.category[]\' -c -r | sort -u\nnetwork\n```\n\nFind the unique dynamic DNS subdomains of a particular domain resolved in our network in the\nlast month\n\n```shell\nlucene-query --since \'now-1M\' \'dns.question.name: *.duckdns.org\' -c \\\n    | jq \'._source.dns.question.name\' -r | sort -u\n...\n```\n\nFind a list of all the unique agent IDs that resolved a known malware domain within the last 12 months.\n\n```shell\n$ lucene-query --since \'now-12M\' \'dns.question.name: puerto2547.duckdns.org\' -c \\\n    | jq \'._source.agent.id\' -r | sort -u\nec82f608-3d1b-4651-900e-b970c68bbeef\n```\n',
    'author': 'Derek Ditch',
    'author_email': 'dcode@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elastic/securitylabs-thruntingtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
