# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexus_pcv', 'nexus_pcv.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'errorhandler>=2.0.1,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['nexus-pcv = nexus_pcv.cli.main:main']}

setup_kwargs = {
    'name': 'nexus-pcv',
    'version': '0.1.2',
    'description': 'A CLI tool to perform a pre-change validation on Nexus Dashboard Insights or Network Assurance Engine.',
    'long_description': '[![Tests](https://github.com/netascode/nexus-pcv/actions/workflows/test.yml/badge.svg)](https://github.com/netascode/nexus-pcv/actions/workflows/test.yml)\n![Python Support](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational "Python Support: 3.7, 3.8, 3.9, 3.10")\n\n# nexus-pcv\n\nA CLI tool to perform a pre-change validation on Nexus Dashboard Insights or Network Assurance Engine. It can either work with provided JSON file(s) or a `terraform plan` output from a [Nexus as Code](https://cisco.com/go/nexusascode) project. It waits for the analysis to complete and evaluates the results.\n\n```\n$ nexus-pcv -h\nUsage: nexus-pcv [OPTIONS]\n\n  A CLI tool to perform a pre-change validation on Nexus Dashboard Insights or\n  Network Assurance Engine.\n\nOptions:\n  --version                   Show the version and exit.\n  -v, --verbosity LVL         Either CRITICAL, ERROR, WARNING, INFO or DEBUG.\n  -i, --hostname-ip TEXT      NAE/ND hostname or IP (required, env:\n                              PCV_HOSTNAME_IP).\n  -u, --username TEXT         NAE/ND username (required, env: PCV_USERNAME).\n  -p, --password TEXT         NAE/ND password (required, env: PCV_PASSWORD).\n  -d, --domain TEXT           NAE/ND login domain (optional, default: \'Local\',\n                              env: PCV_DOMAIN).\n  -g, --group TEXT            NAE assurance group name or NDI insights group\n                              name (required, env: PCV_GROUP).\n  -s, --site TEXT             NDI site or fabric name (optional, only required\n                              for NDI, env: PCV_SITE).\n  -n, --name TEXT             NAE/NDI pre-change validation name (optional,\n                              env: PCV_NAME).\n  -s, --suppress-events TEXT  NAE/NDI comma-separated list of events to\n                              suppress (optional, default: \'APP_EPG_NOT_DEPLOY\n                              ED,APP_EPG_HAS_NO_CONTRACT_IN_ENFORCED_VRF\',\n                              env: PCV_SUPPRESS_EVENTS).\n  -t, --timeout INTEGER       NAE/NDI pre-change validation timeout in minutes\n                              (optional, default: 15, env: PCV_TIMEOUT).\n  -f, --file FILE             NAE/NDI proposed change JSON file (optional,\n                              env: PCV_FILE).\n  -t, --nac-tf-plan FILE      NAE/NDI proposed change Terraform plan output\n                              (optional, env: PCV_NAC_TF_PLAN).\n  -o, --output-summary FILE   NAE/NDI summary of new events/anomalies written\n                              to a file (optional, env: PCV_OUTPUT_SUMMARY).\n  -r, --output-url FILE       NAE/NDI link (URL) to pre-change validation\n                              results written to a file (optional, env:\n                              PCV_OUTPUT_URL).\n  -h, --help                  Show this message and exit.\n```\n\n## Installation\n\nPython 3.7+ is required to install `nexus-pcv`. Don\'t have Python 3.7 or later? See [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/).\n\n`nexus-pcv` can be installed in a virtual environment using `pip`:\n\n```\npip install nexus-pcv\n```\n\n## CI/CD Integration\n\nThe tool can easily be integrated with CI/CD workflows. Arguments can either be provided via command line or environment variables. The tool will exit with a non-zero exit code in case of an error or non-suppressed events being discovered during the pre-change analysis. The `--output-summary` and `--output-url` arguments can be used to write a summary and/or a link (URL) to a file, which can then be embedded into notifications (e.g., Webex).\n\n## *Nexus as Code* Integration\n\n*Nexus as Code* allows users to instantiate network fabrics in minutes using an easy to use, opinionated data model. More information about *Nexus as Code* can be found [here](https://cisco.com/go/nexusascode). A planned change can be validated before applying it to a production environment by running a `terraform plan` operation first and then providing the output to `nexus-pcv` to trigger a pre-change validation.\n\n```\nexport PCV_HOSTNAME_IP=10.1.1.1\nexport PCV_USERNAME=admin\nexport PCV_PASSWORD=Cisco123\nexport PCV_GROUP=LAB\nexport PCV_SITE=LAB1\nterraform plan -out=plan.tfplan\nterraform show -json plan.tfplan > plan.json\nnexus-pcv --name "PCV1" --nac-tf-plan plan.json\n```\n',
    'author': 'Daniel Schmidt',
    'author_email': 'danischm@cisco.com',
    'maintainer': 'Daniel Schmidt',
    'maintainer_email': 'danischm@cisco.com',
    'url': 'https://github.com/netascode/nexus-pcv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
