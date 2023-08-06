# automation_helper

automation_helper is a Python library that speeds up automation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install automation_helper.

```bash
pip install automation-helper
```

### Get started
How to use this lib:

```Python
from helper.kpi import KPI
from helper.config import ConfigINI
from helper.config import ConfigJSON
from helper.db_connector import DBConnector
from helper.reports_utils import reports_utils
from helper.logger import Logger

log = Logger("logs", "logs.log")

log.info("------------- Start Process -------------")
```
