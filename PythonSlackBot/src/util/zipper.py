import logging
from zipfile import ZipFile, BadZipFile
from io import BytesIO

logger = logging.getLogger(__name__)


def unzip(zipfile):
    try:
        byte_data = ZipFile(BytesIO(zipfile))

        # ToDo Do for each file and return file list
        file = byte_data.open(byte_data.filelist[0].filename).read().decode('utf-8')

        return file
    except BadZipFile:
        logger.error("Couldn't unzip file with name %s", byte_data.filelist[0].filename)
    except Exception as e:
        logger.error("Unhandled Exception: \n%s", e)
