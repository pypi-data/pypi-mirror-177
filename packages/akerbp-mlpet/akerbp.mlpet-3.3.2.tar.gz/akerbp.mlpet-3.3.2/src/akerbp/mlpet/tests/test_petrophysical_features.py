import numpy as np
import pandas as pd

from akerbp.mlpet import feature_engineering, petrophysical_features
from akerbp.mlpet.dataloader import DataLoader
from akerbp.mlpet.tests.client import CLIENT, CLIENT_FUNCTIONS
from akerbp.mlpet.tests.data.kubeflow_config import ID_COLUMN
from akerbp.mlpet.tests.data.kubeflow_config import (
    KUBEFLOW_MODEL_URL_VSH as KUBEFLOW_MODEL_URL,
)
from akerbp.mlpet.tests.data.kubeflow_config import VSH_HEADER, VSH_KWARGS

WELL = "15/3-5"


def test_guess_bs_from_cali():
    input = pd.DataFrame({"CALI": [6.1, 5.9, 12.0, 12.02]})
    df = petrophysical_features.guess_BS_from_CALI(input)
    assert "BS" in df.columns.tolist()


def test_calculate_cali_bs():
    input = pd.DataFrame({"CALI": np.array([6.1, 5.9, 12.0, 12.02])})
    df = petrophysical_features.calculate_CALI_BS(input)
    assert "CALI-BS" in df.columns.tolist()


def test_calculate_VSH():
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=CLIENT, metadata={"wellbore_name": WELL, "subtype": "BEST"}
    )
    df[ID_COLUMN] = WELL
    df = petrophysical_features.calculate_LFI(df)
    # BS is required but missing in this sequence to init to all nans
    df["BS"] = np.nan
    df = feature_engineering.add_formations_and_groups(
        df, id_column=ID_COLUMN, depth_column="DEPTH"
    )
    df = feature_engineering.add_vertical_depths(
        df, id_column=ID_COLUMN, md_column="DEPTH"
    )

    df_out = petrophysical_features.calculate_VSH(
        df,
        id_column=ID_COLUMN,
        env="prod",
        return_CI=True,
        client=CLIENT_FUNCTIONS,
        keyword_arguments=dict(
            calculate_denneu=True,
            VSH_curves=["GR", "LFI"],
            groups_column_name="GROUP",
            formations_column_name="FORMATION",
            return_only_vsh_aut=False,
            nan_numerical_value=-9999,
            nan_textual_value="MISSING",
        ),
    )
    assert "VSH" in df_out.columns.tolist()


def test_calculate_VSH_call_kubeflow_model_return_vsh_aut_only_no_CI():
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=CLIENT, metadata={"wellbore_name": WELL, "subtype": "BEST"}
    )
    df[ID_COLUMN] = WELL

    df_out = petrophysical_features.calculate_VSH(
        df=df,
        id_column=ID_COLUMN,
        keyword_arguments=VSH_KWARGS,
        kubeflow_model_url=KUBEFLOW_MODEL_URL,
        request_header=VSH_HEADER,
    )
    output_columns = df_out.columns.tolist()
    assert "VSH" in output_columns and "VSH_AUT_P90" not in output_columns


def test_calculate_VSH_call_kubeflow_model_return_composite_curves_no_CI():
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=CLIENT, metadata={"wellbore_name": WELL, "subtype": "BEST"}
    )
    df[ID_COLUMN] = WELL
    keyword_arguments = VSH_KWARGS.copy()
    keyword_arguments["return_only_vsh_aut"] = False

    df_out = petrophysical_features.calculate_VSH(
        df=df,
        id_column=ID_COLUMN,
        keyword_arguments=keyword_arguments,
        kubeflow_model_url=KUBEFLOW_MODEL_URL,
        request_header=VSH_HEADER,
    )
    output_columns = df_out.columns.tolist()
    assert {"VSH", "VSH_GR_AUT_QCFLAG"}.issubset(
        set(output_columns)
    ) and "VSH_AUT_P90" not in output_columns


def test_calculate_VSH_call_kubeflow_model_return_composite_curves_and_CI():
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=CLIENT, metadata={"wellbore_name": WELL, "subtype": "BEST"}
    )
    df[ID_COLUMN] = WELL
    keyword_arguments = VSH_KWARGS.copy()
    keyword_arguments["return_only_vsh_aut"] = False

    df_out = petrophysical_features.calculate_VSH(
        df=df,
        id_column=ID_COLUMN,
        keyword_arguments=keyword_arguments,
        kubeflow_model_url=KUBEFLOW_MODEL_URL,
        request_header=VSH_HEADER,
        return_CI=True,
    )
    output_columns = df_out.columns.tolist()
    assert {"VSH", "VSH_GR_AUT_QCFLAG", "VSH_AUT_P90"}.issubset(set(output_columns))
