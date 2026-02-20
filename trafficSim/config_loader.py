import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ConfigLoader:
    @staticmethod
    def load_yaml(file_path: str | Path) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        config_dir = Path(__file__).parent / 'config'
        return ConfigLoader.load_yaml(config_dir / 'default.yaml')

    @staticmethod
    def get_vehicles_config() -> Dict[str, Any]:
        config_dir = Path(__file__).parent / 'config'
        return ConfigLoader.load_yaml(config_dir / 'vehicles.yaml')

    @staticmethod
    def parse_color(color_list: List[int]) -> Tuple[int, int, int]:
        if len(color_list) != 3:
            raise ValueError(f"Color must have 3 elements, got {len(color_list)}")
        return (int(color_list[0]), int(color_list[1]), int(color_list[2]))
