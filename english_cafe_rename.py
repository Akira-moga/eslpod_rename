#This is my first Python program.
#It will renames eslpod cast mp3 files and set id3 titles.

# coding:utf-8
import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')
import os
import eyed3
import mimetypes
import re
import binascii

#directory for eslpod.mp3
path = "/Volumes/Share/eslpod/ec/"
#prefix to rename mp3 files
prefix = "EC"
#max track in a disc
max_track_in_a_disk = 100

#extract number pettern
pattern=r'[+-]?\d+'

def isMp3File(fullpath):
    if os.path.isfile(fullpath):
        mime = mimetypes.guess_type(fullpath)
        if mime[0] == "audio/mpeg":
            return True
    return False


def getMp3FileList(dirPath):
    files = []
    for filename in os.listdir(dirPath):
        fullpath = dirPath + filename
        if isMp3File(fullpath):
            files = files + [filename]
    return files

def getTotalDiskNumber(total_track_count):
    max_disc_no = total_track_count / max_track_in_a_disk
    if (len(files) % max_track_in_a_disk) == 0:
        return max_disc_no
    else:
        return max_disc_no + 1



files = getMp3FileList(path)
total_disk_no = getTotalDiskNumber(len(files))
current_disc_no = 0
index = 0
for filename in files:
    fullpath = path + filename
    if isMp3File(fullpath):
        match = re.findall(pattern,filename)
        fileNo = int(match[0])
        index = index + 1
        #rename filename to "ESL PodcastXXXX.mp3"
        new_file_name = path + prefix + "%03d.mp3" %(fileNo)
        os.rename(fullpath , new_file_name)

        #edit the tag
        audiofile = eyed3.load(new_file_name)
        tag = audiofile.tag
        tag.album = u"English as a Second Language Podcast English Cafe"
        tag.artist = u"Center for Educational Development"
        tag.album_artist = u"Center for Educational Development"
        tag.composer = tag.artist
        if (index - 1) % max_track_in_a_disk == 0:
            current_disc_no = current_disc_no + 1
        tag.track_num = (index)
        tag.disc_num = (current_disc_no, total_disk_no)
        tag.title = u"English Cafe #" + str(fileNo)
        print tag.title.encode('utf_8')
        print tag.disc_num
        tag.save(filename=new_file_name,version=eyed3.id3.tag.ID3_V2_4,encoding='utf_8')
