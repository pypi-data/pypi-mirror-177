#!bash

echo "Starting up emulators for running tests"


# Install the package into local .venv and make it editable. Useful for developent.
echo "Install summed package into local venv as --editable"
pip install --editable ..

# Currently, the VS code plugin does not support relative paths, and hardcoding full paths is not very portable
# See e.g.: https://github.com/Azure/Azurite/issues/391

# Make sure to install Azurite emulator first
# npm install -g azurite
echo "Starting up Azurite emulator in project workspace folder"
azurite --silent --location ../.azurite --debug ../.azurite/debug.log


