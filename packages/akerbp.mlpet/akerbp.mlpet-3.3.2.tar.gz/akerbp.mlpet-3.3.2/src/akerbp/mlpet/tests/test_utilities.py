import os

import pandas as pd
import pytest
import yaml
from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import APIKey

from akerbp.mlpet import utilities as utils
from akerbp.mlpet.tests.data.data import (
    FORMATION_TOPS_MAPPER,
    TEST_DF,
    VERTICAL_DEPTHS_MAPPER,
)
from akerbp.mlpet.tests.data.kubeflow_config import ID_COLUMN, KUBEFLOW_INGRESS_IP
from akerbp.mlpet.tests.data.kubeflow_config import (
    KUBEFLOW_MODEL_URL_VSH as KUBEFLOW_MODEL_URL,
)
from akerbp.mlpet.tests.data.kubeflow_config import VSH_HEADER, VSH_KWARGS

# Assuming COGNITE_API_KEY is set in the environment
credentials = APIKey(os.environ["COGNITE_API_KEY"])
client_config = ClientConfig(
    client_name="test", project="akbp-subsurface", credentials=credentials
)
CLIENT = CogniteClient(client_config)
WELL_NAMES = ["25/10-10"]


def test_get_formation_tops():
    formation_tops_mapper = utils.get_formation_tops(WELL_NAMES, CLIENT)
    assert formation_tops_mapper == FORMATION_TOPS_MAPPER


def test_get_vertical_depths():
    retrieved_vertical_depths = utils.get_vertical_depths(WELL_NAMES, CLIENT)
    # empty_queries should be an empty list for the provided WELL_NAMES
    assert retrieved_vertical_depths == VERTICAL_DEPTHS_MAPPER


def test_remove_wo_label():
    df = utils.drop_rows_wo_label(TEST_DF[["AC", "BS"]], label_column="BS")
    assert df.shape[0] == 8


def test_standardize_names():
    mapper = yaml.load(
        open("src/akerbp/mlpet/tests/data/test_mappings.yaml", "r"),
        Loader=yaml.SafeLoader,
    )
    utils.standardize_names(TEST_DF.columns.tolist(), mapper=mapper)


def test_standardize_group_formation_name():
    assert utils.standardize_group_formation_name("ØRN") == "ORN"


def test_map_formation_group_system():
    tests = pd.Series(["UNDIFFERENTIATED", "FOO BAR", "NO FORMAL NAME 1", "HeGrE"])
    tests = tests.apply(utils.standardize_group_formation_name)
    assert utils.map_formation_group_system(tests, MissingValue=-9999) == (
        ("UNKNOWN FM", -9999, "UNKNOWN FM", -9999),
        ("UNKNOWN GP", -9999, "UNKNOWN GP", "HEGRE GP"),
        (-9999, -9999, -9999, "TRIASSIC SY"),
    )


def test_get_well_metadata():
    metadata = utils.get_well_metadata(client=CLIENT, well_names=WELL_NAMES)
    assert metadata[WELL_NAMES[0]]["CDF_wellName"] == WELL_NAMES[0]


def test_get_cognite_client_no_args_returns_logged_in_client():
    client = utils.get_cognite_client()
    logged_in = client.login.status().logged_in
    assert logged_in


def test_get_cognite_client_pass_api_key_returns_logged_in_client():
    api_key = os.environ["COGNITE_API_KEY"]
    client = utils.get_cognite_client(
        cognite_api_key=api_key,
    )
    logged_in = client.login.status().logged_in
    assert logged_in


def test_get_cognite_client_wrong_api_key_return_client_not_logged_in():
    api_key = "wrong_key_go_home"
    client = utils.get_cognite_client(cognite_api_key=api_key)
    logged_in = client.login.status().logged_in
    assert not logged_in


def test_run_kubeflow_model_automatic_vsh_return_metadata():
    metadata_url = f"http://{KUBEFLOW_INGRESS_IP}/v1/models/automatic-vsh/metadata"
    metadata = utils.run_kubeflow_model(
        in_data={"input": {}}, model_url=metadata_url, header=VSH_HEADER
    )
    expected_metadata_fields = [
        "keyword_arguments",
        "model_name",
        "optional_input",
        "optional_output_curves",
        "output_curves",
        "petrel_exposure",
        "required_input",
        "supports_external_retrieval",
    ]
    assert list(metadata.keys()) == expected_metadata_fields


def test_run_kubeflow_model_automatic_vsh_invalid_endpoint_raise_valueerror():
    url = f"http://{KUBEFLOW_INGRESS_IP}/v1/models/automatic-vsh/not_a_valid_endpoint"
    with pytest.raises(ValueError):
        utils.run_kubeflow_model(in_data={"input": {}}, model_url=url)


def test_run_kubeflow_model_automatic_vsh_return_only_vsh_aut():
    df = TEST_DF.rename(columns={"DENC": "DEN"}).fillna(
        VSH_KWARGS["nan_numerical_value"]
    )
    in_data = {
        "input": [
            {
                "well": df.well_name.iloc[0],
                "input_logs": df.to_dict(orient="list"),
                "keyword_arguments": VSH_KWARGS,
            }
        ]
    }
    output_keys = utils.run_kubeflow_model(
        in_data=in_data,
        model_url=KUBEFLOW_MODEL_URL,
        header=VSH_HEADER,
    )[0].keys()
    expected_output_keys = ["VSH_AUT", "well"]
    assert list(output_keys) == expected_output_keys


def test_run_kubeflow_model_automatic_vsh_return_additional_curves():
    df = TEST_DF.rename(columns={"DENC": "DEN"}).fillna(
        VSH_KWARGS["nan_numerical_value"]
    )
    keyword_arguments = VSH_KWARGS.copy()
    keyword_arguments["return_only_vsh_aut"] = False
    in_data = {
        "input": [
            {
                "well": df.well_name.iloc[0],
                "input_logs": df.to_dict(orient="list"),
                "keyword_arguments": keyword_arguments,
            }
        ]
    }
    output_keys = utils.run_kubeflow_model(
        in_data=in_data,
        model_url=KUBEFLOW_MODEL_URL,
        header=VSH_HEADER,
    )[0].keys()
    expected_output_keys = [
        "BS_CHANGE",
        "GR_sh",
        "GR_ss",
        "VSH_AUT",
        "VSH_AUT_P025",
        "VSH_AUT_P10",
        "VSH_AUT_P16",
        "VSH_AUT_P84",
        "VSH_AUT_P90",
        "VSH_AUT_P975",
        "VSH_GR_AUT",
        "VSH_GR_AUT_INTER_RATIO",
        "VSH_GR_AUT_QCFLAG",
        "well",
    ]
    assert list(output_keys) == expected_output_keys


def test_run_kubeflow_model_automatic_vsh_raise_exception_wrong_address():
    ingress_ip_wrong = "1.2.3"
    url = f"http://{ingress_ip_wrong}/v1/models/automatic-vsh/metadata"
    with pytest.raises(ValueError):
        utils.run_kubeflow_model(in_data={"input": {}}, model_url=url)


def test_run_kubeflow_model_automatic_vsh_no_request_header_raise_exception():
    with pytest.raises(ValueError):
        utils.run_kubeflow_model(in_data={"input": {}}, model_url=KUBEFLOW_MODEL_URL)


def test_run_kubeflow_model_automatic_vsh_raise_exception_internal_server_error():
    df = TEST_DF.drop(columns="DEPTH")
    in_data = {
        "input": [
            {
                "well": df.well_name.iloc[0],
                "input_logs": df.fillna(-9999).to_dict(orient="list"),
                "keyword_arguments": VSH_KWARGS,
            }
        ]
    }
    with pytest.raises(ValueError):
        utils.run_kubeflow_model(
            in_data=in_data, model_url=KUBEFLOW_MODEL_URL, header=VSH_HEADER
        )


def test_run_deployed_models_call_kubeflow_model_automatic_vsh_return_only_vsh():
    df = TEST_DF.rename(columns={"DENC": "DEN"}).fillna(
        VSH_KWARGS["nan_numerical_value"]
    )
    original_columns = set(df.columns)
    output_df = utils.run_deployed_model(
        df=df,
        id_column=ID_COLUMN,
        keyword_arguments=VSH_KWARGS,
        kubeflow_model_url=KUBEFLOW_MODEL_URL,
        header=VSH_HEADER,
    )
    output_columns = set(output_df.columns)
    assert output_columns - original_columns == {
        "VSH_AUT",
        "well",
    }, "Curve 'VSH_AUT' was not added to the dataframe"


def test_run_deployed_model_call_kubeflow_model_missing_DEPTH_column_raise_exception():
    df = TEST_DF.drop(columns="DEPTH")
    with pytest.raises(ValueError):
        utils.run_deployed_model(
            df=df,
            id_column=ID_COLUMN,
            keyword_arguments=VSH_KWARGS,
            kubeflow_model_url=KUBEFLOW_MODEL_URL,
            header=VSH_HEADER,
        )


def test_run_deployed_models_call_kubeflow_model_automatic_vsh_return_composite_curves():
    df = TEST_DF.rename(columns={"DENC": "DEN"}).fillna(
        VSH_KWARGS["nan_numerical_value"]
    )
    original_columns = set(df.columns)
    keyword_arguments = VSH_KWARGS.copy()
    keyword_arguments["return_only_vsh_aut"] = False
    output_df = utils.run_deployed_model(
        df=df,
        id_column=ID_COLUMN,
        keyword_arguments=keyword_arguments,
        kubeflow_model_url=KUBEFLOW_MODEL_URL,
        header=VSH_HEADER,
    )
    output_columns = set(output_df.columns)
    assert output_columns - original_columns == {
        "BS_CHANGE",
        "GR_sh",
        "GR_ss",
        "VSH_AUT",
        "VSH_AUT_P025",
        "VSH_AUT_P10",
        "VSH_AUT_P16",
        "VSH_AUT_P84",
        "VSH_AUT_P90",
        "VSH_AUT_P975",
        "VSH_GR_AUT",
        "VSH_GR_AUT_INTER_RATIO",
        "VSH_GR_AUT_QCFLAG",
        "well",
    }, "Curve 'VSH_AUT' and the composite VSH curves were not added to the dataframe"
