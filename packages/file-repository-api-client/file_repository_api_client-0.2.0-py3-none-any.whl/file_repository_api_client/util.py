from xmlrpc.client import boolean


class SupportedFiles:
    # list of supported extensions
    supported_extensions: list = [
        'pdf', 'pdb', 'npy', 'txt', 'png', 'svg', 'ico', 'docx', 'zip', 'jpg', 'jpeg', 'gz', 'tar', 'bmp', 'json',
        'project', 'yaml'
    ]

    # supported binary mime types
    supported_binary_files: dict = {
        'pdf': {'ext': 'pdf', 'mime-type': 'application/pdf'},
        'npy': {"ext": "pdf", 'mime-type': 'application/octet-stream'},
        'png': {"ext": "png", 'mime-type': 'image/png'},
        'bmp': {"ext": "bmp", 'mime-type': 'image/x-ms-bmp'},
        'svg': {"ext": "svg", 'mime-type': 'image/svg+xml'},
        'ico': {"ext": "ico", 'mime-type': 'image/x-icon'},
        'docx': {"ext": "docx", 'mime-type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
        'zip': {"ext": "zip", 'mime-type': 'application/zip'},
        'jpg': {"ext": "jpg", 'mime-type': 'image/jpeg'},
        'jpeg': {"ext": "jpeg", 'mime-type': 'image/jpeg'},
        'gz': {"ext": "gz", 'mime-type': 'application/x-gzip'},
        'tar': {"ext": "tar", 'mime-type': 'application/x-gzip'},
    }

    # supported text mime types
    supported_text_files = {
        'yaml': {'ext': 'yaml', 'mime-type': 'text/plain'},
        'pdb': {"ext": "pdb", 'mime-type': 'text/plain'},
        'txt': {"ext": "text", 'mime-type': 'text/plain'},
        'json': {"ext": "json", 'mime-type': 'text/plain'},
        'project': {"ext": "project", 'mime-type': 'text/plain'},
    }

    def is_supported(self, extension: str) -> boolean:
        """
        Check if extension is supported
        :param extension:
        :return:
        """
        return extension.lower() in self.supported_extensions

    def is_binary_file(self, extension: str) -> boolean:
        """
        Check if file is binary
        :return:
        """
        return extension.lower() in self.supported_binary_files.keys()

    def is_text_file(self, extension: str) -> boolean:
        """
        Check if file is text
        :return:
        """
        return extension.lower() in self.supported_text_files.keys()

    def get_mime_type(self, extension: str) -> dict:
        """
        Get supported mime type
        :param extension:
        :return:
        """

        if self.is_binary_file(extension):
            return self.supported_binary_files.get(extension.lower())
        else:
            return self.supported_text_files.get(extension.lower())
