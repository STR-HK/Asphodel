import os
import pathlib
import datetime
import pymediainfo
from moviepy.editor import *

readerPath = './assets/taskmgr/'
thumbnailPath = './assets/thumbnail/'

B = 1024 ** 0
KB = 1024 ** 1
MB = 1024 ** 2
GB = 1024 ** 3
TB = 1024 ** 4
PB = 1024 ** 5

def MyUnitChange(size):
    if (size == 0):
        return [str(int(0)), 'B']
    elif (B <= size < KB):
        return [str(int(round(size / B))) , 'B']
    elif (KB <= size < MB):
        return [str(int(round(size / KB, 0))) , 'KB']
    elif (MB <= size < GB):
        return [str(int(round(size / MB))) , 'MB']
    elif (GB <= size < TB):
        return [str(float(round(size / GB, 1))) , 'GB']
    elif (TB <= size < PB):
        return [str(int(round(size / TB, 0))) , 'TB']

def read_metadata(readerPath, firstLevelFile, folderInherit=False, folderPath=None):
    fullpath = readerPath + firstLevelFile

    time = datetime.datetime.fromtimestamp(pathlib.Path(fullpath).stat().st_mtime)
    path = fullpath

    creationtime_t = int(time.timestamp() * 1000000)
    creationtime = time.strftime("%Y/%m/%d %H:%M:%S.%f")

    name = list(os.path.splitext(firstLevelFile))[0]
    ext = list(os.path.splitext(firstLevelFile))[1].replace('.','')
    if ext == "": ext = None

    size = os.path.getsize(fullpath)
    length = None
    lengthIso = None
    resolution = None

    if os.path.isfile(fullpath):
        type_ = ['Single']
        fileinfo = pymediainfo.MediaInfo.parse(fullpath)
        for track in fileinfo.tracks:
            if track.track_type == 'Video':
                type_.append('Video')
                length = track.other_duration[3]
                lengthIso = track.other_duration[1]
                MyThumbnail = '{}{}.jpg'.format(thumbnailPath, name)
                if not os.path.isfile(MyThumbnail):
                    if (os.path.isdir('{}{}'.format(thumbnailPath, folderPath)) == False and folderInherit == True):
                        os.makedirs('{}{}'.format(thumbnailPath, folderPath))
                    clip = VideoFileClip(fullpath)
                    try: clip.save_frame(MyThumbnail, t=30)
                    except: clip.save_frame(MyThumbnail, t=10)
                resolution = [int(track.width), int(track.height)]
            elif track.track_type == 'Image':
                type_.append('Image')
                try: resolution = [int(track.width), int(track.height)]
                except: resolution = None
            
    elif os.path.isdir(fullpath):
        type_ = ['Folder']
        foldersize = []
        for f in os.listdir(fullpath):
            f = '{}/{}'.format(fullpath, f)
            if os.path.isfile(f):
                foldersize.append(os.path.getsize(f))
        size = sum(foldersize)
        
    bytesize = size
    changed_sized = MyUnitChange(bytesize)
    size = '{} {}'.format(changed_sized[0], changed_sized[1])
    tags = []
    
    solved = {'path':path, 'creationtime_t':creationtime_t,  'creationtime':creationtime, 
                'name':name, 'size':size, 'bytesize':bytesize, 'length':length, 'lengthIso':lengthIso,
                'type':type_, 'resolution':resolution, 'tags':tags, 
                'extension':ext, 'children':[]}

    return solved

children = list()

def create_file_metadata():
    global read
    # 파일 목록을 읽어옵니다
    firstFilesOfDir = os.listdir(readerPath)

    # 돌려줄 정보의 묶음을 담을 리스틀 만듭니다
    reads = list()

    # 첫번째 파일 리스트의 모든 파일을 분석합니다
    for firstLevelFile in firstFilesOfDir:

        # 선택된 파일의 일부 상대경로를 가져옵니다
        fullpath = readerPath + firstLevelFile

        children = list()
        read = read_metadata(readerPath, firstLevelFile)

        if os.path.isdir(fullpath):
            recursion_metatdata(fullpath, firstLevelFile, [])
        if children != []: read['children'] = children
        reads.append(read)

    return reads

def recursion_metatdata(fullpath, firstLevelFile, newchilden):
    for f in os.listdir(fullpath):
        realfolderfile = '{}/{}'.format(firstLevelFile, f)
        r = read_metadata(readerPath, realfolderfile, folderInherit=True, folderPath=firstLevelFile)
        insert(r)
        newrealfolderfile = '{}/{}'.format(firstLevelFile, f)
        newMaxPath = readerPath + realfolderfile
        if os.path.isdir(newMaxPath):
            recursion_metatdata(newMaxPath, newrealfolderfile, newchilden)

def insert(what):
    splited = what['path'].split('/')

    group = list()
    for s in range(len(splited) - 3):
        group.append('/'.join(splited[ 0 : (s + 3) ]))
    
    children = read['children']
    path = read['path']
    for s, spath in enumerate(group):
        if path == spath and s == ( len(group) - 1 ):
            children.append(what)
            return

    repeat_insert(children, group, what)

def repeat_insert(given_children, group, what):
    for gr in given_children:
        if gr['path'] == group[-1]:
            if what not in gr['children']:
                gr['children'].append(what)
            return
        repeat_insert(given_children[-1]['children'], group, what)

from Asphodel import app

@app.get('/taskmgr/import')
async def taskmgr_import():
    return {'response':create_file_metadata()}

def get_name_metadata(dataset):
    names = list()
    for data in dataset:
        if data['extension'] != None: names.append('{}.{}'.format(data['name'], data['extension']))
        else: names.append(data['name'])
    return names

from modules import configparser

def insert_to_sqlDB(dataset):
    for data in dataset:
        configparser.insert_value(path=data['path'], creationtime=data['creationtime'], creationtime_t=data['creationtime_t'],
                                    name=data['name'], size=data['size'], bytesize=data['bytesize'],
                                    length=data['length'], lengthIso=data['lengthIso'], type_=data['type'],
                                    resolution=data['resolution'], tags=data['tags'],
                                extension=data['extension'], children=data['children'])