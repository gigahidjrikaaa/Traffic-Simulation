from typing import Dict, Any


class Configurable:
    """Base class for objects with configurable properties."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        """Initialize with configuration dict.

        Args:
            config: Dictionary of configuration overrides
        """
        if config is None:
            config = {}
        self.set_defaults()
        self.apply_config(config)

    def set_defaults(self) -> None:
        """Set default configuration values.

        Override in subclasses to define default values.
        """
        pass

    def apply_config(self, config: Dict[str, Any]) -> None:
        """Apply configuration dict with validation.

        Args:
            config: Dictionary of configuration values

        Raises:
            AttributeError: If config contains unknown keys
        """
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Unknown config option: {key}")
