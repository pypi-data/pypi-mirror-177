## How to setup and run SumMed tests

We use ``pytest`` with plugins for testing (unittest, integration, acceptance/BDD).

In order to run tests locally, you'll need to setup the following:
1. Install Azurite (Azure Storage Emulator) for local testing: 
 https://docs.microsoft.com/en-us/azure/storage/blobs/use-azurite-to-run-automated-tests
   1. e.g. you can do a local install with `` npm install -g azurite ``
   2. Then run it e.g. `` azurite --silent --location ../.azurite --debug ../.azurite/debug.log ``


2.  Make sure to install our module into the current virtual environment for debugging:
``` pip install --editable .. ```

You can use the script ``start_emulators_for_testing.sh ``

