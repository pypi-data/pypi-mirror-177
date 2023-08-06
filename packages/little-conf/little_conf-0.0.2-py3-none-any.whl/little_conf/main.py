import functools
import os
from typing import Any

import yaml
from deepmerge import always_merger
from pydantic import BaseSettings


def yaml_config_settings_source(
    settings: BaseSettings, base_path: str, env: str, ret_conf: dict
) -> dict[str, Any]:

    if base_path is not None:
        if ret_conf is None:
            ret_conf = {}
            base_conf = {}
            base_conf_file = os.path.join(base_path, 'base.yaml')
            if os.path.exists(base_conf_file):
                with open(base_conf_file, 'r') as fp:
                    base_conf = yaml.safe_load(fp) or {}

            ret = {}
            if env is not None:
                with open(os.path.join(base_path, f'{env}.yaml'), 'r') as fp:
                    ret = yaml.safe_load(fp) or {}

            ret_conf = always_merger.merge(base_conf, ret)

        return ret_conf
    else:
        return {}


class LittleSettings(BaseSettings):
    class Config:
        yaml_conf_path = os.environ.get('service_yaml_conf_path', 'conf')
        conf_env = os.environ.get('service_conf_env', 'local')
        env_prefix = os.environ.get('env_prefix', 'service_')

        _ret_conf = None

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):

            conf_env = os.environ.get('service_conf_env', cls.conf_env)
            yaml_conf_path = os.environ.get(
                'service_yaml_conf_path', cls.yaml_conf_path
            )

            return (
                init_settings,
                env_settings,
                functools.partial(
                    yaml_config_settings_source,
                    base_path=yaml_conf_path,
                    env=conf_env,
                    ret_conf=cls._ret_conf,
                ),
                file_secret_settings,
            )
