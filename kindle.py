#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import collections
import os
import msgpack
import sys
import getopt

BOUNDARY = "==========\n"
OUTPUT_DIR = "clip"
FORTUNE_DIR = "fortune"
FORTUNE_FILE = "kindle-fortune"
FILE_NAME = "My Clippings.txt"
DATA_FILE = "clips.msgpack"

def get_sections(filename):
    with open(filename, 'r') as f:
        content = f.read()
    content = content.replace("\ufeff", "")
    return content.split(BOUNDARY)

def get_highlight(section):
    clip = {}
    lines = [l for l in section.split('\n') if l]
    position = re.findall(r'[\d]+-[\d]+', lines[1])
    clip['position'] = position[0]
    clip['book'] = lines[0]
    clip['content'] = lines[2]

    return clip

def get_note(high_section, note_section):
    notelines = [l for l in note_section.split('\n') if l]
    note = notelines[2]

    clip = get_highlight(high_section)
    clip['note'] = note
    return clip
    
def get_clip(section):
    clip = {}
    lines = [l for l in section.split('\n') if l]
    position = re.findall(r'[\d]+', lines[1])[0]
    clip['position'] = position
    clip['book'] = lines[0]
    clip['content'] = lines[2]
    
    return clip

def get_type(section):
    """设BookMark为0，Highlight为1，Note为2, ClipAritle为3"""
    lines = [l for l in section.split('\n') if l]
    if len(lines) != 3:
        return 0

    if re.findall(r'[\d]+-[\d]+', lines[1]):
        return 1
    else:
        if re.findall(r'剪贴|Clip', lines[1]):
            return 3
        else:
            return 2

def save_clips(clips):
    """
    save clips to DATA_FILE
    """
    with open(DATA_FILE, 'wb') as f:
        f.write(msgpack.packb(clips))

def export_txt(clips,type):
    """
    Export each book's clipping to a single markdown file
    """
    for book in clips:
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos])
        
        if type == "markdown":
            filename = os.path.join(OUTPUT_DIR, "%s.md" % book)
        elif type == "common":
            filename = os.path.join(OUTPUT_DIR, "%s.txt" % book)
        elif type == "fortune":
            filename = os.path.join(FORTUNE_DIR, FORTUNE_FILE)

        if type in ("markdown","common"):
            with open(filename, 'w') as f:
                f.write(''.join(lines))
        elif type == "fortune":
            with open(filename, 'a') as f:
                f.write(''.join(lines))

    print("Done! Go to the output directory to checkout the clipping files.^.^")


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return msgpack.unpack(f,encoding='utf-8')
    except IOError:
        return {}

def get_note_format(clip,type):
    """Note的表现样式，与markdown结合"""
    position = clip['position']
    highlight = clip['content']
    note = clip['note']
    book = clip['book']
    if type == "markdown":
        format = ">" + highlight + "\nNote:**"+note +"**\n-At Kindle page:" + position + "\n\n--------------\n\n"
    elif type == "fortune":
        format = highlight + "\nNote: " + note + "\n-" + book + "\n%\n"
    elif type == "common":
        format = highlight + "\nNote: " + note + "\n-At Kindle page:" + position + "\n\n------------------\n\n"
    return format

def get_highlight_format(clip,type):
    """Highlight的表现样式，与markdown相结合""" 
    position = clip['position']
    highlight = clip['content']
    book = clip['book']
    if type == "markdown":
        format = ">" + highlight + "\n-At Kindle page:" + position +"\n\n------------------\n\n"
    elif type == "fortune":
        format = highlight + "\n-" + book + "\n%\n"
    elif type == "common":
        format = highlight + "\n-At Kindle page:" + position + "\n\n------------------\n\n"
    return format

def help():
    print("""welcome to use kindle-clips.
       -m --markdown 导出markdown格式的书摘
       -f --fortune  导出fortune格式的书摘
       默认导出txt文本格式。""")
    return

def checkdirectory():
    if not os.path.exists(FORTUNE_DIR):
        os.mkdir(FORTUNE_DIR)

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    return 

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hfmi",["help","fortune","markdown"])
    except getopt.GetoptError:
        print("参数出错，-h查看参数使用")
        sys.exit(2)

    type = "common"
    checkdirectory()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-f", "--fortune"):
            type = "fortune"
            os.remove(os.path.join(FORTUNE_DIR, FORTUNE_FILE))
        elif opt in ("-m", "--markdown"):
            type = "markdown"
        elif opt == "-m":
            FILE_NAME = arg


    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    sections = get_sections(FILE_NAME)
    nextpass = 0
    for i,section in enumerate(sections):
        if nextpass:
            nextpass = 0
            continue

        if get_type(section) == 0:
            continue
        if get_type(section) == 1:
            clip = get_highlight(section)
            clips[clip['book']][clip['position']] = get_highlight_format(clip,type)
        else:
            if get_type(section) == 2:
                clip = get_note(sections[i+1], section)
                clips[clip['book']][clip['position']] = get_note_format(clip,type)
                nextpass = 1
            else:
                clip = get_clip(section)
                clips[clip['book']][clip['position']] = get_highlight_format(clip,type)


    save_clips(clips)
    export_txt(clips,type)

if __name__ == '__main__':
    main(sys.argv[1:])
