##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

from .CloudFile import *
from .CloudFileVersion import *

import json, datetime, time

from pathlib import Path


# Support downloading object under a different name
class CloudStorage(list):
    def __init__(self, files: list = []):
        self._key = str(uuid4())
        super().__init__(files)

    def download(self, wait=True):
        if len(self) > 0:
            print("Downloading", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            optumi.core.download_files(
                self._key,
                [x.versions[0].hash for x in self],
                [x.versions[0].path for x in self],
                [x.versions[0].size for x in self],
                False,
                None,
            )

            if wait:
                while True:
                    progress = optumi.core.get_download_progress([self._key])
                    time.sleep(0.2)
                    if progress[self._key]["progress"] < 0:
                        break

                print("...completed")

    def remove(self):
        if len(self) > 0:
            print("Removing", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            hashes = []
            paths = []
            created = []

            for cloud_file in self:
                for version in cloud_file.versions:
                    hashes.append(version.hash)
                    paths.append(version.path)
                    created.append(version.created)

            optumi.core.delete_files(
                hashes,
                paths,
                created,
                "",
            )
            print("...completed")

    @classmethod
    def list(self):
        res = optumi.core.list_files()
        response = json.loads(res.text)
        files = CloudStorage()
        versions = {}

        for i in range(len(response["files"])):
            path = response["files"][i]
            version = CloudFileVersion(
                path,
                response["hashes"][i],
                response["filessize"][i],
                response["filescrt"][i],
                response["filesmod"][i],
            )
            if path in versions:
                versions[path].append(version)
            else:
                versions[path] = [version]

        for path in versions:
            files.append(CloudFile(path, versions[path]))

        return files

    @classmethod
    def expandpath(self, localFile):
        if not localFile:
            return localFile
        # Resolve the '~'
        expand = os.path.expanduser(localFile)
        # Create an absolute path
        if not os.path.isabs(expand):
            expand = Path(os.getcwd()) / expand
        return str(expand)

    @classmethod
    def find(self, match="", contains=""):
        if match:
            return CloudStorage(
                [
                    x
                    for x in CloudStorage.list()
                    if CloudStorage.expandpath(match) == os.path.expanduser(x.path)
                ]
            )
        elif contains:
            return CloudStorage(
                [
                    x
                    for x in CloudStorage.list()
                    if str(contains) in os.path.expanduser(x.path)
                ]
            )
        else:
            return CloudStorage([])

    def __str__(self):
        return str([str(x) for x in self])
