# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psql-to-models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'sqlalchemy>=1.4.44,<2.0.0']

setup_kwargs = {
    'name': 'psql-to-models',
    'version': '0.1.0',
    'description': 'Use regex patterns to match PostgreSQL schemas and output SQLAlchemy and Pydantic Models. Designed for FastAPI.',
    'long_description': '# PSQL TO MODELS\n\nUse regex patterns to match PostgreSQL schemas and output SQLAlchemy and Pydantic Models. \n\nDesigned for FastAPI.\n\n## Install\n\nRequires Python 3.10.\n\n```shell\ngit clone git@github.com:AlbertoV5/psql-to-models.git\n```\n\n```shell\ncd psql-to-models\n```\nInstall in editable mode.\n```shell\npip install -e .\n```\n\n## Usage\n\n```shell\npython -m psql-to-models\n```\nBefore.\n```shell\nschema.sql\n```\nAfter.\n```shell\nmodels_alchemy.py\tschema.sql\nmodels_pydantic.py\n```\n\n## Results Example\n\nSQL Input\n```sql\nDROP TABLE IF EXISTS DATETIMEEVENTS CASCADE;\nCREATE TABLE DATETIMEEVENTS\n(\n  ROW_ID INT NOT NULL,\n\tSUBJECT_ID INT NOT NULL,\n\tHADM_ID INT,\n\tICUSTAY_ID INT,\n\tITEMID INT NOT NULL,\n\tCHARTTIME TIMESTAMP(0) NOT NULL,\n\tSTORETIME TIMESTAMP(0) NOT NULL,\n\tCGID INT NOT NULL,\n\tVALUE TIMESTAMP(0),\n\tVALUEUOM VARCHAR(50) NOT NULL,\n\tWARNING SMALLINT,\n\tERROR SMALLINT,\n\tRESULTSTATUS VARCHAR(50),\n\tSTOPPED VARCHAR(50),\n\tCONSTRAINT datetime_rowid_pk PRIMARY KEY (ROW_ID)\n) ;\n\nDROP TABLE IF EXISTS DIAGNOSES_ICD CASCADE;\nCREATE TABLE DIAGNOSES_ICD\n(\n  ROW_ID INT NOT NULL,\n\tSUBJECT_ID INT NOT NULL,\n\tHADM_ID INT NOT NULL,\n\tSEQ_NUM INT,\n\tICD9_CODE VARCHAR(10),\n\tCONSTRAINT diagnosesicd_rowid_pk PRIMARY KEY (ROW_ID)\n) ;\n```\nSQLALchemy Output\n\n```python\nclass Datetimeevents(Base):\n\n    __tablename__ = "datetimeevents"\n\n    row_id = Column(Integer, nullable=False, primary_key=True)\n    subject_id = Column(Integer, nullable=False)\n    hadm_id = Column(Integer)\n    icustay_id = Column(Integer)\n    itemid = Column(Integer, nullable=False)\n    charttime = Column(TIMESTAMP(0), nullable=False)\n    storetime = Column(TIMESTAMP(0), nullable=False)\n    cgid = Column(Integer, nullable=False)\n    value = Column(TIMESTAMP(0))\n    valueuom = Column(String(50), nullable=False)\n    warning = Column(SmallInteger)\n    error = Column(SmallInteger)\n    resultstatus = Column(String(50))\n    stopped = Column(String(50))\n\n\nclass Diagnoses_icd(Base):\n\n    __tablename__ = "diagnoses_icd"\n\n    row_id = Column(Integer, nullable=False, primary_key=True)\n    subject_id = Column(Integer, nullable=False)\n    hadm_id = Column(Integer, nullable=False)\n    seq_num = Column(Integer)\n    icd9_code = Column(String(10))\n```\n\nPydantic Output\n\n```python\nclass Datetimeevents(BaseModel):\n\n    row_id: int\n    subject_id: int\n    hadm_id: int | None\n    icustay_id: int | None\n    itemid: int\n    charttime: datetime\n    storetime: datetime\n    cgid: int\n    value: datetime | None\n    valueuom: str\n    warning: int | None\n    error: int | None\n    resultstatus: str | None\n    stopped: str | None\n\n    class Config:\n        orm_mode = True\n\n\nclass Diagnoses_icd(BaseModel):\n\n    row_id: int\n    subject_id: int\n    hadm_id: int\n    seq_num: int | None\n    icd9_code: str | None\n\n    class Config:\n        orm_mode = True\n```\n\n## Supported Queries\n\n```sql\nCREATE TABLE *\n```\n\n```sql\nNOT NULL\n```\n\n```sql\nCONSTRAINT UNIQUE\nCONSTRAINT PRIMARY KEY\n```\n\n## Constants\n\nMake sure to edit the header constants under __ main __.py\n\n```python\nALCHEMY_HEADER = \'\'\'"""\nSQLAlchemy Models\n"""\nfrom sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, SmallInteger\nfrom sqlalchemy.dialects.postgresql import DOUBLE_PRECISION\nfrom db.setup import Base\n\n\'\'\'\n```\n\nYou can always extend the supported types by editing the TYPE_LOOKUP dict in the types.py file.\n\n```python\nTYPE_LOOKUP: dict[str, tuple[str, str]] = {\n    "INT": ("Integer", "int"),\n    "SMALLINT": ("SmallInteger", "int"),\n    "VARCHAR": ("String", "str"),\n    "TIMESTAMP": ("TIMESTAMP", "datetime"),\n    "DOUBLE": ("DOUBLE_PRECISION", "float"),\n    "CHAR": ("CHAR", "str"),\n    "TEXT": ("String", "str"),\n}\n"""Values are tuples of SQLAlchemy Model Type and Pydantic/Python Type."""\n```\n\n## Notes\n\n- This utility is meant to be modified to match every case that\'s why the installation is in editable mode.\n- The __ main __ .py file contains all the necessary logic and header configs.\n- The types.py file contains a lookup table for the postgresql -> models type lookup.\n- The header assumes a path for the SQLAlchemy Base so make sure to change it to match yours, etc.\n\n## Plans\n\n- A more robust tool can be created which uses .toml files (or whatever) for configuration instead of python files so there is no need for editable installation.\n- The applications are Postgresql schemas with FastAPI but the tool can be generalized even further to support different types for other RDMS and frameworks.\n- I\'ll add support for more queries as I find them in my day-to-day work but feel free to contribute!\n',
    'author': 'AlbertoV5',
    'author_email': '58243333+AlbertoV5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
