import logging
import pkgutil

# This will recursivly load all modules in this package
# So all we have to do is importing or loading "summed.analysis" and it will load all child modules, which include the Languge components

__all__ = []

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    logging.info(f"Loaded module: {module_name}")
    globals()[module_name] = _module
