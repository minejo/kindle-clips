kindle-clips
============

使用kindle-clips导出笔记，标注和剪贴文章。

## About My Clippings.txt
在`My Clippings.txt`中，有4种类型的摘录。每一种类型都只占4行。
### 书签 ###
格式为：

    Book Title\n
    - 我的书签 位置N | 已添加至 sometime\n
    \n
    \n

### 标注 ###
格式为：

    Book Title\n
    - 我的标注 位置N-N | 已添加至 sometime\n
    \n
    标注内容\n

### 笔记 ###
笔记比较特殊，笔记是与标注连在一起的。表示该笔记是在该标注上完成的。

    Book Title\n
    - 我的笔记 位置N | 已添加至 sometime\n
    \n
    笔记内容\n
    ==========\n
    Book Title\n
    - 我的标注 位置N-N | 已添加至 sometime\n
    \n
    标注内容\n

### 剪贴文章 ###

    Book Title\n
    - 剪贴文章 位置N | 已添加至 sometime\n
    \n
    剪贴文章内容\n

每一个摘录都用`==========\n`分割开。


##关于脚本##
--------

Clippings are stored in a python dict with this structure

    clips = {'book': {'position': 'clipping'}}

Msgpack was used to serialize clippings for archive.

Each new `My Clippings.txt` will add clips to previous archive automatically.

Clips will be export to `output` directory, find them there.


##使用##
首先需要安装`msgpack-python`包。

    $ pip install msgpack-python

clone该项目并把`My Clippings.txt`复制到该项目根目录。

然后运行kindle.py即可

    $ python kindle.py

去`output`目录即可找到根据书名导出的摘录。

##Tips##
1. 目前导出的摘录为`.md`格式，若需修改格式，修改`kindle.py`中的`export_txt`函数。

2. 导出摘录的排列各种为适应于markdown格式的，如需修改，修改`get_note_format`和`get_highlight_format`函数即可。

3. 任何建议，欢迎交流。

##参考
* [lxyu-Kindle Clippings](https://github.com/lxyu/kindle-clippings)




