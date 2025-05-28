import importlib.metadata


def is_package_installed(package_name: str) -> bool:
    try:
        importlib.metadata.version(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False

names = ["h7-file-finder", "h7-env-manager", "h7-logger-manager"]
for name in names:
    print(f"{name}: {'Available' if is_package_installed(name) else 'Not Available'}")
