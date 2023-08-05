ARTIFACT_TYPE_SERVABLE = 'artifact_servable'
ARTIFACT_TYPE_IMAGE = 'artifact_image'
ARTIFACT_TYPE_TABLE = 'artifact_table'
ARTIFACT_TYPE_TEXT = 'artifact_text'
ARTIFACT_TYPE_JSON = 'artifact_json'
ARTIFACT_TYPE_SKLEARN_CLF = 'artifact_sklearn_clf_report_json'
ARTIFACT_TYPE_SKLEARN_SL_CONF_MAT = 'artifact_sklearn_sl_conf_matrix_json'
ARTIFACT_TYPE_SKLEARN_ML_CONF_MAT = 'artifact_sklearn_ml_conf_matrix_json'

ARTIFACT_MAP = {
    ".jpg": ARTIFACT_TYPE_IMAGE,
    ".png": ARTIFACT_TYPE_IMAGE,
    ".jpeg": ARTIFACT_TYPE_IMAGE,
    ".txt": ARTIFACT_TYPE_TEXT,
    ".json": ARTIFACT_TYPE_JSON,
    ".h5": ARTIFACT_TYPE_SERVABLE
}

ARTIFACT_SIZE_LIMIT = 1024 * 2  # in MB
ARTIFACT_MULTI_PART_CHUNK_SIZE = 8 * 1024 * 1024  # in MB
ARTIFACT_MULTI_PART_BATCH_SIZE = 92
