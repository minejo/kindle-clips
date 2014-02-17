#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import collections
import os
import msgpack

BOUNDARY = "==========\n"
OUTPUT_DIR = "output"
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
    print(clip)
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

def export_txt(clips):
    """
    Export each book's clipping to a single markdown file
    """
    for book in clips:
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos])
            print(clips[book][pos])
        
        filename = os.path.join(OUTPUT_DIR, "%s.md" % book)
        with open(filename, 'w') as f:
            f.write('\n\n-----------------\n\n'.join(lines))

def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return msgpack.unpack(f,encoding='utf-8')
    except IOError:
        return {}

def get_note_format(clip):
    """Note的表现样式，与markdown结合"""
    position = clip['position']
    highlight = clip['content']
    note = clip['note']
    format = ">" + highlight + "\nNote:**"+note +"**\n-At Kindle page:" + position
    return format

def get_highlight_format(clip):
    """Highlight的表现样式，与markdown相结合""" 
    position = clip['position']
    highlight = clip['content']
    format = ">" + highlight + "\n-At Kindle page:" + position
    return format


def main():
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    sections = get_sections(FILE_NAME)
    nextpass = 0
    for i,section in enumerate(sections):
        if nextpass:
            nextpass = 0
            continue

        print(get_type(section))
        if get_type(section) == 0:
            continue
        if get_type(section) == 1:
            clip = get_highlight(section)
            clips[clip['book']][clip['position']] = get_highlight_format(clip)
        else:
            if get_type(section) == 2:
                clip = get_note(sections[i+1], section)
                clips[clip['book']][clip['position']] = get_note_format(clip)
                nextpass = 1
                print(clips[clip['book']][clip['position']])
            else:
                clip = get_clip(section)
                clips[clip['book']][clip['position']] = get_highlight_format(clip)


    save_clips(clips)
    export_txt(clips)

if __name__ == '__main__':
    main()
