# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pii_anonymizer',
 'pii_anonymizer.common',
 'pii_anonymizer.common.tests',
 'pii_anonymizer.spark',
 'pii_anonymizer.spark.acquire',
 'pii_anonymizer.spark.acquire.tests',
 'pii_anonymizer.spark.analyze',
 'pii_anonymizer.spark.analyze.detectors',
 'pii_anonymizer.spark.analyze.detectors.tests',
 'pii_anonymizer.spark.analyze.utils',
 'pii_anonymizer.spark.anonymize',
 'pii_anonymizer.spark.anonymize.tests',
 'pii_anonymizer.spark.report',
 'pii_anonymizer.spark.report.tests',
 'pii_anonymizer.spark.write',
 'pii_anonymizer.spark.write.tests',
 'pii_anonymizer.standalone',
 'pii_anonymizer.standalone.acquire',
 'pii_anonymizer.standalone.acquire.tests',
 'pii_anonymizer.standalone.analyze',
 'pii_anonymizer.standalone.analyze.detectors',
 'pii_anonymizer.standalone.analyze.detectors.tests',
 'pii_anonymizer.standalone.analyze.utils',
 'pii_anonymizer.standalone.analyze.utils.tests',
 'pii_anonymizer.standalone.anonymize',
 'pii_anonymizer.standalone.anonymize.tests',
 'pii_anonymizer.standalone.report',
 'pii_anonymizer.standalone.report.tests',
 'pii_anonymizer.standalone.tests',
 'pii_anonymizer.standalone.tests.config',
 'pii_anonymizer.standalone.write',
 'pii_anonymizer.standalone.write.tests']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.0,<2.0.0', 'pyspark>=3.3.0,<3.4.0']

setup_kwargs = {
    'name': 'pii-anonymizer',
    'version': '0.1.1',
    'description': 'Data Protection Framework is a python library/command line application for identification, anonymization and de-anonymization of Personally Identifiable Information data.',
    'long_description': '# Data Protection Framework\nData Protection Framework is a python library/command line application for identification, anonymization and de-anonymization of Personally Identifiable Information data.\n\nThe framework aims to work on a two-fold principle for detecting PII:\n1. Using RegularExpressions using a pattern\n2. Using NLP for detecting NER (Named Entity Recognitions)\n\n## Common Usage\n1. `pip install pii-anonymizer`\n2. Specify configs in `pii-anonymizer.json`\n3. Choose whether to run in standalone or spark mode with `python -m pii_anonymizer.standalone` or `python -m pii_anonymizer.spark`\n\n## Features and Current Status\n\n### Completed\n * Following Global detectors have been completed:\n   * [x] EMAIL_ADDRESS :  An email address identifies the mailbox that emails are sent to or from. The maximum length of the domain name is 255 characters, and the maximum length of the local-part is 64 characters.\n   * [x] CREDIT_CARD_NUMBER : A credit card number is 12 to 19 digits long. They are used for payment transactions globally.\n\n * Following detectors specific to Singapore have been completed:\n   * [x] PHONE_NUMBER : A telephone number.\n   * [x] FIN/NRIC : A unique set of nine alpha-numeric characters on the Singapore National Registration Identity Card.\n\n * Following anonymizers have been added\n    * [x] Redaction: Deletes all or part of a detected sensitive value.\n    * [x] Encryption :  Encrypts the original sensitive data value using a cryptographic key. Cloud DLP supports several types of tokenization, including transformations that can be reversed, or "re-identified."\n\n### TO-DO\nFollowing features  are part of the backlog with more features coming soon\n * Detectors:\n    * [ ] NAME\n    * [ ] ADDRESS\n * Anonymizers:\n    * [ ] Masking: Replaces a number of characters of a sensitive value with a specified surrogate character, such as a hash (#) or asterisk (*).\n    * [ ] Bucketing: "Generalizes" a sensitive value by replacing it with a range of values. (For example, replacing a specific age with an age range,\n    or temperatures with ranges corresponding to "Hot," "Medium," and "Cold.")\n    * [ ] Replacement: Replaces a detected sensitive value with a specified surrogate value.\n\n\nYou can have a detailed at upcoming features and backlog in this [Github Board](https://github.com/thoughtworks-datakind/anonymizer/projects/1?fullscreen=true)\n\n## Development setup\n1. Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)\n2. Setup hooks and install packages with `make install`\n\n### Config JSON\nAn example for the config JSON is located at `<PROJECT_ROOT>/pii-anonymizer.json`\n```\n{\n  "acquire": {\n    "file_path": <FILE PATH TO YOUR INPUT CSV>,\n    "delimiter": <YOUR CSV DELIMITER>\n  },\n  "analyze": {\n\n  },\n  "report" : {\n    "location" : <PATH TO YOUR REPORT OUTPUT FOLDER>,\n    "level" : <LOG LEVEL>\n  },\n  "anonymize": {\n    "output_file_path" : <PATH TO YOUR CSV OUTPUT FOLDER>\n  }\n}\n```\n\n### Running Tests\nYou can run the tests by running `make test` or triggering shell script located at `<PROJECT_ROOT>/bin/run_tests.sh`\n\n### Trying out on local\n\n##### Anonymizing a delimited csv file\n1. Set up a JSON config file similar to the one seen at the project root.\nIn the \'acquire\' section of the json, populate the input file path and the delimiter.\nIn the \'report\' section, provide the output path, where you want the PII detection report to be generated.\nA \'high\' level report just calls out which columns have PII attributes.\nA \'medium\' level report calls out the percentage of PII in each column and the associated PII (email, credit card, etc)type for the same.\n2. Run the main class - `python -m pii_anonymizer.standalone --config <optionally, path of the config file or leave blank to defaults to pii-anonymizer.json>`\nYou should see the report being appended to the file named \'report_\\<date\\>.log\' in the output path specified in the\nconfig file.\n\n### Packaging\nRun `poetry build` and the `.whl` file will be created in the `dist` folder.\n\n### Licensing\nDistributed under the MIT license. See ``LICENSE`` for more information.\n\n### Contributing\n\nYou want to help out? _Awesome_!\n',
    'author': 'Thoughtworks',
    'author_email': 'thoughtworks@thoughtworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
