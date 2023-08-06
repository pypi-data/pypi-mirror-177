##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import os, datetime, time
from uuid import uuid4

STORAGE_TOTAL = 0
STORAGE_LIMIT = 1024 * 1024 * 1024 * 1024  # Assume the largest storage total

# Support downloading object under a different name
# Add log and summary objects that support a download function
# Shared between local storage and cloud storage
class LocalFile:
    def __init__(
        self,
        path: str,
    ):
        self._key = str(uuid4())
        self._path = optumi.utils.fix_path(os.path.abspath(os.path.expanduser(path)))

    def upload(self, wait=True):
        print("Uploading file...", self)
        optumi.core.upload_files(
            self._key, [self._path], True, STORAGE_TOTAL, STORAGE_LIMIT, True
        )

        if wait:
            while True:
                progress = optumi.core.get_upload_progress([self._key])
                time.sleep(0.2)
                if progress[self._key]["progress"] < 0:
                    break

            print("...completed")

    @property
    def path(self):
        return os.path.abspath(os.path.expanduser(self._path))

    @property
    def hash(self):
        return optumi.utils.hash_file(self._path)

    @property
    def size(self):
        return os.path.getsize(self._path)

    @property
    def created(self):
        return (
            datetime.datetime.utcfromtimestamp(os.stat(self._path).st_ctime).isoformat()
            + "Z"
        )

    @property
    def modified(self):
        return (
            datetime.datetime.utcfromtimestamp(os.stat(self._path).st_mtime).isoformat()
            + "Z"
        )

    def __str__(self):
        return self.path + " " + str(self.size) + " " + self.modified
