#!/usr/bin/env python3
"""
PyPI Publishing Script for h7-file-finder

This script automates the process of building and publishing the h7-file-finder package to PyPI.
It handles creating distribution files, validating them, and uploading to PyPI.

Requirements:
- Python 3.7+
- build, twine packages (installed by this script if missing)
- PyPI account credentials

Usage:
    python publish_h7.py

The script will guide you through the process with prompts for PyPI credentials.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Package directory
PACKAGE_DIR = Path("C:/Users/RogerMori/projects/python_toolbox/h7-file-finder")


def check_dependencies():
    """Check and install required dependencies for publishing."""
    print("Checking and installing required dependencies...")

    dependencies = ["build", "twine"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} is already installed")
        except ImportError:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} installed successfully")


def clean_dist_directory():
    """Clean up any existing distribution files."""
    dist_dir = PACKAGE_DIR / "dist"
    if dist_dir.exists():
        print(f"Cleaning up existing distribution directory: {dist_dir}")
        shutil.rmtree(dist_dir)

    # Also clean up build directory if it exists
    build_dir = PACKAGE_DIR / "build"
    if build_dir.exists():
        print(f"Cleaning up existing build directory: {build_dir}")
        shutil.rmtree(build_dir)

    # Clean up egg-info directory if it exists
    for egg_info in PACKAGE_DIR.glob("*.egg-info"):
        print(f"Cleaning up {egg_info}")
        shutil.rmtree(egg_info)


def build_package():
    """Build source and wheel distributions."""
    print("/nBuilding package distributions...")

    # Change to the package directory
    os.chdir(PACKAGE_DIR)

    # Build the package
    subprocess.check_call([sys.executable, "-m", "build"])

    # Check if dist directory was created and contains files
    dist_dir = PACKAGE_DIR / "dist"
    if not dist_dir.exists() or not list(dist_dir.glob("*")):
        print("Error: Failed to build distribution files.")
        sys.exit(1)

    print("✓ Package built successfully!")
    print("/nDistribution files created:")
    for file in dist_dir.glob("*"):
        print(f"  - {file.name}")


def validate_package():
    """Validate the built distributions with twine check."""
    print("/nValidating distribution files...")

    # Change to the package directory
    os.chdir(PACKAGE_DIR)

    # Run twine check on the dist directory
    result = subprocess.run(
        [sys.executable, "-m", "twine", "check", "dist/*"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error: Package validation failed.")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    print("✓ Package validation successful!")
    print(result.stdout)


def upload_to_pypi():
    """Upload the package to PyPI."""
    print("/n=== UPLOADING TO PYPI ===")
    print("This step will upload your package to the main PyPI repository.")
    print("You will need your PyPI username and password.")

    # Prompt for confirmation
    confirm = input("/nAre you ready to upload to PyPI? (yes/no): ").lower()
    if confirm != "yes":
        print("Upload cancelled. You can upload manually later with:")
        print(f"  cd {PACKAGE_DIR} && python -m twine upload dist/*")
        return

    # Change to the package directory
    os.chdir(PACKAGE_DIR)

    # Upload to PyPI
    print("/nUploading to PyPI...")
    print("You will be prompted for your PyPI credentials.")

    try:
        subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])
        print("/n✓ Package successfully uploaded to PyPI!")
        print(
            "Your package should now be available at: https://pypi.org/project/h7-file-finder/"
        )
    except subprocess.CalledProcessError as e:
        print(f"/nError uploading to PyPI: {e}")
        print("/nIf you encountered authentication issues, you can:")
        print("1. Create a PyPI account at https://pypi.org/account/register/")
        print("2. Try uploading manually with:")
        print(f"   cd {PACKAGE_DIR} && python -m twine upload dist/*")


def create_pypirc_instructions():
    """Create instructions for setting up .pypirc file."""
    print("/n=== PYPI CREDENTIALS SETUP (OPTIONAL) ===")
    print("To avoid entering credentials each time, you can create a .pypirc file:")

    pypirc_content = """[distutils]
index-servers =
    pypi

[pypi]
username = your_username
password = your_password
"""

    print("/n1. Create a file at ~/.pypirc with the following content:")
    print("-" * 50)
    print(pypirc_content)
    print("-" * 50)
    print("2. Replace 'your_username' and 'your_password' with your PyPI credentials")
    print("3. Secure the file: chmod 600 ~/.pypirc")


def main():
    """Main function to run the publishing process."""
    print("=" * 60)
    print("publish_h7 PyPI Publishing Script")
    print("=" * 60)

    # Check if we're in the right directory structure
    if not PACKAGE_DIR.exists():
        print(f"Error: Package directory not found at {PACKAGE_DIR}")
        sys.exit(1)

    # Check for required dependencies
    check_dependencies()

    # Clean up any existing distribution files
    clean_dist_directory()

    # Build the package
    build_package()

    # Validate the package
    validate_package()

    # Upload to PyPI
    upload_to_pypi()

    # Provide instructions for .pypirc
    create_pypirc_instructions()

    print("/n" + "=" * 60)
    print("Publishing process completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
