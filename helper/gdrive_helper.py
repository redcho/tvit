from helper.gdrive_auth_helper import *
from helper.bt_logging import get_logger
from googleapiclient.http import HttpRequest, MediaFileUpload
from typing import IO, Optional
from googleapiclient.http import MediaIoBaseDownload

NUM_RETRIES = 2


def _ensure_folders_exists(path: str) -> str:
    logger = get_logger(__name__)

    current_parent = "root"
    folders = path.split("/")
    depth = 0
    # First tries to enter directories
    for current_folder in folders:
        logger.debug("Looking for %s directory with %s parent", current_folder, current_parent)
        conditions = [
            "mimeType = 'application/vnd.google-apps.folder'",
            f"name='{current_folder}'",
            f"'{current_parent}' in parents",
        ]
        result = (
            service.files()
                .list(q=" and ".join(conditions), spaces="drive", fields="files(id, name)")
                .execute(num_retries=NUM_RETRIES)
        )
        files = result.get("files", [])
        if not files:
            logger.info("Not found %s directory", current_folder)
            # If the directory does not exist, break loops
            break
        depth += 1
        current_parent = files[0].get("id")

    # Check if there are directories to process
    if depth != len(folders):
        # Create missing directories
        for current_folder in folders[depth:]:
            file_metadata = {
                "name": current_folder,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [current_parent],
            }
            file = (
                service.files()
                    .create(body=file_metadata, fields="id")
                    .execute(num_retries=NUM_RETRIES)
            )
            logger.info("Created %s directory", current_folder)

            current_parent = file.get("id")
    # Return the ID of the last directory
    return current_parent


def upload_file(local_location: str, remote_location: str) -> str:
    """
    Uploads a file that is available locally to a Google Drive service.
    :param local_location: The path where the file is available.
    :param remote_location: The path where the file will be send
    :return: File ID
    :rtype: str
    """
    logger = get_logger(__name__)

    directory_path, _, file_name = remote_location.rpartition("/")
    if directory_path:
        parent = _ensure_folders_exists(directory_path)
    else:
        parent = "root"

    file_metadata = {"name": file_name, "parents": [parent]}
    media = MediaFileUpload(local_location)
    file = (
        service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute(num_retries=NUM_RETRIES)
    )
    logger.info("File %s uploaded to gdrive://%s.", local_location, remote_location)
    return file.get("id")


def get_media_request(file_id: str) -> HttpRequest:
    """
    Returns a get_media http request to a Google Drive object.
    :param file_id: The Google Drive file id
    :return: request
    :rtype: HttpRequest
    """
    request = service.files().get_media(fileId=file_id)
    return request


def download_content_from_request(file_handle, request: dict, chunk_size: int) -> None:
    """
    Download media resources.
    Note that  the Python file object is compatible with io.Base and can be used with this class also.
    :param file_handle: io.Base or file object. The stream in which to write the downloaded
        bytes.
    :param request: googleapiclient.http.HttpRequest, the media request to perform in chunks.
    :param chunk_size: int, File will be downloaded in chunks of this many bytes.
    """
    downloader = MediaIoBaseDownload(file_handle, request, chunksize=chunk_size)
    done = False
    while done is False:
        _, done = downloader.next_chunk()
    file_handle.flush()


def get_file_id(folder_id: str, file_name: str, drive_id: Optional[str] = None):
    """
    Returns the file id of a Google Drive file
    :param folder_id: The id of the Google Drive folder in which the file resides
    :param file_name: The name of a file in Google Drive
    :param drive_id: Optional. The id of the shared Google Drive in which the file resides.
    :return: Google Drive file id if the file exists, otherwise None
    :rtype: str if file exists else None
    """
    query = f"name = '{file_name}'"
    if folder_id:
        query += f" and parents in '{folder_id}'"
    if drive_id:
        files = (
            service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id, mimeType)",
                orderBy="modifiedTime desc",
                driveId=drive_id,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                corpora="drive",
            )
            .execute(num_retries=NUM_RETRIES)
        )
    else:
        files = (
            service.files()
            .list(q=query, spaces="drive", fields="files(id, mimeType)", orderBy="modifiedTime desc")
            .execute(num_retries=NUM_RETRIES)
        )
    file_metadata = {}
    if files['files']:
        file_metadata = {"id": files['files'][0]['id'], "mime_type": files['files'][0]['mimeType']}
    return file_metadata


def download_file(file_path: str, local_path: str, chunk_size: int = 104857600):
    """
    Download a file from Google Drive.
    :param file_id: the id of the file
    :param file_handle: file handle used to write the content to
    """
    logger = get_logger(__name__)

    directory_path, _, file_name = file_path.rpartition("/")

    current_parent = "root"
    directories = directory_path.split("/")
    for directory in directories:
        dir = get_file_id(current_parent, directory)
        current_parent = dir['id']

    file = get_file_id(current_parent, file_name)

    local_dir, _, local_file_name = local_path.rpartition("/")
    os.makedirs(local_dir, exist_ok=True)

    f = open(local_path, "wb")

    request = get_media_request(file_id=file['id'])
    download_content_from_request(file_handle=f, request=request, chunk_size=chunk_size)

    logger.debug(f"File from gdrive://{file_path} downloaded to {local_path}")

    f.flush()
    f.close()


def list_files():
    try:
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=50, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

