import base64
import binascii
import hashlib
import logging
import mimetypes
import os
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Union

import requests

# Dependency:
# Azure Blob storage
from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    ContentSettings,
    ResourceTypes,
    AccountSasPermissions,
    generate_account_sas,
)
from pydantic import BaseModel

# Dependency:
# requests lib + extension: load file:// urls (e.g. to upload local files)
from requests_file import FileAdapter

from summed.data import Document, DocumentSource, FileInfo, GlossaryContainer
from summed.detector import Detector
from summed.summed_platform import SumMedPlatform
from summed.utils import create_thumbnail_from_url


class ISpace(ABC):
    """
    A "Space" is a abstraction for storing files before extraction/analysis.
    Current implementation uses Azure Blob Storage.

    Args:
        ABC (_type_): abstract base class
    """

    @abstractmethod
    def list_files(self) -> List[FileInfo]:
        pass

    @abstractmethod
    def upload(
        self, source: Union[DocumentSource, Path, str], overwrite: bool = False
    ) -> FileInfo:
        pass

    @abstractmethod
    def download(self, filename: str) -> bytes:
        pass

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def delete_all_files(self) -> None:
        pass

    @abstractmethod
    def exists(self) -> bool:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    @abstractmethod
    def get_public_url(self, file_info: Union[FileInfo, str]) -> str:
        pass

    @abstractmethod
    def is_existfile(self, file_info: Union[FileInfo, str]) -> bool:
        pass

    @abstractmethod
    def save_document(self, document: Document, filename: str = None, thumbnail: bool = True) -> Document:
        pass

    @abstractmethod
    def load_document(self, document: Union[Document, FileInfo, str]) -> Document:
        pass

    @abstractmethod
    def is_document(self, file_info: Union[FileInfo, str]) -> bool:
        pass

    @abstractmethod
    def delete_document_files(
        self, document: Union[Document, FileInfo, str], source: bool = False, thumbnail: bool = True
    ) -> None:
        pass

    @abstractmethod
    def find_documents(self, query: str = "*", max: int = None) -> List[Document] or List[str]:
        pass

    @abstractmethod
    def save_glossary(self, glossary: GlossaryContainer) -> FileInfo:
        pass

    @abstractmethod
    def load_glossary(self, glossary: Union[GlossaryContainer, FileInfo, str]) -> GlossaryContainer:
        pass


class Space(BaseModel, ISpace):
    """
    Spaces are collections of (blob) files and other resources that are used for data storage and retrieval.
    The default implementation uses Azure Blob storage.

    """

    # Platform to access global configuration
    platform: SumMedPlatform
    name: Optional[str] = "default"
    description: Optional[str]

    
    def _get_filename_from_source(self, source: DocumentSource) -> str:
        # We have a filename already set ? Then just use this
        if source.filename:
            return source.filename

        # No filename? Try last segment from url
        if source.url:
            # remove query and anchor from url, remove trailing slash
            url = source.url.split("#")[0].split("?")[0].rstrip("/")

            # Use given content type, or try to guess from source document
            content_type = source.content_type or self._get_content_type_from_source(
                source
            )

            # If we can't find an existing file extension/suffix, use this
            default_suffix = (
                mimetypes.guess_extension(content_type) if content_type else ".html"
            )

            # we can use os.path to get the final component from the url
            basename = os.path.basename(url)

            if basename:
                # basename might look like "file.html" or "file" or "" (empty)
                # file.html => ('file', '.html')
                # "file" => ('file', '')
                # "" => ('','')
                parts = os.path.splitext(basename)

                # santize filename
                # "1 file-with-non alpha=numeric chars" => "1_file_with_non_alpha_numeric_chars"
                name = "".join([c if c.isalnum() else "_" for c in parts[0]])

                # split into filename and suffix/extension
                suffix = (
                    parts[1] if parts[1] else default_suffix
                )  # use existing suffix or default if none found
                return f"{name}{suffix}"

            else:  # basename is empty ?
                # create a new filename from url, try to guess the extension (if not set)
                hash = hashlib.md5(source.url.encode("utf-8")).hexdigest()
                return f"{binascii.hexlify(hash)[:10]}{default_suffix}"

    def _get_content_type_from_source(self, source: DocumentSource) -> str:
        """Tries to determine the content type form a DocumentSource.


        Args:
            source (DocumentSource): The

        Returns:
            str: _description_
        """
        # We have a content type already set ? Then just use this
        if source.content_type:
            return source.content_type

        # For http url sources, we assume the content type is text/html,
        # unless detect_content_type returns something else (e.g. application/pdf)
        if source.url and source.url.lower().startswith("http"):
            default_content_type = "text/html"
        else:
            default_content_type = "application/octet-stream"

        return Detector(self.platform).detect_content_type(
            source.url or source.filename, default_content_type
        )

    def __init__(self, platform: SumMedPlatform, **kwargs):
        """
        Initializes the space, e.g. validates config and makes sure the storage container is created and accessible
        """
        super().__init__(platform=platform, **kwargs)
        self.platform = platform

        try:
            # Platform will provide the Blob service client to us
            client = self.platform.get_azure_blob_service_client()

            # We need to make sure the container exists
            if not client.exists():
                client.create_container()
        except Exception as e:
            logging.error(f"Error initializing space: {e}")
            raise (e)

    def upload(
        self, source: Union[DocumentSource, Path, str], overwrite: bool = False
    ) -> FileInfo:
        """Upload a document to the space. Returns the file info if successful.

        Args:
            source (DocumentSource|Path|str): source document, e.g. via url, base64 encoded, or container/filename.

            overwrite (bool, optional): [description]. Defaults to False.

        Returns:
            FileInfo: Information about the uploaded file, e.g. to download it later.
        """
        last_modified = datetime.utcnow()
        ts = int(last_modified.timestamp())

        container_client: ContainerClient = (
            self.platform.get_azure_blob_service_client()
        )

        # For convenience, we can just pass a Path-like (with url=file://...)
        # or a url string directly.
        if isinstance(source, DocumentSource):
            pass
        if isinstance(source, Path):
            source = DocumentSource(url=source.as_uri())
        elif isinstance(source, str):
            source = DocumentSource(url=source)  # TODO make sure this is a valid URL ?
        assert isinstance(source, DocumentSource)

        blob_filename = self._get_filename_from_source(source)

        # If already exists and overwrite is False, generate a new filename instead
        if container_client.get_blob_client(blob_filename).exists():
            if not overwrite:
                name, extension = os.path.splitext(blob_filename)
                blob_filename = f"{name}_{ts}{extension}"

        # Create the blob from the DocumentSource
        blob_client: BlobClient = container_client.get_blob_client(blob_filename)

        upload_result = None

        try:
            # detect content type
            content_type = self._get_content_type_from_source(
                source
            )  # source.determine_content_type()

            if source.data:
                # Data should be base64 encoded
                try:
                    data = base64.b64decode(source.data, validate=True)
                except Exception as e:
                    raise ValueError(f"Invalid base64 encoded data: {e}")
                upload_result = blob_client.upload_blob(
                    data=data,
                    blob_type="BlockBlob",
                    content_settings=ContentSettings(content_type=content_type),
                    overwrite=True,
                )
            elif source.url:
                # (http or file) URL given: download the file into the storage container
                # We need to register the file adapter here to support http and file urls
                session = requests.Session()
                session.mount("file://", FileAdapter())

                # TODO support custom headers, auth etc...
                response = session.get(source.url)

                if not response.ok:
                    raise ValueError(
                        f"Could not download file from url: {response.status_code} - {response.text}"
                    )

                data = response.content
                session.close()
                # TODO see if we can determine content type and other metadata
                # from the response
                upload_result = blob_client.upload_blob(
                    data=data,
                    blob_type="BlockBlob",
                    content_settings=ContentSettings(content_type=content_type),
                    overwrite=True,
                )
            elif source.container and source.filename:
                # TODO container + filename: copy from another blob file / container
                raise NotImplementedError(
                    "upload from blob storage container: Not implemented yet"
                )
            else:
                raise ValueError(
                    "Invalid document source, require either data or url to upload"
                )
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            raise ValueError(e)

        size = len(upload_result)
        info = FileInfo(
            filename=blob_filename,
            size=size,
            last_modified=last_modified,
            source=source,
            content_type=content_type,
            metadata=upload_result,
        )

        return info

    def download(self, file_info: Union[FileInfo, str]) -> bytes:
        """Download a file from the space.

        Args:
            file_info (FileInfo or str): file info of the file to download,
            or string with filename, as filenames are unique within a space.

        Returns:
            bytes: file data
        """
        filename = (
            file_info.filename if isinstance(file_info, FileInfo) else str(file_info)
        )

        container_client: ContainerClient = (
            self.platform.get_azure_blob_service_client()
        )

        blob_client = container_client.get_blob_client(filename)
        if not blob_client.exists():
            raise ValueError(f"File does not exist in blob container: {filename}")

        try:
            result = blob_client.download_blob().readall()
        except Exception as e:
            raise Exception(f"Error downloading file from blob storage: {e}")

        return result

    def list_files(self) -> List[FileInfo]:
        """List all the files in the space.

        Returns:
            List[FileInfo]: list of all the files in the space
        """
        container_client = self.platform.get_azure_blob_service_client()
        result = []

        for blob_props in container_client.list_blobs():
            # create our fileinfo object from blob properties
            f = FileInfo(filename=blob_props.name)
            # TODO add other properties

            result.append(f)

        return result

    def delete_file(self, file: Union[FileInfo, str]) -> bool:
        """Delete a file from the space.

        Args:
            filename (str): filename of the file to delete
        """
        container_client = self.platform.get_azure_blob_service_client()

        if isinstance(file, FileInfo):
            filename = file.filename
        else:
            filename = str(file)

        try:
            container_client.get_blob_client(filename).delete_blob()
        except Exception as e:
            logging.error(f"Error deleting file: {e}")
            return False

        return True

    def delete_all_files(self) -> bool:
        """Delete all files in the space.

        Returns:
            bool: True if successful, False indicates a problem with deletion
        """
        container_client = self.platform.get_azure_blob_service_client()
        if not container_client.exists():
            logging.warning(f"Blob container does not exist: {self.container_name}")
            return False

        blob_name_list = list(b.name for b in container_client.list_blobs())

        # Delete blobs
        if len(blob_name_list) > 0:
            try:
                # Fixme: didn't work for me in 12.9.0 -
                # client.delete_blobs(blob_name_list)
                for filename in blob_name_list:
                    container_client.delete_blob(filename)

            except Exception as e:
                logging.error(f"Error deleting files: {e}")
                return False
        else:
            logging.info(f"No files to delete")

        return True

    def exists(self) -> bool:
        client = self.platform.get_azure_blob_service_client()
        return client and client.exists()

    def delete(self) -> None:
        """Deletes the space and all its files - use with caution, removes the storage container"""

        if self.exists():
            self.delete_all_files()
            container_client = self.platform.get_azure_blob_service_client()
            container_client.delete_container()

    def get_public_url(self, file_info: Union[FileInfo, str]) -> str:
        """Get the public url for a file from Azure Blob Storage.
        
        Args:
            file_info (FileInfo or str): file info of the file to get the public url for.
            
            Returns:
                str: public url for the file.
        """
        filename = (
            file_info.filename if isinstance(file_info, FileInfo) else str(file_info)
        )

        container_client: ContainerClient = (
            self.platform.get_azure_blob_service_client()
        )

        blob_client = container_client.get_blob_client(filename)
        if not blob_client.exists():
            raise ValueError(f"File does not exist in blob container: {filename}")

        sas_token = generate_account_sas(
            container_client.account_name,
            account_key=container_client.credential.account_key,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        return blob_client.url + "?" + sas_token

    def is_existfile(self, file_info: Union[FileInfo, str]) -> bool:
        """Check if a file exists in the space.
            
        Args:
            file_info (FileInfo or str): file info of the file to check.
    
        Returns:
            bool: True if file exists, False otherwise.
        """
        filename = (
            file_info.filename if isinstance(file_info, FileInfo) else str(file_info)
        )
    
        container_client: ContainerClient = (
            self.platform.get_azure_blob_service_client()
        )
    
        try:
            blob_client = container_client.get_blob_client(filename)
        except Exception as e:
            logging.error(f"Error getting file from blob storage: {e}")
            return False
        
        return blob_client.exists()

    def save_document(self, document: Document, filename: str = None, thumbnail: bool = True) -> Document:
        """Save a document to the file in the space (also can try to save a thumbnail of the document source_file).

        Args:
            document (Document): the document to save.

            filename (str, optional): the name of the file where the document is to be saved. If omitted,
            will be generated from the document.source_file.filename.

            thumbnail (bool, optional): if True, will try to save a thumbnail of the document source_file too.
            Defaults to True.

        Returns:
            Document: the saved document.
        """
        if filename:
            filename = filename.strip().replace(" ", "_")
        else:
            filename = document.source_file.filename

        # make a HASH-string for the filename
        # if the field document.source_file.metadata['content_md5'] is set, take it as HASH
        if document.source_file.metadata and 'content_md5' in document.source_file.metadata:
            HASH = document.source_file.metadata['content_md5'].hex()
        else:
            # if sorce_file is exist, generate a HASH from it by md5, otherwise take a zero HASH
            if self.is_existfile(document.source_file):
                HASH = hashlib.md5(self.get_file(document.source_file)).hexdigest()
            else:
                HASH = '00000000000000000000000000000000'
                # set 'thumbnail' to False, because the source_file is not exist
                thumbnail = False

        # adding "SumMed_Document" marker and document version marker (HASH) to filename
        filename = filename + "_SumMed_Document_" + HASH

        if thumbnail:
            # {save thumbnail begin
            thumbnail_filename = filename + "_thumbnail_.jpg"
            # if thumbnail of source_file already exists, we take it from the space, because it's much faster
            if self.is_existfile(thumbnail_filename):
                b_thumbnail = self.download(thumbnail_filename)
            else:
                try:
                    # try to create the thumbnail  (!significant time required!)
                    # TODO: here we can set the size of the thumbnail
                    b_thumbnail = create_thumbnail_from_url(self.get_public_url(document.source_file))
                    if not b_thumbnail:
                        raise ValueError("Thumbnail is empty")
                except Exception as e:
                    logging.warning(f"Failed to create thumbnail: {e}")
                    thumbnail = False
            if thumbnail:
                document_thumbnail = DocumentSource(
                    filename=thumbnail_filename,
                    data=base64.b64encode(b_thumbnail),
                    content_type="image/jpeg",
                )
                document.thumbnail_file = self.upload(document_thumbnail, overwrite=True)
            # }save thumbnail end

        # {save document in json format begin
        document_filename = filename + ".json"
        
        # pre-saving the document to record information about the saved file inside the document
        data = document.json()
        document_json = DocumentSource(
            filename=document_filename,
            data=base64.b64encode(data.encode("utf-8")),
            content_type="application/json",
        )
        document.document_file = self.upload(document_json, overwrite=True)
        
        # final saving of the document
        data = document.json()
        document_json.data = base64.b64encode(data.encode("utf-8"))
        self.upload(document_json, overwrite=True)
        # }save document in json format end

        return document

    def load_document(self, document: Union[Document, FileInfo, str]) -> Document:
        """Load a document from the space.
    
            Args:
                document (Document or FileInfo or str): the document to load.
    
            Returns:
                Document: the loaded document.
            """
        if isinstance(document, Document):
            document = document.document_file
        elif isinstance(document, str):
            document = FileInfo(filename=document)
    
        if not self.is_existfile(document):
            raise ValueError(f"File does not exist in the space: {document}")
    
        document_json = self.download(document)
        try:
            new_document = Document.parse_raw(document_json)
            # restore metadata['content_md5'] field from hex to bytearray in document_file, thumbnail_file and source_file
            for file in [new_document.document_file, new_document.thumbnail_file, new_document.source_file]:
                if 'content_md5' in file.metadata:
                    file.metadata['content_md5'] = bytearray.fromhex(file.metadata['content_md5'])
            return new_document
        except Exception as e:
            logging.error(f"Error parsing document: {e}")

    def is_document(self, file_info: Union[FileInfo, str]) -> bool:
        """Determine by filename if a file is a SumMed document.

        Returns:
            bool: True if a file is a SumMed document, False otherwise.
        """
        filename = file_info.filename if isinstance(file_info, FileInfo) else str(file_info)
        if ("_SumMed_Document_" in filename) and (filename.endswith(".json")):
            return True
        else:
            return False

    def delete_document_files(
        self, document: Union[Document, FileInfo, str], source: bool = False, thumbnail: bool = True
    ) -> bool:
        """Delete document files from the space.
    
            Args:
                document (Document or FileInfo or str): the document whose files are to be deleted.

                source (bool, optional): if True, will delete the source_file of the document. Defaults to False.

                thumbnail (bool, optional): if True, will delete the thumbnail_file of the document. Defaults to True.
     
            Returns:
                bool: True if document json-file is realy had been deleted, False otherwise.
            """
        if isinstance(document, Document):
            document_filename = document.document_file.filename
            # delete source_file if needed
            if source and document.source_file:
                self.delete_file(document.source_file)
                thumbnail = True
            # delete thumbnail_file if needed
            if thumbnail and document.thumbnail_file:
                self.delete_file(document.thumbnail_file)
        else:
            # in this case, thumbnail file and source file will not be deleted
            if isinstance(document, FileInfo):
                document_filename = document.filename
            else:
                document_filename = document
            if not self.is_document(document_filename):
                logging.warning(f"File is not a SumMed document: {document_filename}")
                return False
        
        return self.delete_file(document_filename)
       
    def find_documents(self, query: str = "*", max: int = None) -> List[Document] or List[str]:
        """Find documents in the space.

        Args:
            query (str, optional): a query string. Defaults to "*".
            max (int, optional): the maximum number of documents to return. Defaults to None.

        Returns:
            List[Document]: a list of documents, if query is "*".
            List[str]: a list of document filenames, if query is "filename".
        """
        result = []
        for file in self.list_files():
            if self.is_document(file):
                # TODO: implement query
                if query == "*":
                    # Try to load a document
                    item = self.load_document(file)
                elif query == "filename":
                    # Return only document filenames
                    item = file.filename
                if item:
                    result.append(item)
                    if max:
                        if len(result) >= max:
                            break
        return result

    def save_glossary(self, glossary: GlossaryContainer) -> FileInfo:
        """Save glossary to space

        Args:
            glossary (GlossaryContainer): glossary
        """
        data = glossary.json()
        glossary_json = DocumentSource(
            filename=glossary.filename,
            data=base64.b64encode(data.encode("utf-8")),
            content_type="application/json",
        )
        return self.upload(glossary_json, overwrite=True)

    def load_glossary(self, glossary: Union[GlossaryContainer, FileInfo, str]) -> GlossaryContainer:
        """Load glossary from space

        Args:
            glossary (GlossaryContainer): glossary

        Returns:
            GlossaryContainer: loaded glossary
        """
        if isinstance(glossary, GlossaryContainer) or isinstance(glossary, FileInfo):
            glossary = glossary.filename
        
        glossary_json = self.download(glossary)
        try:
            glossary = GlossaryContainer.parse_raw(glossary_json)
        except Exception as e:
            logging.error(f"Error parsing glossary: {e}")
            raise e

        return glossary


    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
