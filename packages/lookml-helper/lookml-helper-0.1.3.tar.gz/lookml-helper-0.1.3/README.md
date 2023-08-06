# Python LookML Code Generator

A reusable library for boostrapping LookML code for BigQuery datasets with Python.

This library takes a GBQ table and turns it into Looker explores and views using some of the naming conventions, attributes and measures that are used in the Dimensions Data Solutions Team.

Please note that this is an all-purpose generator and most likely requires further manual editing afterwards.

* pypi: https://pypi.org/project/lookml-helper/


## How to Run

You can run it either as a command line application, or using Python e.g. via a script or within a Colab notebook.  

The prerequisite in both cases is an authenticated connection to Google BigQuery. When running via Colab, that's created at runtime via the oauth authentication mechanism.   

## Input
These is all the input data we need to run the script:
- GBQ project and table information

There are other options that normally take defaults values but can be customised when calling the script from Python. See  `gbqgen/main.py`

## Output

By default, data gets saved in the home folder (`~`). 

See the `extras` folder for an example.


## Installation (all users)

```bash
pip install lookml-helper
```


## Installation (developers)

With Python 3.9 and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html)

```bash
$ git clone git@gitlab.com:digital-science/dimensions/data-solutions/looker-lookml-generator.git
$ mkvirtualenv lookml-helper
$ pip install -r requirements.txt
$ pip install -e .
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


## Prerequisites: Accessing BigQuery 

You need to be able to connect to [Google BigQuery](https://cloud.google.com/bigquery/) using Python. This means:

* **Installing the SDK**. Installing & authorizing the the Google Cloud SDK, "gcloud," available [directly from Google](https://cloud.google.com/sdk/docs/install). If you can open a terminal and the `gcloud` command is recognized, it has been sufficiently configured.
* **Setting up a GCP project**. Each time you interact with BigQuery, you need to specify which GCP project you are using. This is generally used for resources access management. More info [here](https://docs.dimensions.ai/bigquery/gcp-setup.html).

> Note: when using Colab, all of the above is handled in the background for you by the standard Colab-GCP connectivity features. 


## Example run as CLI

```bash
$ lookml-helper -b ds-data-solutions-gbq -d dimensions-ai.data_analytics.clinical_trials
Querying dimensions-ai.data_analytics.clinical_trials information schema...
Found 258 fields...
Generating LookML...
Done.
```


## Example run from Python

```python
In [1]: import lookmlhelper

In [2]: lookmlhelper.from_gbq("ds-data-solutions-gbq", "dimensions-ai.data_analytics.clinical_trials")
Querying dimensions-ai.data_analytics.clinical_trials information schema...
Found 258 fields...
Generating LookML...
Done.
```

