import logging
import logging.config
import mimetypes
import base64
import pathlib
from file_repository_api_client.util import SupportedFiles
from pathlib import Path
from typing import Any

import requests


class UnSupportedFileException(Exception):
    pass


class FileApi(object):
    """
    Store and Retrieve files store in a file repository api.
    used with a custom based aws file repository api.

    :param api_url: the custom api end point
    :type api_url: str
    """

    def __init__(self, api_url: str):
        self.api_url = api_url

    def store_file(self, absolute_file_path: str, project_guid=None) -> dict:
        """
        Stole file name
        :param absolute_file_path:
        :param project_guid:
        :return:
        """
        supported_files_instance = SupportedFiles()
        file_name = Path(absolute_file_path).name
        file_ext = Path(file_name).suffix.replace('.', '').lower()

        # is supported extension
        if not supported_files_instance.is_supported(file_ext):
            raise UnSupportedFileException("UnSupportedFileException...see list of supported files")

        # is binary file
        if supported_files_instance.is_binary_file(file_ext):
            is_binary_file = True
            with open(absolute_file_path, mode="rb") as fr:
                file_content = base64.b64encode(fr.read())

        else:
            is_binary_file = False
            with open(absolute_file_path, mode="r") as fr:
                file_content = fr.read()

        file_name = Path(absolute_file_path).name
        file_mime_type = supported_files_instance.get_mime_type(file_ext)['mime-type']

        results_dict: dict = {}
        headers = {"name": file_name, "Content-Type": file_mime_type, "project_guid": project_guid,
                   'is_binary_file': str(is_binary_file)}

        try:
            response: Any = requests.post(self.api_url, headers=headers, data=file_content)
            response.raise_for_status()
            results_dict = response.json()
        except requests.exceptions.HTTPError as err:
            logging.exception(
                f"Exception occurred whilst attempting to store file using api:{self.api_url}"
            )
            raise Exception(err) from err

        return results_dict

    def retrieve_file(self, guid: str) -> dict:
        """
        Retrieve file name
        :param guid:
        :return:
        """

        results_dict: dict = {}
        headers = {"Accept": "application/json"}

        formatted_url: str = f"{self.api_url}/{guid}"
        try:
            response: Any = requests.get(formatted_url, headers=headers)
            response.raise_for_status()
            results_dict = response.json()
        except requests.exceptions.HTTPError as err:
            logging.exception(
                f"Exception occurred whilst attempting to retrieve file using api:{formatted_url}"
            )
            raise Exception(err) from err

        return results_dict
