import json
import os
from pathlib import Path


class Config:
    def __init__(self, environment: str, *, base_file: str = 'settings.json', env_prefix: str = 'ENV_'):
        self.environment = environment
        if (self.environment is None) or (self.environment == ''):
            self.environment = os.getenv('ENVIRONMENT', 'dev')
        basefile = Path(base_file)
        parts = list(basefile.parts)
        filename = parts[-1].split('.')
        parts = parts[:-1]
        env_settings_file = Path(*parts, f'{filename[0]}.{environment}.{filename[1]}')
        def_settings_file = Path(*parts, f'{filename[0]}.{filename[1]}')
        secrets_file = Path(*parts, f'.secrets.{filename[1]}')
        self.settings = dict()
        # base settings: default file
        def_settings = self.load_settings(def_settings_file)
        if def_settings:
            self.settings.update(def_settings)

        env_settings = self.load_settings(env_settings_file)
        if env_settings:
            self.settings.update(env_settings)

        secrets = self.load_settings(secrets_file)
        if secrets:
            self.settings.update(secrets)

        # load settings from env variables starting with env_prefix
        for k, v in os.environ.items():
            if k.startswith(env_prefix):
                self.settings[k[len(env_prefix):]] = v

    def load_settings(self, filepath: Path):
        if not filepath.exists():
            return None

        try:
            print(f'Loading settings from {filepath}')
            with open(filepath) as f:
                if filepath.suffix == '.json':
                    return json.load(f)
                if filepath.suffix == '.yml':
                    import yaml
                    return yaml.load(f, Loader=yaml.FullLoader)
                if filepath.suffix == '.toml':
                    import toml
                    return toml.load(f)

        except Exception as e:
            print(f'Error loading settings from {filepath}: {e}')
            return None
