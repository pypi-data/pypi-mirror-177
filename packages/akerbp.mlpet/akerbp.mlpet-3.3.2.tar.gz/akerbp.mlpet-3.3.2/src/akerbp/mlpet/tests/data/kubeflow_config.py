import os

ID_COLUMN = "well_name"
KUBEFLOW_INGRESS_IP = os.environ.get("KUBEFLOW_INGRESS_IP")
KUBEFLOW_MODEL_URL_VSH = f"http://{KUBEFLOW_INGRESS_IP}/v1/models/automatic-vsh/predict"
API_KEY_VSH = os.environ.get("KUBEFLOW_API_KEY")
VSH_HEADER = {"KUBEFLOW_API_KEY": API_KEY_VSH}
VSH_KWARGS = {
    "nan_numerical_value": -9999,
    "nan_textual_value": "MISSING",
    "VSH_curves": ["GR"],
}
