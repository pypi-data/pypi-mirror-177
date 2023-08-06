# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['copier_template_tester']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.11.0', 'copier>=7.0.1']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1']}

entry_points = \
{'console_scripts': ['ctt = copier_template_tester.main:run']}

setup_kwargs = {
    'name': 'copier-template-tester',
    'version': '1.0.2',
    'description': 'Test copier templates',
    'long_description': '# copier-template-tester\n\n![./ctt-logo.png](./ctt-logo.png)\n\nParametrize copier templates to test for syntax errors, check the expected output, and to check against copier versions.\n\nNote that `ctt` only tests the `copier copy` operation and doesn\'t check the `update` behavior and any version-specific logic that your template may contain because of how quickly those tests become complex.\n\n## Usage\n\n### Configuration File\n\nWhen creating a copier template repository, I recommend following the nested ["subdirectory" approach](https://copier.readthedocs.io/en/latest/configuring/#subdirectory) so that the directory looks like this:\n\n```sh\n└── template_dir\n│   └── {{ _copier_conf.answers_file }}.jinja\n├── README.md\n├── copier.yml\n└── ctt.toml\n```\n\nCreate a new `ctt.toml` file in the top-level directory of your copier repository. Populate the file to look like the below example.\n\n```toml\n# Specify shared data across all \'output\' destinations\n# Note that the copier.yml defaults are used whenever the key is not set in this file\n[defaults]\nproject_name = "placeholder"\ncopyright_year = 2022\n\n# Parametrize each output with a relative path and optionally any values to override\n[output.".ctt/defaults"]\n\n[output.".ctt/no_all"]\npackage_name = "testing-no-all"\ninclude_all = false\n```\n\n### Pre-Commit Hook\n\nFirst, add this section to your `.pre-commit-config.yml` file:\n\n```yaml\nrepos:\n  - repo: https://github.com/KyleKing/copier-template-tester\n    rev: main\n    hooks:\n      - id: copier-template-tester\n```\n\nInstall and update to the latest revision:\n\n```sh\npre-commit autoupdate\n```\n\nThe run with `pre-commit`:\n\n```sh\npre-commit run --all-files copier-template-tester\n```\n\n### pipx\n\nYou can also try `ctt` as a CLI tool by installing with `pipx`:\n\n```sh\npipx install copier-template-tester\n\ncd ~/your/copier/project\nctt\n```\n\n### More Examples\n\nFor more example code, see the [tests] directory or how this utility is used in a real project: [KyleKing/calcipy_template](https://github.com/KyleKing/calcipy_template)\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n### Open Source Status\n\nWe try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/copier_template_tester)\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/kyleking/copier-template-tester/LICENSE\n[style_guide]: ./docs/STYLE_GUIDE.md\n[tests]: https://github.com/kyleking/copier-template-tester/tests\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/copier-template-tester',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
