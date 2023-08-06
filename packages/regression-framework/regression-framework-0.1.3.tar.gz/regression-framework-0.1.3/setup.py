# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regression_framework',
 'regression_framework.bp',
 'regression_framework.dmo',
 'regression_framework.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'regression-framework',
    'version': '0.1.3',
    'description': 'Provide a Framework for Regression Testing',
    'long_description': '# Regression Framework\nThis microservice creates a framework for running regression tests\n\n## Sample Test Case\nThe header specifies the `runner` and the `comparator`.\n\nThe `runner` is the name of the function that will be used to create the *actual results*.\n\nThe `comparator` is the name of the function that will be used to compare the *actual results* to the *expected results*.\n\nEach test file can contain multiple test cases.\n\nBy convention, each test file should correspond to an issue in GitHub.\n\nEach test file should test a single aspect or function of the system, using as many variations in input as are necessary to ensure the design is functional.\n\n```yaml\nengine:\n  runner: "mutato"\n  comparator: "mutato"\n  loglevel: ERROR\n  ontologies:\n    - unitest\n\n## ---------------------------------------------------------- ##\n## Purpose:     Testing Swap for "Doctoral Degree"\n## Reference:   https://github.com/craigtrim/owl-parse/issues/6\n## ---------------------------------------------------------- ##\n\ncases:\n  - id: 06-01\n    ## ---------------------------------------------------------- ##\n    ##  Purpose:    Span \'doctoral degree\'\n    ## ---------------------------------------------------------- ##\n    input: regression/inputs/tokens-0001.json\n    output:\n      - normal: "doctoral_degree"\n```\n\n## Driver Tutorial\nEach project that implements this service will need to create a *driver*.\n\nThe driver is responsible for calling `regression-framework\\regression_framework\\bp\\regression_api.py` with the correct parameters, as well as implementing the runner(s) and comparator(s).\n\n### Driver\nA simple but functional driver looks like this:\n```python\nimport os\nfrom typing import Callable\nfrom baseblock import FileIO\nfrom baseblock import BaseObject\nfrom regression_framework.bp import RegressionAPI\n\nclass RegressionDriver(BaseObject):\n\n    def __init__(self):\n        BaseObject.__init__(self, __name__)\n\n    def find_runner(self,\n                    d_test_case: dict) -> Callable:\n\n        runner_name = d_test_case[\'engine\'][\'runner\']\n\n        if runner_name == "mutato":\n            return self.runner\n\n        raise NotImplementedError(runner_name)\n\n    def find_comparator(self,\n                        d_test_case: dict) -> Callable:\n\n        runner_name = d_test_case[\'engine\'][\'runner\']\n\n        if runner_name == "mutato":\n            return self.comparator\n\n        raise NotImplementedError(runner_name)\n\n    def run(self):\n\n        api = RegressionAPI(find_runner=self.find_runner,\n                            find_comparator=self.find_comparator)\n\n        api.process(FileIO.join_cwd("regression/cases"))\n```\nNote that the driver must implement a finder method for the runner and comparator.\n\nThe regression framework supports the notion of multiple runners and multiple comparators and each corresponds to this aspect of the test file:\n```yaml\nengine:\n  runner: "mutato"\n  comparator: "mutato"\n```\n\n### Runner\nThe runner (in this case) looks like this:\n```python\ndef runner(self,\n            ontologies: list,\n            input_text: str) -> str:\n\n    from owl_parse import owl_parse\n\n    def get_content() -> list:\n        if FileIO.exists(input_text):\n            return FileIO.read_json(input_text)\n        raise NotImplementedError(input_text)\n\n    absolute_path = FileIO.join_cwd(\'resources/testing\')\n\n    return owl_parse(tokens=get_content(),\n                        ontology_name=ontologies[0],\n                        absolute_path=absolute_path)\n```\nIt is a simple invocation of a known method, with the correct parameters, and the results are returned.\n\n### Comparator\nThe comparator looks like this:\n```python\ndef comparator(self,\n                actual_results: object,\n                expected_results: object) -> bool:\n\n    def compare_normal_attribute(expected_value: str) -> bool:\n        for actual_result in actual_results:\n            if \'normal\' in actual_result:\n                if actual_result[\'normal\'] == expected_value:\n                    return True\n        return False\n\n    for expected_result in expected_results:\n        if \'normal\' in expected_result:\n            if not compare_normal_attribute(expected_result[\'normal\']):\n                return False\n\n    return True\n```\nThe actual results are searched and if the expected value(s) are found, the function will return a truth value.\n\nThe full implementation is here:\nhttps://github.com/craigtrim/regression-framework/issues/2\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/regression-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
