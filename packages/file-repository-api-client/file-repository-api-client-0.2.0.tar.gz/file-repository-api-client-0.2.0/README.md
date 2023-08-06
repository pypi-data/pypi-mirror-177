# file-repository-api-client
A small api client library used with a file repository Api.

### Installation
```
pip install file-repository-api-client
```

### Save file to File Repository API

```Python
from file_repository_api_client import FileApi

url: str = "https://file.example.api.com/files"
file: str = "~/my_file.txt"

api = FileApi(url)

resp: dict = api.store_file(file)

#get file guid
print(resp["results"]["guid"])
```
### Retrieve file from File Repository API
Send file to repository API for storage:

```Python
import requests
from file_repository_api_client import FileApi


url: str = "https://file.example.api.com/files"
guid: str = "bd353120-e0ed-4400-83f1-9eba80db2809"

api = FileApi(url)

resp: dict = api.retrieve_file(guid)

#specify local file name
file_name: str = f"{resp['results']['name']}"

try:
    response = requests.get(resp["results"]["presigned_url"], allow_redirects=True)
    response.raise_for_status()
    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))
except requests.exceptions.HTTPError as err:
    print(f"Exception occurred whilst attempting download file from api, error: {err}")

```