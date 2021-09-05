import os
import datetime
import pathlib
import json
from posixpath import splitext

import pymediainfo

# info = pymediainfo.MediaInfo.parse(relative_path)

# for track in info.tracks:
#     print(track.track_type)

#     if track.track_type == "General":
#         print()

# print(info.to_json())

# class TaskmgrData:
#     def __init__(self) -> None:
#         pass

#     def data(self):
#         self.dir =


def scrapChildMetadata(childFolder):
    db_plain = childFolder.removeprefix("./assets/taskmgr/")
    db_dir = childFolder
    db_filedir = childFolder
    db_filename = os.path.split(childFolder)[-1]
    db_name = os.path.basename(os.path.splitext(childFolder)[0])
    db_time = datetime.datetime.fromtimestamp(os.stat(db_dir).st_mtime)

    db_size = 0
    db_type = []

    db_duration = 0
    db_resloution = []
    db_extension = None

    if os.path.isfile(db_dir):

        db_stat = "File"

        db_size = os.path.getsize(db_dir)

        info = pymediainfo.MediaInfo.parse(db_dir)

        for track in json.loads(info.to_json())["tracks"]:

            track_type = track["track_type"]

            if track_type not in db_type:
                db_type.append(track["track_type"])

            if track_type == "General":
                db_extension = track["file_extension"]

            if track_type == "Video":
                db_duration = track["duration"]

            if track_type in ["Video", "Image"]:
                db_resloution = [track["width"], track["height"]]

        # General
        # Video
        # Audio
        # Text
        # Image
        # Other

    elif os.path.isdir(db_dir):

        db_stat = "Folder"

        for path, dirs, files in os.walk(db_dir):

            for file in files:

                filepath = os.path.join(path, file)
                db_size += os.path.getsize(filepath)
                

    # print(f"db_plain : {db_plain}")
    # print(f"db_dir : {db_dir}")
    # print(f"db_filedir : {db_filedir}")
    # print(f"db_filename : {db_filename}")
    # print(f"db_name : {db_name}")
    # print(f"db_time : {db_time}")

    # print(f"db_type : {db_type}")
    # print(f"db_size : {db_size}")
    # print(f"db_stat : {db_stat}")

    # print(f"db_duration : {db_duration}")
    # print(f"db_resolution : {db_resloution}")
    # print(f"db_extension : {db_extension}")

    # print("\n")

    datum = {
        # "dir": db_dir,
        # "filedir": db_filedir,
        "plain": db_plain,
        # "filename": db_filename,
        # "name": db_name,
        # "time": db_time,
        # "type": db_type,
        # "size": db_size,
        "stat": db_stat,
        # "duration": db_duration,
        # "resolution": db_resloution,
        # "extension": db_extension,
    }
    # print(datum)
    return datum

def clean_path(path):
    path = path.removeprefix('/').removesuffix('/')
    path += '/'

    if path == '/':
        path = ''

    return path

readerFolder = "./import/resources/"

from Asphodel import app
@app.get("/taskmgr/import")
def generate_metadata(dir):
    dir = clean_path(dir)
    metadata = []

    realdir = f"{readerFolder}{dir}"

    for file in os.listdir(realdir):
        metadata.append(scrapChildMetadata(f"{realdir}{file}"))

    print(metadata)
    return metadata

generate_metadata("/")