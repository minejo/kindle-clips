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

def get_clip(section):
    clip = {}

    lines = [l for l in section.split('\n') if l]
    if len(lines) != 3:
        return

    position = re.findall(r'[\d]+-[\d]+', lines[1])
    clip['position'] = position[0]
    clip['book'] = lines[0]
    clip['content'] = lines[2]

    return clip

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
        
        filename = os.path.join(OUTPUT_DIR, "%s.txt" % book)
        with open(filename, 'w') as f:
            f.write('\n\n-----\n\n'.join(lines))

def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return msgpack.unpack(f,encoding='utf-8')
    except IOError:
        return {}

def main():
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    sections = get_sections(FILE_NAME)
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][clip['position']] = clip['content']

    save_clips(clips)
    export_txt(clips)

if __name__ == '__main__':
    main()
