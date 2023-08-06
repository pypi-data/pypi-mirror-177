from mlplatform_lib.api_client import ApiClient, RunMode
from mlplatform_lib.mllab.mllab_http_client import MllabHttpClient
from mlplatform_lib.hyperdata.hyperdata_http_client import HyperdataHttpClient
from mlplatform_lib.hyperdata.hyperdata_api import HyperdataApi
from mlplatform_lib.dataclass.model.model_dto import ModelDto
from mlplatform_lib.dataclass import (
    InsertTupleObject,
    TableColumnInfo,
)
import os
import pandas as pd
import sys
from typing import List, Optional


class MllabImageType:
    TENSORFLOW_V1 = "tf_v1.15.2"
    TENSORFLOW_V2 = "tf_v2.1.0"
    TORCH = "torch_v1.6.0"


if os.environ["image"] == MllabImageType.TENSORFLOW_V1 or os.environ["image"] == MllabImageType.TENSORFLOW_V2:
    import tensorflow as tf
elif os.environ["image"] == MllabImageType.TORCH:
    import torch


class MllabApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        if api_client.run_mode == RunMode.KUBERNETES:
            self.mllab_mlplatform_client = MllabHttpClient(mlplatform_addr=os.environ["mlplatformAddr"], api_client=api_client)
            self.mllab_hyperdata_client = HyperdataHttpClient(hd_addr=self.api_client.hyperdata_addr, api_client=self.api_client)
            self.mllab_hyperdata_api = HyperdataApi(api_client=self.api_client)
        self.experiment_id = self.api_client.experiment_id
        self.image = os.environ["image"]

    def get_model_list(self) -> Optional[List[ModelDto]]:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            return self.mllab_mlplatform_client.get_model_list(
                experiment_id=self.experiment_id
            )
        else:
            print("Current mode is local, Skip get_list_model.")
            return None

    def get_model(self, model_path: str = None):
        if self.api_client.run_mode == RunMode.KUBERNETES:
            if model_path is None:
                latest_model_dto = self.mllab_mlplatform_client.get_latest_model(
                    experiment_id=self.experiment_id
                )
                model_path = latest_model_dto.model_path

            if self.image == MllabImageType.TENSORFLOW_V1:
                return tf.compat.v2.saved_model.load(model_path + "/")
            elif self.image == MllabImageType.TENSORFLOW_V2:
                return tf.saved_model.load(model_path + "/")
            elif self.image == MllabImageType.TORCH:
                sys.path.append(model_path + "/")
                from network_class import Net

                net = Net()
                return net, torch.load(model_path + "/" + "model.pt")
        else:
            print("Current mode is local, Skip get_list_do.")
            return None

    def save_model(self, model, signatures=None) -> bool:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            export_dir = self.api_client.pvc_mount_path + "/model/model-" + self.api_client.train_id + "/1"
            if not os.path.isdir(export_dir):
                os.makedirs(export_dir)

            if self.image == MllabImageType.TENSORFLOW_V1:
                tf.saved_model.save(model, export_dir, signatures)
            elif self.image == MllabImageType.TENSORFLOW_V2:
                tf.saved_model.save(model, export_dir, signatures)
            elif self.image == MllabImageType.TORCH:
                torch.save(model.state_dict(), export_dir + "/model.pt", _use_new_zipfile_serialization=False)
                if os.path.isfile(self.api_client.pvc_mount_path + "/user_files/user_train.py"):
                    fin = open(self.api_client.pvc_mount_path + "/user_files/user_train.py", "r")
                    fout = open(export_dir + "/network_class.py", "w+")
                    for line in fin:
                        if line.strip().startswith("import pandas as pd"):
                            continue
                        elif line.strip().startswith("import os"):
                            continue
                        elif line.strip().startswith("from sklearn.model_selection import train_test_split"):
                            continue
                        elif line.strip().startswith(
                            "from sklearn.metrics import precision_recall_fscore_support"
                        ):
                            continue
                        elif line.strip().startswith("import hyper"):
                            continue
                        else:
                            fout.write(line)

            model_dto = self.mllab_mlplatform_client.get_model_by_id(
                experiment_id=self.experiment_id, train_id=self.api_client.train_id
            )
            model_dto.model_path = export_dir
            return self.mllab_mlplatform_client.update_model(
                experiment_id=self.experiment_id,
                train_id=self.api_client.train_id,
                dto=model_dto
            )
        else:
            print("Current mode is local, Skip get_list_do.")
            return None

    def get_do_list(self) -> dict:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            return self.mllab_hyperdata_client.get_do_simple_list()
        else:
            print("Current mode is local, Skip get_list_do.")
            return None

    def get_do(self, do_id: str, char_encoding="euc-kr") -> pd.DataFrame:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            file_name = do_id + ".csv"
            dir_name = self.api_client.pvc_mount_path + "/data"
            full_path = dir_name + "/" + file_name
            if os.path.exists(full_path):
                result = pd.read_csv(full_path, encoding=char_encoding)
                return result
           
            do_path = self.mllab_hyperdata_api.download_csv(
                do_id=do_id,
                data_rootpath=dir_name
            )

            if os.path.exists(do_path) :
                result = pd.read_csv(do_path, encoding=char_encoding)
            else :
                print("Fail")
                result = None
            return result
        else:
            print("Current mode is local, Skip get_do.")
            return None

    def get_do_meta(self, do_id: str) -> List[TableColumnInfo]:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            tableDescInfo = self.mllab_hyperdata_client.get_do_detail_info(
                do_id=do_id
            )
            return tableDescInfo.col_info_list
        else:
            print("Current mode is local, Skip get_do_meta.")
            return None

    def save_do(self, input_data: pd.DataFrame, do_id: str, is_truncated: str = False) -> bool:
        if self.api_client.run_mode == RunMode.KUBERNETES:
            print(self.api_client.inference_id)
            if self.api_client.inference_id is not None:
                file_dir = (
                    self.api_client.pvc_mount_path + "/inference/inference-" + self.api_client.inference_id
                )
                file_path = file_dir + "/inference-result.csv"
                if not os.path.isdir(file_dir):
                    os.mkdir(file_dir)
                input_data.to_csv(file_path, index=False, header=True)
            else:
                print("inference id is None")
                return False

            inference_dto = self.mllab_mlplatform_client.get_inference_by_id(
                experiment_id=self.experiment_id,
                inference_id=self.api_client.inference_id
            )
            inference_dto.inference_path = file_path
            self.mllab_mlplatform_client.update_inference(
                experiment_id=self.experiment_id, dto=inference_dto
            )

            insert_tuple_object = InsertTupleObject(
                isTruncated=is_truncated,
                targetColNames=input_data.columns.tolist(),
                tableData=input_data.values.tolist(),
            )
            res = self.mllab_hyperdata_client.insert_dataobject_tuple(
                dataobject_id=do_id, insert_tuple_objects=insert_tuple_object
            )
            if res.status_code == 200:
                return True
            else:
                return False
