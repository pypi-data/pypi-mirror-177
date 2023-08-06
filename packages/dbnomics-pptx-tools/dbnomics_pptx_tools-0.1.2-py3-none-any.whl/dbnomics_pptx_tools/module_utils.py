import importlib.util
from pathlib import Path
from types import ModuleType

import daiquiri

logger = daiquiri.getLogger(__name__)


def load_python_module_from_path(module_path: Path, *, module_name: str) -> ModuleType:
    logger.debug("Loading Python module from path %r", str(module_path))
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ValueError(f"Could not build module spec from file location {str(module_path)}")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ValueError(f"Module spec built from file location {str(module_path)} has no loader")
    spec.loader.exec_module(module)
    return module
