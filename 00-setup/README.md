# Setup

We can start setting up the environment for the following labs.

## Prerequisites

- [Python 3.13 or later version](https://www.python.org/downloads) installed. Open a terminal (**Command Prompt** on PC, **Terminal** on Mac) and check your version:

    ```sh
    python --version
    ```

- Install the python requirements (we'll need them in the following chapters):

    ```sh
    pip install -r requirements.txt
    ```

- [VS Code](https://code.visualstudio.com/) installed with the [Jupyter notebook extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) enabled.
  - Open VS Code, go to “Extensions” (Ctrl+Shift+X or Cmd+Shift+X).
  - Search for 'Jupyter' and click Install.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed. Check installation:

    ```sh
    az --version
    ```

- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools) installed.
- [Sign in to Azure with Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively).
  - To sign in interactively, use the az login command:

    ```sh
    az login
    ```

  - Beginning with Azure CLI version 2.61.0, if you have access to multiple subscriptions, you're prompted to select an Azure subscription. Select the "xyz" subscription for this Hackathon.

### 🚀 Get started

Proceed by opening the [Jupyter notebook](./setup.ipynb), and follow the steps provided.
