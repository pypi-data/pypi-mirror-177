# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archimedes',
 'archimedes.data',
 'archimedes.data.api',
 'archimedes.testdata',
 'archimedes.utils',
 'archimedes.utils.split']

package_data = \
{'': ['*'], 'archimedes.testdata': ['datasets/*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0',
 'iteration-utilities>=0.11.0,<0.12.0',
 'msal-extensions>=1.0.0,<2.0.0',
 'msal>=1.10.0,<2.0.0',
 'pandas>=1.0.5',
 'requests>=2.27.0',
 'retry>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'archimedes-python-client',
    'version': '4.10.2',
    'description': 'The Python library for Archimedes',
    'long_description': '# archimedes\nThis is the Python library for Archimedes.\n\n## Installation\nMake sure you are running Python 3.8 or later.\n\nIt can be added to existing projects like so:\n```shell\npoetry add archimedes-python-client\n```\n\nIt can also be installed with pip:\n```shell\npip install archimedes-python-client\n```\n\nIt is recommended to use [arcl](https://github.com/OptimeeringAS/archimedes-cli) to generate new projects. The \ngenerated projects will install `archimedes-python-client` as a part of the project. It will also include the required\n`archimedes.toml`.\n\n## Development\nFormatting with [black](https://pypi.org/project/black/).\n\n## Configuration\n\nCertain behaviors of the client can be configured by using environment variables. \n\n| Configuration          | Description                               |\n|------------------------|-------------------------------------------|\n| ARCHIMEDES_ENVIRONMENT | The API to use (dev/prod). Default: prod. |\n| ARCHIMEDES_API_TIMEOUT | The request timeout for the API calls     |\n\nThe dev version has been deployed to \n[https://api-dev.fabapps.io/](http://api-dev.fabapps.io/) and the prod version is at \n[https://api.fabapps.io/](http://api.fabapps.io/).\n\nFor authentication-related environment variables, see below.\n\n## Authentication\n\nThe following 3 different types of authentication methods are supported:\n\n### local (default)\n\nThis uses your authentication credentials from arcl login (`arcl auth login optimeering`) and is implemented in the \nclass `ArchimedesLocalAuth`. This should only be used when running arcl locally.\n\n### confidential\n\nThis should be used when you want to allow a background application to have access to the API. This is suitable for \nuse-cases when the backend of one app needs full access to the API. To use it, set the environment variable \n`USE_APP_AUTHENTICATION`. In addition, an Azure AD B2C app needs to be created to represent this app (find the \ninstructions on how to do that on an app which is deployed this way \nhttps://github.com/OptimeeringAS/predictor-dashboard#api-access-setup) and the following additional environment \nvariables need to be set:\n\n| Configuration                  | Value                                                                                           |\n|--------------------------------|-------------------------------------------------------------------------------------------------|\n| AZURE_AD_TENANT_ID             | The value should be the **Directory (tenant) ID** of the authentication app.                    |\n| AZURE_AD_APP_ID                | The value should be the **Application (client) ID** of the authentication app.                  |\n| AZURE_AD_APP_CLIENT_CREDENTIAL | The value should be a client secret generated under **Certificates & secrets** in the Azure AD. |\n\n### web (public client)\n\nThis should be used when you want to allow users to login to public client applications (desktop app, mobile app or a \nweb app). The users will be asked to log in to the Archimedes API and allow your application to access the data the \nusers have access to. To use it, set the environment variable `USE_APP_AUTHENTICATION`. In addition, an Azure AD B2C \napp needs to be created to represent this app. The instructions for this are similar to the one used for [Azure AD app\nfor archimedes-cli](https://github.com/OptimeeringAS/archimedes-api#create-an-application-for-the-cli).\n\nOnce that is done, one of the following ways can be used to get the token:\n\n#### For a python cli app\n\n```python\nfrom archimedes.auth import ArchimedesPublicClientAuth\n\nAZURE_AD_TENANT_ID = "" # The value should be the **Directory (tenant) ID** of the public client app\nAZURE_AD_APP_ID = "" # The value should be the **Application (client) ID** of the public client app\nAZURE_APP_ID_AUTHORITY = "https://login.microsoftonline.com/common"\n\narchimedes_auth_app = ArchimedesPublicClientAuth(AZURE_AD_APP_ID, AZURE_APP_ID_AUTHORITY).app\n```\n\nAfter that, the `archimedes_auth_app` is an instance of `msal.PublicClientApplication` which can then be used to\nimplement the public client flow to get the token.\n\nOnce the token is retrieved, it can be used as such:\n\n```python\nimport archimedes\n\naccess_token = "" # See above on how to get it\n\narchimedes.get("NP/AreaPrices", "NO1", start="2022-02-24", end="2022-02-25", access_token=access_token)\n```\n\n#### For an SPA web app\n\nSee [msal.js](https://github.com/AzureAD/microsoft-authentication-library-for-js).\n\n## Publishing releases to pypi\n\nA new release can be made by \n[creating a release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) \nusing the GitHub web interface.\n\nWhen the release it created, as long as the tag naming convention is followed, it is automatically built and published \nto pypi by GitHub Actions, which is configured in the [.github/workflows](../.github/workflows) in this repo. Please refer \nto the following instructions when making releases:\n\n* Make sure that [pyproject.toml](pyproject.toml) is updated with a new version. We use \n[semantic versioning](https://semver.org/). Make sure the version hasn\'t already been published to \n[pypi](https://pypi.org/project/archimedes-python-client/#history). \n* Go to the Releases page of the project\n* Click the `Create a new release` button\n* Click on `Choose a tag` and in the input field, enter `release/client/v{VERSION_NUMBER_FROM_pyproject.toml}`, for e.g. \n`release/client/v1.2.3`. This tag name should NOT already exist, so it will NOT appear in the dropdown menu which appears as \nyou enter text. You need to click on `Create new tag release/client/v{VERSION_NUMBER_FROM_pyproject.toml} on publish` to create \nthe tag.\n* In the release title, write `v{VERSION_NUMBER_FROM_pyproject.toml}`, for e.g. `v1.2.3`.\n* In Release Notes, ideally, we should write the titles of all the Shortcut stories and link to them.\n* Click on the `Publish Release` button.\n* Then, check that the release pipeline is running by navigating to the Actions tab and wait for it to complete \nsuccessfully.\n* Verify the release is [published to pypi](https://pypi.org/project/archimedes-python-client/#history).\n* If there were no errors, a new `archimedes-python-client` version should be released.\n',
    'author': 'Optimeering AS',
    'author_email': 'dev@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
