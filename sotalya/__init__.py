submodules = [
        "pycli",
        "tucuxi",
    ]

def __getattr__(name):
        if name in submodules:
            return _importlib.import_module(f'sotalya.{name}')
        else:
            try:
                return globals()[name]
            except KeyError:
                raise AttributeError(
                    f"Module 'sotalya' has no attribute '{name}'"
                )