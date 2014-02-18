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

然后运行kindle.py即可。

本脚本支持导出txt普通文本格式，markdown文本格式，用于fortune程序的名言格式。

###普通文本###

    $ python kindle.py

去`clip`目录即可找到根据书名导出的摘录。

示例文本：

    请记住，所谓“流行”（传统观念也是一种流行），本质上就是自己看不见自己的样子。
    -At Kindle page:1036-1036

    ------------------

    如果你想要清晰地思考，就必须远离人群。但是走得越远，你的处境就会越困难，受到的阻力也会越大，因为你没有迎合社会习俗，而是一步步地与它背道而驰。小时候，每个人都会鼓励你不断成长，变成一个心智成熟、不再耍小孩子脾气的人。但是，很少有人鼓励你继续成长，变成一个怀疑和抵制社会错误潮流的人。
    -At Kindle page:1057-1059

    ------------------

###Markdown文本###

    $ python kindle.py -m

文件导出在`clip`目录.

示例文本：

    >请记住，所谓“流行”（传统观念也是一种流行），本质上就是自己看不见自己的样子。
    -At Kindle page:1036-1036

    ------------------

    >如果你想要清晰地思考，就必须远离人群。但是走得越远，你的处境就会越困难，受到的阻力也会越大，因为你没有迎合社会习俗，而是一步步地与它背道而驰。小时候，每个人都会鼓励你不断成长，变成一个心智成熟、不再耍小孩子脾气的人。但是，很少有人鼓励你继续成长，变成一个怀疑和抵制社会错误潮流的人。
    -At Kindle page:1057-1059

    ------------------

###Fortune格式###
Fortune是一个随机显示名言的Linux程序，其文本格式要求为：
每一条语句要放在一行中，行与行之间不要有空格。每条语句之间用`%`来分割。

    $ python kindle.py -f
文件导出在`fortune`目录中,文件名为`kindle-fortune`。

然后把`kindle-fortune`格式化为`fortune`识别的文件：

    $ strfile kindle-fortune

最后，使用：

   $ fortune /path/to/kindle-fortune

示例文本：

    可是這話也不真實：在某個時刻，在街上某個地點，你看見某種跡象顯示一些不可能誤解的、罕有的、也許是輝煌的事物：你很想把它講出來，但以前關於阿格蘿拉的一切傳說把你的詞彙堵死了，你只能重複別人的話而說不出自己的話。
    -看不見的城市 (卡爾維諾)
    %
    在我很年輕的時候，有一天早晨來到這裡，街上有許多人匆匆走向市場，婦女都有好看的牙齒並且坦率望進你的眼睛，三個兵士在高台上吹響小號，輪子在周圍轉動，彩旗在風裡飄揚。
    -看不見的城市 (卡爾維諾)
    %

使用效果：
>li@li ~
  % fortune ~/Workspace/Github/kindle-clips/fortune/kindle-fortune                                                                                              
  波羅：「從這花園平台望下去，也許只看得見我們心裡的湖——」 忽必烈：「無論我們作為軍人和商人的艱苦任務把我們帶到什麼地方，我們心裡還維護著這片靜寂的陰處、這斷斷續續的對話、這永遠不變的夜晚。」 波羅：「除非我們應當作相反的假設：在戰場和港口上搏鬥的人之所以存在，是因為我們兩人——自從盤古初開就靜止不動——在這竹籬笆裡念及他們。」 忽必烈：「除非勞動、吶喊、傷口、臭味都不存在，只有這叢杜鵑花。」 波羅：「除非腳夫、石匠、清道夫、清洗雞肺的廚子、石旁的浣衣婦、一邊燒飯一邊喂嬰兒的母親之所以存在，只是因為我們心念裡想到他們。」 忽必烈：「說實話，我從來不想這些人。」 波羅：「那麼，他們是不存在的。」 忽必烈：「我看這種假設似乎並不符合我們目的。沒有這些人，我們就不可能躺在這吊床裡蕩來蕩去。」 波羅：「那麼我們必須拒絕這種假設。就是說，另一種假設才是正確的：他們存在，我們不存在。」 忽必烈：「我們已經證明，假如我們在這裡，我們就不存在。」 波羅：「而事實上，我們確實在這裡。」
 
>  -看不見的城市 (卡爾維諾)

##Tips##
1. 若需修改文件格式，修改`kindle.py`中的`export_txt`函数。

2. 排列样式如不符合要求，修改`get_note_format`和`get_highlight_format`函数即可。

3. 使用`-h`参数查看帮助。

4. 任何建议，欢迎交流。

##参考
* [lxyu-Kindle Clippings](https://github.com/lxyu/kindle-clippings)
* [自己定制mint-fortune 打造个性linuxmint终端窗口](http://blog.51osos.com/linux/mint-fortune-linuxmint-terminal/)




