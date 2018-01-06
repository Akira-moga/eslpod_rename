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
path = "/Volumes/Share/eslpod/eslpod/"
#prefix to rename mp3 files
prefix = "ESLPod"
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

def getTitle(tag):
    isMatch = False
    for comment in tag.comments:
        match = re.search(r"(ESL|esl)", comment.text)
        if match:
            isMatch = True
            break
    if isMatch:
        title = comment.text.replace('\r\n', ".")
        title = title.replace('\r', ".")
        title = title.replace('\n', ".")
        title = title.replace('http', ".")
        title = title + u"."
    else:
        title = tag.title + u"."

    match = re.search(u"(: |-|–)(.*?)(\.|@|http)", title)
    if match:
        a =  match.group(2).strip() + u'.'
        b = u"ESL Podcast #" + unicode(fileNo)
        ret_title = b + u" - " + a
        isMatch = True
    else:
        ret_title = title
        isMatch = False
    return isMatch, ret_title

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
        new_file_name = path + prefix + "%04d.mp3" %(fileNo)
        os.rename(fullpath , new_file_name)

        #edit the tag
        audiofile = eyed3.load(new_file_name)
        tag = audiofile.tag
        tag.album = u"English as a Second Language Podcast"
        tag.artist = u"Center for Educational Development"
        tag.album_artist = u"Center for Educational Development"
        tag.composer = tag.artist
        result = getTitle(tag)
        if result[0]:
            tag.title = result[1]
        else:
            print "can't convert title!!!!!!!"

        if (index - 1) % max_track_in_a_disk == 0:
            current_disc_no = current_disc_no + 1
        tag.track_num = (index)
        tag.disc_num = (current_disc_no, total_disk_no)
        print tag.title.encode('utf_8')
        print tag.disc_num
        tag.save(filename=new_file_name,version=eyed3.id3.tag.ID3_V2_4,encoding='utf_8')
