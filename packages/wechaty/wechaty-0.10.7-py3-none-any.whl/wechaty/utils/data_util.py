"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
import json

import os
from typing import (
    Any,
)
from collections import UserDict
import pickle


def save_pickle_data(obj: object, path: str):
    """save pickle data

    Args:
        obj (object): the pickled data
        path (str): the path of pickle data
    """
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle_data(path: str) -> object:
    """load pickle data from path

    Args:
        path (str): the path of pickle data

    Returns:
        object: the final data
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


class WechatySetting(UserDict):
    """save setting into file when changed"""
    def __init__(
        self,
        setting_file: str
    ):
        """init wechaty setting"""
        super().__init__()
        self.setting_file = setting_file
        self._init_setting()
        self.data = self.read_setting()

    def _init_setting(self):
        """init setting file"""
        # 1. init setting dir
        setting_dir = os.path.dirname(self.setting_file).strip()
        if setting_dir:
            os.makedirs(setting_dir, exist_ok=True)

        # 2. init setting file
        if not os.path.exists(self.setting_file):
            self.save_setting({})

        # 3. check the content of setting file
        else:
            with open(self.setting_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                self.save_setting({})
        
    def read_setting(self) -> dict:
        """read the setting from file

        Returns:
            dict: the data of setting file
        """
        with open(self.setting_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
    def save_setting(self, value: dict) -> None:
        """update the plugin setting"""
        with open(self.setting_file, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False)
        self.data = value

    def __setitem__(self, key: str, value: Any) -> None:
        """triggered by `data[key] = value`"""
        self.data[key] = value
        self.save_setting(self.data)

    def to_dict(self) -> dict:
        """return the dict data"""
        return self.read_setting()


# class QCloudSetting(WechatySetting):
#     """Tencent Cloud Object Storaging"""
#     def __init__(self, setting_file: str):
#         super().__init__(setting_file)

#         from qcloud_cos import CosConfig
#         from qcloud_cos import CosS3Client
        
#         secret_id = config.get_environment_variable("q_secret_id")
#         secret_key = config.get_environment_variable("q_secret_key")
#         region = config.get_environment_variable("q_secret_region")
#         self.bucket_name = config.get_environment_variable("bucket_name")
#         self.bucket_path_prefix: str = config.get_environment_variable("bucket_prefix", "")

#         cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
#         self.client = CosS3Client(cos_config)
    
#     def read_setting(self) -> dict:
#         """read setting from q-cloud

#         Returns:
#             dict: the object of setting
#         """
#         remote_path = os.path.join(self.bucket_path_prefix, self.setting_file)   
#         self.client
