# Python LookML Code Generator

A reusable library for boostrapping LookML code for BigQuery datasets with Python.

This library takes a GBQ table and turns it into Looker explores and views using some of the naming conventions, attributes and measures that are used in the Dimensions Data Solutions Team.

Please note that this is an all-purpose generator and most likely requires further manual editing afterwards.

* pypi: https://pypi.org/project/lookml-helper/

## Input
These is all the input data we need to run the script:
- GBQ project and table information

Other options use defaults that can be overridden when calling the script from Python. See  `gbqgen/main.py`

## Output

By default, data gets saved in the home folder (`~`). 

See the `extras` folder for an example.


## Installation 

```bash
pip install lookml-helper
```



## Run as CLI

```bash
$ lookml-helper -b ds-data-solutions-gbq -d dimensions-ai.data_analytics.clinical_trials
Querying dimensions-ai.data_analytics.clinical_trials information schema...
Found 258 fields...
Generating LookML...
Done.
```


## Run from Python

```python
In [1]: import lookmlhelper

In [2]: lookmlhelper.from_gbq("ds-data-solutions-gbq", "dimensions-ai.data_analytics.clinical_trials")
Querying dimensions-ai.data_analytics.clinical_trials information schema...
Found 258 fields...
Generating LookML...
Done.
```



## Developers - first time setup

Create virtual env and install dependencies

```
$ mkvirtualenv lookmlhelper
$ pip -r requirements.txt .
$ pip install --editable .
```

Then you can run

```
$ lookmlhelper
Usage: lookmlhelper [OPTIONS]

  lookmlhelper CLI. Requires both a billproject and dataset to run.

Options:
  --examples              Show some examples
  -b, --billproject TEXT  BILLING PROJECT: the GCP billing project to access
                          resources.
  -d, --dataset TEXT      DATASET: a fully scopes GBQ dataset eg `dimensions-
                          ai.data_analytics.clinical_trials`.
  --help                  Show this message and exit.
```