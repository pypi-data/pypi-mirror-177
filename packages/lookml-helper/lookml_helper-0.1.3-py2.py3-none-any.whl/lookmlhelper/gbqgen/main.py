#!/usr/bin/python
# -*- coding: utf-8 -*-


from string import Template
import pandas as pd
import numpy as np
import re
import os
import shutil
import pandas as pd
import itertools
from datetime import datetime


try:
    # if COLAB is available, authenticate with it
    from google.colab import auth
    auth.authenticate_user()
except:
    # we expect a valid GCP environment to be available 
    pass

from .utils import *
from .extract_fields import *
from .gen_explores import write_base_explore, write_joined_explore
from .gen_views import *
# from ..CONFIG import *


# This governs if additional information is churned out

OUTPUT_LOCAL = os.path.join(os.path.expanduser('~'), 'lookmlhelper')



def run_gbq_extraction( gbq_billing_project,
                        gbq_dataset,
                        looker_name="",
                        looker_parent_folder="",
                        fields_w_offset_joins_input="",
                        special_labels=None,
                        exclude_field_paths=None,
                        unnest_suffix="__unnested",
                        special_casts=None,
                        output_folder = None,
                        verbose=False):
    """Query a GBQ table and generates LookML docs for it.

    Parameters
    ----------
    gbq_billing_project : _type_
        _description_
    gbq_dataset : _type_
        _description_
    looker_name : str, optional
        The name used in Looker for the main object being represented, by default the GBQ table name.
    looker_parent_folder : str, optional
        The parent folder name for the Looker structure, by default the GBQ dataset name.
    fields_w_offset_joins_input : str, optional
        Fields that require an offset with explore joins. Expects a comma separated list eg "field1, field2, field3"
    special_labels : dict, optional
        Mappings between fields and labels to be used in Looker, as a dictionary. 
    exclude_field_paths : list, optional
        Exclusion fields list, as a list of strings.
    unnest_suffix : str, optional
        Suffix text to be used in unnested views, by default "__unnested"
    special_casts : dict, optional
        Special rules for casting, by default None
    output_folder : str, optional
        Path where to save the generated LookML, by default '~/lookmlhelper'
    verbose : bool, optional
        Verbose mode, by default False
    """    

    try:
        gbq_resource_name, gbq_datset_name, gbq_table_name = gbq_dataset.strip().split(".")
    except:
        printDebug("ERROR: gbq_dataset must have the format `resource.dataset.table`", "red")

    # defaults
    looker_name = looker_name or gbq_table_name
    pretty_looker_name = looker_name.title().replace("_", " ")
    looker_parent_folder = looker_parent_folder or gbq_datset_name
    if not looker_parent_folder.startswith("/"):
        looker_parent_folder = f"/{looker_parent_folder}"
    special_labels = special_labels or {}
    exclude_field_paths = exclude_field_paths or []
    special_casts = special_casts or {}
    output_folder = output_folder or OUTPUT_LOCAL

    # fill in config object
    CONFIGURATION = get_global_configuration()

    CONFIGURATION['gbq_project_id'] = gbq_billing_project
    CONFIGURATION['gbq_resource_name'] = gbq_resource_name
    CONFIGURATION['gbq_datset_name'] = gbq_datset_name
    CONFIGURATION['gbq_table_name'] = gbq_table_name
    CONFIGURATION['looker_name'] = looker_name
    CONFIGURATION['looker_parent_folder'] = looker_parent_folder
    CONFIGURATION['pretty_looker_name'] = pretty_looker_name
    CONFIGURATION['capital_looker_name'] = pretty_looker_name.upper()
    CONFIGURATION['fields_w_offset_joins'] = [x.strip() for x in fields_w_offset_joins_input.split(",")]
    CONFIGURATION['special_labels'] = special_labels
    CONFIGURATION['exclude_field_paths'] = exclude_field_paths
    CONFIGURATION['unnest_suffix'] = unnest_suffix
    CONFIGURATION['special_casts'] = special_casts
    CONFIGURATION['output_folder'] = output_folder

    printDebug(f"Querying {gbq_dataset} information schema...")

    sql = f"""
        SELECT column_name, field_path, data_type, description
        FROM `{gbq_resource_name}`.{gbq_datset_name}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS
        WHERE table_name = "{gbq_table_name}"
    """
    gbq_metadata = inspect_gbq(sql)
    gbq_metadata["modus"] = gbq_metadata.data_type.apply(get_gbq_mode)

    printDebug(f"Found {len(gbq_metadata)} fields...")
    if exclude_field_paths:
        printDebug(f"Excluding {len(exclude_field_paths)} fields...")

    looker_metadata = gbq_metadata.copy()

    # Exclude all field paths specified above
    for exclude_field_path in exclude_field_paths:
        looker_metadata = looker_metadata[
            ~looker_metadata.field_path.str.startswith(exclude_field_path)
        ]


    looker_metadata["array_parent_field_path"] = looker_metadata.field_path.apply(
        get_array_parent_field_path, looker_metadata=looker_metadata
    )
    looker_metadata["nested_view_name"] = looker_metadata.apply(
        get_nested_view_name, axis=1, 
    )
    looker_metadata["nested_dimension_name"] = looker_metadata.apply(
        get_nested_dimension_name, axis=1,
    )
    looker_metadata["unnested_view_name"] = looker_metadata.apply(
        get_unnested_view_name, axis=1,
    )
    looker_metadata["unnested_dimension_name"] = looker_metadata.apply(
        get_unnested_dimension_name, axis=1, 
    )
    looker_metadata["unnested_sql"] = looker_metadata.apply(get_unnested_sql, axis=1)
    looker_metadata["label"] = looker_metadata.field_path.apply(get_label)
    looker_metadata["label_plural"] = looker_metadata["label"].apply(make_label_plural)
    looker_metadata["group_label"] = looker_metadata.apply(get_group_label, axis=1, looker_metadata=looker_metadata)


    # Make nice top array headers as comments in the coding
    # This is usually if a new column_name starts but this can be sometimes the first child
    # if that field is a struct e.g. patents.orange_book
    looker_metadata["top_header"] = ""

    # Never do this but this is the easiest way to do it and we only have a few rows
    past_column_names = []
    for index, row in looker_metadata.iterrows():
        if row.modus in ["STRUCT", "ARRAY"] and row.column_name not in past_column_names:
            looker_metadata.loc[index, "top_header"] = (
                looker_metadata.loc[looker_metadata.field_path == row.column_name]
                .iloc[0]
                .label
            )
            if row.modus == "ARRAY":
                past_column_names.append(row.column_name)

    if verbose:
        printDebug(
            looker_metadata[
                [
                    "field_path",
                    "data_type",
                    "nested_view_name",
                    "nested_dimension_name",
                    "unnested_view_name",
                    "unnested_dimension_name",
                    "unnested_sql",
                    "label",
                    "label_plural",
                    "group_label",
                ]
            ]
        )

    printDebug(f"Generating LookML in '{output_folder}'...")

    output_path = gen_folders(looker_name, output_folder)

    write_base_explore(output_path, looker_metadata)
    write_joined_explore(output_path, looker_metadata)
    write_raw_array_view(output_path, looker_metadata)
    write_raw_fields_view(output_path, looker_metadata)
    write_unested_array_view(output_path, looker_metadata)
    write_base_view(output_path, looker_metadata)
    write_unnested_view(output_path, looker_metadata)

    printDebug(f"Done.")