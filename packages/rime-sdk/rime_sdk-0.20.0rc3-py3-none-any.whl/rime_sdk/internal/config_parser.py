"""Parse json config to proto."""
import copy
import json
from copy import deepcopy
from typing import Any, List, Optional, Tuple, TypeVar

import pandas as pd
from google.protobuf.message import Message

from rime_sdk.protos.ri.api.modeltesting.incremental_config_pb2 import (
    ImagesIncrementalConfig,
    NLPIncrementalConfig,
    TabularIncrementalConfig,
    TypedIncrementalConfig,
)
from rime_sdk.protos.ri.api.resultsynthesizer.result_message_pb2 import DataType
from rime_sdk.protos.ri.schema.cliconfig.cli_config_pb2 import (
    EmbeddingInfo,
    HuggingFaceSingleDataLoadingInfo,
    ImagesCLIConfig,
    ImagesDataInfo,
    ImagesSingleDataFileInfo,
    ImagesSingleDataInfo,
    NLPCLIConfig,
    NLPDataInfo,
    NLPSingleDataFileInfo,
    NLPSingleDataInfo,
    RankingInfo,
    SingleDataCollectorInfo,
    SingleDataLoadingInfo,
    SingleDeltaLakeInfo,
    SinglePredictionInfo,
    TabularCLIConfig,
    TabularDataInfo,
    TabularSingleDataFileInfo,
    TabularSingleDataInfo,
    TabularSingleDataInfoParams,
    TypedCLIConfig,
    UnstructuredEmbeddingInfo,
    UnstructuredSingleDataInfoParams,
)


def _formatted_time_to_int_time(timestamp_str: str) -> int:
    """Convert formatted time to integer time."""
    # TODO: change function once we replace protobuf start_time/end_time
    # int type with protobuf Timestamp type
    # TODO: consolidate timestamp format with rime-engine
    # NOTE: we use pd.to_datetime instead of datetime.strptime because
    # to_datetime allows a subset of values (e.g. just year and month)
    timestamp = pd.to_datetime(timestamp_str)
    return int(timestamp.timestamp())


def convert_tabular_params_to_proto(
    config: dict,
) -> Optional[TabularSingleDataInfoParams]:
    """Convert tabular params dictionary to proto."""
    proto_names = [
        field.name for field in TabularSingleDataInfoParams.DESCRIPTOR.fields
    ]
    param_config = {name: config.pop(name) for name in proto_names if name in config}
    if len(param_config) == 0:
        return None
    if "loading_kwargs" in param_config and param_config["loading_kwargs"] is not None:
        param_config["loading_kwargs"] = json.dumps(param_config["loading_kwargs"])
    if "ranking_info" in param_config and param_config["ranking_info"] is not None:
        param_config["ranking_info"] = RankingInfo(**param_config["ranking_info"])
    if "embeddings" in param_config and param_config["embeddings"] is not None:
        param_config["embeddings"] = [
            EmbeddingInfo(**info) for info in param_config["embeddings"]
        ]
    if "intersections" in param_config and param_config["intersections"] is not None:
        param_config["intersections"] = param_config["intersections"]
    return TabularSingleDataInfoParams(**param_config)


def convert_single_tabular_data_info_to_proto(config: dict) -> TabularSingleDataInfo:
    """Convert a dictionary to single tabular data info proto message."""
    tabular_params = convert_tabular_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        single_data_file_info_proto = TabularSingleDataFileInfo(
            file_name=config.pop("file_name"),
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_file_info=single_data_file_info_proto,
        )
    elif config_type == "custom":
        loader_kwargs_json = ""
        if "loader_kwargs" in config and "loader_kwargs_json" in config:
            raise ValueError(
                "Got both loader_kwargs and loader_kwargs_json, "
                "but only one should be provided."
            )
        elif "loader_kwargs" in config:
            # This can be None, but we don't want to set, so check first.
            _val = config.pop("loader_kwargs")
            if _val is not None:
                loader_kwargs_json = json.dumps(_val)
        elif "loader_kwargs_json" in config:
            # This can be None, but we don't want to set, so check first.
            _val = config.pop("loader_kwargs_json")
            if _val is not None:
                loader_kwargs_json = _val
        else:
            pass
        single_data_loading_info_proto = SingleDataLoadingInfo(
            load_path=config.pop("load_path"),
            load_func_name=config.pop("load_func_name"),
            loader_kwargs_json=loader_kwargs_json,
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_loading_info=single_data_loading_info_proto,
        )
    elif config_type == "data_collector":
        start_time = _formatted_time_to_int_time(config.pop("start_time"))
        end_time = _formatted_time_to_int_time(config.pop("end_time"))
        single_data_collector_info_proto = SingleDataCollectorInfo(
            start_time=start_time, end_time=end_time
        )
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_data_collector_info=single_data_collector_info_proto,
        )
    elif config_type == "delta_lake":
        # note: if using SDK, server_hostname/http_path will get populated
        # by the data source manager.
        # still keep if used in rime-engine though
        start_time = _formatted_time_to_int_time(config.pop("start_time"))
        end_time = _formatted_time_to_int_time(config.pop("end_time"))
        single_delta_lake_info_proto = SingleDeltaLakeInfo(
            table_name=config.pop("table_name"),
            start_time=start_time,
            end_time=end_time,
            time_col=config.pop("time_col"),
        )
        if "server_hostname" in config:
            single_delta_lake_info_proto.server_hostname = config.pop("server_hostname")
        if "http_path" in config:
            single_delta_lake_info_proto.http_path = config.pop("http_path")
        proto = TabularSingleDataInfo(
            single_params=tabular_params,
            single_delta_lake_info=single_delta_lake_info_proto,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")
    if config:
        raise ValueError(
            f"Found parameters in the data info config that do not belong: {config}"
        )
    return proto


def convert_default_tabular_data_info_to_split(
    config: dict,
) -> Tuple[TabularSingleDataInfo, TabularSingleDataInfo]:
    """Convert default TabularDataInfo config to split ref and eval SingleDataInfo protos."""
    try:
        ref_config = {"file_name": config.pop("ref_path")}
        eval_config = {"file_name": config.pop("eval_path")}
    except KeyError:
        raise ValueError("Missing ref_path and/or eval_path specification")
    if "ref_pred_path" in config:
        ref_config["pred_path"] = config.pop("ref_pred_path")
    if "eval_pred_path" in config:
        eval_config["pred_path"] = config.pop("eval_pred_path")
    ref_config.update(config)
    eval_config.update(config)
    ref_data_info = convert_single_tabular_data_info_to_proto(ref_config)
    eval_data_info = convert_single_tabular_data_info_to_proto(eval_config)
    return ref_data_info, eval_data_info


def convert_tabular_data_info_to_proto(config: dict) -> TabularDataInfo:
    """Convert a dictionary to tabular data info proto message."""
    config_type = config.get("type", "default")

    if config_type == "default":
        ref_data_info, eval_data_info = convert_default_tabular_data_info_to_split(
            config
        )
    elif config_type == "custom":
        # TabularDataLoadingInfo
        eval_config = config.copy()
        if "ref_pred_path" in config:
            config["pred_path"] = config.pop("ref_pred_path")
            del eval_config["ref_pred_path"]
        if "eval_pred_path" in config:
            eval_config["pred_path"] = eval_config.pop("eval_pred_path")
            del config["eval_pred_path"]
        config["load_func_name"] = "get_ref_data"
        ref_data_info = convert_single_tabular_data_info_to_proto(config)
        eval_config["load_func_name"] = "get_eval_data"
        eval_data_info = convert_single_tabular_data_info_to_proto(eval_config)
    elif config_type == "split":
        eval_data_info = convert_single_tabular_data_info_to_proto(
            config["eval_data_info"]
        )
        ref_data_info = convert_single_tabular_data_info_to_proto(
            config["ref_data_info"]
        )
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")

    return TabularDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_tabular_config_to_proto(config: dict) -> TabularCLIConfig:
    """Convert config to tabular proto."""
    # pop to remove from original config dict
    data_info = convert_tabular_data_info_to_proto(config.pop("data_info"))
    proto = TabularCLIConfig(data_info=data_info)
    config_field_names = [field.name for field in TabularCLIConfig.DESCRIPTOR.fields]
    for name in config_field_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def convert_single_unstructured_params_to_proto(
    config: dict,
) -> Optional[UnstructuredSingleDataInfoParams]:
    """Convert unstructured params dictionary to proto."""
    complicated_fields = {"prediction_info", "embeddings"}
    proto_names = [
        field.name
        for field in UnstructuredSingleDataInfoParams.DESCRIPTOR.fields
        if field.name not in complicated_fields
    ]
    param_config = {name: config.pop(name) for name in proto_names if name in config}
    if "prediction_info" in config and config["prediction_info"] is not None:
        single_pred_info = SinglePredictionInfo(**config["prediction_info"])
        param_config["prediction_info"] = single_pred_info
    if "embeddings" in config and config["embeddings"] is not None:
        embeddings = [
            UnstructuredEmbeddingInfo(**info) for info in config["embeddings"]
        ]
        param_config["embeddings"] = embeddings
    return UnstructuredSingleDataInfoParams(**param_config) if param_config else None


def convert_single_nlp_data_info_to_proto(config: dict) -> NLPSingleDataInfo:
    """Convert a dictionary to single nlp data info proto message."""
    unstructured_params = convert_single_unstructured_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        return NLPSingleDataInfo(
            single_data_file_info=NLPSingleDataFileInfo(file_name=config["file_name"]),
            single_params=unstructured_params,
        )
    elif config_type == "custom":
        loader_kwargs_json = ""
        if "loader_kwargs" in config and config["loader_kwargs"] is not None:
            loader_kwargs_json = json.dumps(config["loader_kwargs"])
        if "loader_kwargs_json" in config and config["loader_kwargs_json"] is not None:
            loader_kwargs_json = config["loader_kwargs_json"]
        single_data_loading_info = SingleDataLoadingInfo(
            load_path=config["load_path"],
            load_func_name=config["load_func_name"],
            loader_kwargs_json=loader_kwargs_json,
        )
        return NLPSingleDataInfo(
            single_data_loading_info=single_data_loading_info,
            single_params=unstructured_params,
        )
    elif config_type == "huggingface":
        huggingface_single_info = HuggingFaceSingleDataLoadingInfo(
            dataset_uri=config["dataset_uri"],
            split_name=config["split_name"],
            text_key=config.get("text_key", "text"),
            loading_params_json=json.dumps(config.get("loading_params")),
        )
        if "label_key" in config:
            huggingface_single_info.label_key = json.dumps(config["label_key"])
        if config.get("text_pair_key") is not None:
            huggingface_single_info.text_pair_key = config["text_pair_key"]
        return NLPSingleDataInfo(
            huggingface_single_data_loading_info=huggingface_single_info,
            single_params=unstructured_params,
        )
    elif config_type == "delta_lake":
        start_time = _formatted_time_to_int_time(config["start_time"])
        end_time = _formatted_time_to_int_time(config["end_time"])
        single_delta_lake_info_proto = SingleDeltaLakeInfo(
            server_hostname=config["server_hostname"],
            http_path=config["http_path"],
            table_name=config["table_name"],
            start_time=start_time,
            end_time=end_time,
            time_col=config["time_col"],
        )
        return NLPSingleDataInfo(
            single_delta_lake_info=single_delta_lake_info_proto,
            single_params=unstructured_params,
        )
    elif config_type == "data_collector":
        start_time = _formatted_time_to_int_time(config["start_time"])
        end_time = _formatted_time_to_int_time(config["end_time"])
        single_data_collector_info_proto = SingleDataCollectorInfo(
            start_time=start_time, end_time=end_time
        )
        if unstructured_params is not None and unstructured_params.HasField(
            "prediction_info"
        ):
            raise ValueError(
                "'prediction_info' cannot be specified with data config"
                f" of type {config_type}"
            )
        return NLPSingleDataInfo(
            single_data_collector_info=single_data_collector_info_proto,
            single_params=unstructured_params,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")


def _get_default_nlp_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get default NLP config type data info split configs."""
    ref_config = {"file_name": config.pop("ref_path")}
    eval_config = {"file_name": config.pop("eval_path")}
    ref_config.update(config)
    eval_config.update(config)
    return ref_config, eval_config


def _get_custom_nlp_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get custom NLP config type data info split configs."""
    ref_config = {"load_func_name": "get_ref_data"}
    eval_config = {"load_func_name": "get_eval_data"}
    ref_config.update(config)
    eval_config.update(config)
    return ref_config, eval_config


def _get_huggingface_data_info_split_configs(config: dict) -> Tuple[dict, dict]:
    """Get huggingface config type data info split configs."""
    ref_config, eval_config = {}, {}
    ref_config["split_name"] = config.pop("ref_split", "train")
    eval_config["split_name"] = config.pop("eval_split", "test")
    if "eval_label_key" in config:
        eval_config["label_key"] = config.pop("eval_label_key")
    ref_config.update(config)
    if "label_key" in config:
        del config["label_key"]
    eval_config.update(config)
    return ref_config, eval_config


def convert_nlp_data_info_to_proto(config: dict) -> NLPDataInfo:
    """Convert config to proto message for nlp data."""
    config_type = config.get("type", "default")
    if config_type == "default":
        ref_config, eval_config = _get_default_nlp_data_info_split_configs(config)
    elif config_type == "custom":
        ref_config, eval_config = _get_custom_nlp_data_info_split_configs(config)
    elif config_type == "huggingface":
        ref_config, eval_config = _get_huggingface_data_info_split_configs(config)
    elif config_type == "split":
        ref_config = config["ref_data_info"]
        eval_config = config["eval_data_info"]
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")
    ref_data_info = convert_single_nlp_data_info_to_proto(ref_config)
    eval_data_info = convert_single_nlp_data_info_to_proto(eval_config)
    return NLPDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_nlp_config_to_proto(config: dict) -> NLPCLIConfig:
    """Convert config to nlp proto."""
    # pop to remove from original config dict
    data_info = convert_nlp_data_info_to_proto(config.pop("data_info"))
    proto = NLPCLIConfig(data_info=data_info)
    config_names = [field.name for field in NLPCLIConfig.DESCRIPTOR.fields]
    for name in config_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def convert_single_images_data_info_to_proto(config: dict) -> ImagesSingleDataInfo:
    """Convert a dictionary to single image data info proto message."""
    unstructured_params = convert_single_unstructured_params_to_proto(config)
    config_type = config.pop("type", "default")
    if config_type == "default":
        proto = ImagesSingleDataInfo(
            single_data_file_info=ImagesSingleDataFileInfo(
                file_name=config["file_name"]
            ),
            single_params=unstructured_params,
        )
    else:
        raise ValueError(f"Unsupported config type: {config_type}")
    if "load_path" in config and config["load_path"] is not None:
        proto.load_path = config["load_path"]
    return proto


def convert_images_data_info_to_proto(config: dict) -> ImagesDataInfo:
    """Convert config to proto message for images data."""
    config_type = config.get("type", "default")
    if config_type == "default":
        ref_config = copy.deepcopy(config)
        ref_config["file_name"] = config["ref_path"]
        eval_config = copy.deepcopy(config)
        eval_config["file_name"] = config["eval_path"]
        eval_data_info = convert_single_images_data_info_to_proto(eval_config)
        ref_data_info = convert_single_images_data_info_to_proto(ref_config)
    elif config_type == "split":
        eval_data_info = convert_single_images_data_info_to_proto(
            config["eval_data_info"]
        )
        ref_data_info = convert_single_images_data_info_to_proto(
            config["ref_data_info"]
        )
    else:
        raise ValueError(f"Unsupported config type: {config['type']}")
    return ImagesDataInfo(ref_data_info=ref_data_info, eval_data_info=eval_data_info)


def convert_images_config_to_proto(config: dict) -> ImagesCLIConfig:
    """Convert config to images proto."""
    # pop to remove from original config dict
    data_info = convert_images_data_info_to_proto(config.pop("data_info"))
    proto = ImagesCLIConfig(data_info=data_info)
    config_names = [field.name for field in ImagesCLIConfig.DESCRIPTOR.fields]
    for name in config_names:
        if name in config and config[name] is not None:
            # pop to remove from original config dict
            setattr(proto, name, json.dumps(config.pop(name)))
    return proto


def _update_key_names(config: dict) -> dict:
    """Update key names in config for backwards compatibility."""
    key_names = [
        ("test_config", "tests_config"),
        ("subset_profiling_config", "subset_profiling_info"),
    ]
    if "workspace_name" in config:
        config.pop("workspace_name")
    for old_name, new_name in key_names:
        if old_name in config:
            if new_name in config:
                raise ValueError(
                    f"Both {old_name} and {new_name} cannot be present in the config."
                )
            config[new_name] = config.pop(old_name)
    return config


def convert_config_to_proto(_config: dict, data_type: "DataType.V") -> TypedCLIConfig:
    """Convert a dictionary config to proto."""
    config = deepcopy(_config)
    config = _update_key_names(config)
    try:
        if data_type == DataType.TABULAR:
            tabular_config = convert_tabular_config_to_proto(config)
            proto = TypedCLIConfig(tabular_config=tabular_config)
        elif data_type == DataType.NLP:
            nlp_config = convert_nlp_config_to_proto(config)
            proto = TypedCLIConfig(nlp_config=nlp_config)
        elif data_type == DataType.IMAGES:
            images_config = convert_images_config_to_proto(config)
            proto = TypedCLIConfig(images_config=images_config)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    except KeyError:
        raise ValueError(f"Invalid config: {config}")

    for name in config:
        if name not in config or config[name] is None:
            continue
        if name == "tests_config":
            setattr(proto, name, json.dumps(config[name]))
        else:
            try:
                setattr(proto, name, config[name])
            except AttributeError:
                raise ValueError(
                    f"Config parsing fails on attribute '{name}'. "
                    "Make sure the data type aligns with the data provided. "
                    "Please specify data_type = 'tabular', 'nlp', or 'images'. "
                )
    return proto


def convert_tabular_incremental_config_to_proto(
    config: dict,
) -> TabularIncrementalConfig:
    """Convert a dictionary incremental config to tabular incremental proto."""
    try:
        if "eval_data_info" in config:
            eval_data_info = convert_single_tabular_data_info_to_proto(
                config["eval_data_info"]
            )
            proto = TabularIncrementalConfig(eval_data_info=eval_data_info)
        elif "eval_path" in config:
            data_file_info = TabularSingleDataFileInfo(file_name=config["eval_path"])
            tabular_params = TabularSingleDataInfoParams(
                timestamp_col=config["timestamp_col"]
            )
            if "eval_pred_path" in config:
                tabular_params.pred_path = config["eval_pred_path"]

            eval_data_info = TabularSingleDataInfo(
                single_data_file_info=data_file_info, single_params=tabular_params
            )
            proto = TabularIncrementalConfig(eval_data_info=eval_data_info)
        else:
            raise ValueError(f"Invalid incremental config: {config}")
    except KeyError:
        raise ValueError(f"Invalid incremental config: {config}")

    return proto


def convert_nlp_incremental_config_to_proto(config: dict) -> NLPIncrementalConfig:
    """Convert a dictionary incremental config to nlp incremental proto."""
    if "eval_data_info" in config:
        eval_data_info = convert_single_nlp_data_info_to_proto(config["eval_data_info"])
        proto = NLPIncrementalConfig(eval_data_info=eval_data_info)
    elif "eval_path" in config:
        # if config is in the old format, convert to use singledatainfo format
        data_file_info = NLPSingleDataFileInfo(file_name=config["eval_path"])
        eval_data_info = NLPSingleDataInfo(single_data_file_info=data_file_info)
        # NOTE: if eval_pred_path specified, create corresponding prediction_info
        # in eval_data_info
        if "eval_pred_path" in config and config["eval_pred_path"] is not None:
            eval_data_info.single_params.prediction_info.CopyFrom(
                SinglePredictionInfo(path=config["eval_pred_path"])
            )

        proto = NLPIncrementalConfig(eval_data_info=eval_data_info)
    else:
        raise ValueError(f"Invalid incremental config: {config}")
    return proto


def convert_images_incremental_config_to_proto(config: dict) -> ImagesIncrementalConfig:
    """Convert a dictionary incremental config to image incremental proto."""
    if "eval_data_info" in config:
        eval_data_info = convert_single_images_data_info_to_proto(
            config["eval_data_info"]
        )
        proto = ImagesIncrementalConfig(eval_data_info=eval_data_info)
    elif "eval_path" in config:
        # if config is in the old format, convert to use singledatainfo format
        data_file_info = ImagesSingleDataFileInfo(file_name=config["eval_path"])
        eval_data_info = ImagesSingleDataInfo(single_data_file_info=data_file_info)
        # NOTE: if eval_pred_path specified, create corresopnding prediction_info
        # in eval_data_info
        if "eval_pred_path" in config and config["eval_pred_path"] is not None:
            eval_data_info.single_params.prediction_info.CopyFrom(
                SinglePredictionInfo(path=config["eval_pred_path"])
            )

        proto = ImagesIncrementalConfig(eval_data_info=eval_data_info)
    else:
        raise ValueError(f"Invalid incremental config: {config}")
    return proto


def convert_incremental_config_to_proto(
    _config: dict, data_type: "DataType.V"
) -> TypedIncrementalConfig:
    """Convert a dictionary incremental config to proto."""
    config = deepcopy(_config)
    # TODO: implement other modalities too
    if data_type == DataType.TABULAR:
        tabular_config = convert_tabular_incremental_config_to_proto(config)
        proto = TypedIncrementalConfig(tabular_incremental_config=tabular_config)
    elif data_type == DataType.NLP:
        nlp_config = convert_nlp_incremental_config_to_proto(config)
        proto = TypedIncrementalConfig(nlp_incremental_config=nlp_config)
    elif data_type == DataType.IMAGES:
        images_config = convert_images_incremental_config_to_proto(config)
        proto = TypedIncrementalConfig(images_incremental_config=images_config)
    else:
        raise ValueError(f"Unknown data type: {data_type}")

    if "include_model" in config:
        setattr(proto, "include_model", config["include_model"])
    return proto


def proto_is_empty(proto_val: Any) -> bool:
    """Check if a proto is empty."""
    if isinstance(proto_val, Message):
        return proto_val == proto_val.__class__()
    return not bool(proto_val)


def all_protos_empty(proto_val: Any, fields: List[str]) -> bool:
    """Check if all fields of a proto are empty."""
    return all([proto_is_empty(getattr(proto_val, field)) for field in fields])


PROTO_T = TypeVar("PROTO_T", bound=Message)


def copy_with_mask(proto: PROTO_T, other: PROTO_T, fields_to_retain: List[str]) -> None:
    """Copy 'other' into 'proto' inplace without overwriting certain fields."""
    other_copy = copy.deepcopy(other)
    # First copy the fields that we want to retain
    # to the other proto
    for field in fields_to_retain:
        current_val = getattr(proto, field)
        if isinstance(current_val, Message):
            # If the field is a proto, we need to copy the fields of the proto
            # since there's an attribute error using setattr
            other_msg: Message = getattr(other_copy, field)
            other_msg.CopyFrom(current_val)
        else:
            setattr(other_copy, field, current_val)
    proto.CopyFrom(other_copy)
