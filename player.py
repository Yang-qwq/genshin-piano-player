# -*- coding: utf-8 -*-
# 本程序理论仅能运行在Windows环境下，暂不考虑对其他系统的支持
import sys
import time
import keyboard
import webbrowser
import os
import yaml
import ctypes

__playing_status__ = False
__pid__ = os.getpid()

dd_keys = {
    'c': 503,
    'n': 506,
    'z': 501,
    'd': 403,
    # 'l': 409,
    'w': 302,
    'u': 307,
    'e': 303,
    'f': 404,
    'y': 306,
    'x': 502,
    'g': 405,
    'v': 504,
    'r': 304,
    # 'i': 308,
    'a': 401,
    'm': 507,
    'h': 406,
    'b': 505,
    # 'k': 408,
    'q': 301,
    'j': 407,
    # 'p': 310,
    # 'o': 309,
    't': 305,
    's': 402,
}

__note2keys_data__ = {
    # 1
    'd1': 'z',
    'r1': 'x',
    'm1': 'c',
    'f1': 'v',
    's1': 'b',
    'l1': 'n',
    't1': 'm',

    # 2
    'd2': 'a',
    'r2': 's',
    'm2': 'd',
    'f2': 'f',
    's2': 'g',
    'l2': 'h',
    't2': 'j',

    # 3
    'd3': 'q',
    'r3': 'w',
    'm3': 'e',
    'f3': 'r',
    's3': 't',
    'l3': 'y',
    't3': 'u',

    # 其他
    ' ': 'pass',
    '': 'pass'
}


class Song(object):
    def __init__(self, lines: list):
        # 处理乐谱
        self.data = lines
        self.song_name = lines[0]
        self.author = lines[1]
        self.mapper = lines[2]
        self.speed = float(lines[3])
        self.comment = lines[4].format(newline='\n')

        # 读取后删除无用数据
        # lines = []

        for i in range(0, 6):
            self.data.pop(0)

    def print_meta(self):
        print("""歌曲名称：{name}
歌曲作者：{author}
谱师：{mappper}
附言：{comment}""".format(name=self.song_name, author=self.author, mappper=self.mapper, comment=self.comment))

    def get_speed(self):
        return self.speed

    def get_map_data(self):
        notes = []
        for line in self.data:
            notes.append(line.split(' '))
        return notes

    def note2keys(self):
        # map_data = [[<notes>], [<notes>], [<notes>]]
        map_data = self.get_map_data()
        new_map_data = []
        for note_lines in map_data:
            # note_lines = [note_a, note_b, note_3]
            new_list = []
            for note in note_lines:
                # note = 'd1'
                new_key = __note2keys_data__[note]
                new_list.append(new_key)
            new_map_data.append(new_list)
        return new_map_data


def press(keys: list):
    print('[%s]: %s %s' % (note_cursor, keys, '(driver=' + str(__driver_status__) + ')'))
    if __driver_status__ is not False and conf_enable_driver is True:
        # 按下
        for key in keys:
            if key is not 'pass':
                dd_dll.DD_key(dd_keys[key], 1)
            else:
                pass

        # 抬起
        for key in keys:
            dd_dll.DD_key(dd_keys[key], 2)
    else:
        for key in keys:
            if key is not 'pass':
                keyboard.press(key)
            else:
                pass


def f8exit():
    print('f8 已被按下，停止演奏！')
    print('正在杀死进程 pid={}'.format(__pid__))
    os.kill(__pid__, 2)


def main():
    global conf_enable_driver
    global __playing_status__
    global dd_dll
    global __driver_status__
    global note_cursor

    # 读取配置
    with open('config.yml', 'r', encoding='utf-8') as f:
        conf = yaml.safe_load(f)
    conf_enable_driver = conf['driver']['enable']
    conf_enable_browser = conf['enable_browser']
    conf_browser_live = conf['browser_live_url']
    conf_driver_path = conf['driver']['path']
    print(conf_driver_path)

    # 判断驱动设置并加载它（未完成）
    if conf_enable_driver is True:
        try:
            dd_dll = ctypes.windll.LoadLibrary(conf_driver_path)
        except:
            __driver_status__ = False
        else:
            print('驱动已启用')
            __driver_status__ = True
    else:
        __driver_status__ = False

    print('准备中，请稍后...')

    # 读取歌曲
    song_path = sys.argv[1]
    with open(song_path, 'r', encoding='utf-8') as song:
        song_lines = song.read().splitlines()

    song = Song(song_lines)
    song.print_meta()

    if conf_enable_browser:
        webbrowser.open(conf_browser_live)
        time.sleep(3)

    map_data = song.note2keys()
    print('已准备好演奏歌曲，如果你已经切换到了指定的界面，请按 p 开始演奏，并且可以使用 F8 停止演奏')
    keyboard.wait('p')

    # 绑定退出热键
    keyboard.add_hotkey('f8', f8exit)

    # 开始
    __playing_status__ = True
    note_cursor = 0
    for keys in map_data:
        note_cursor += 1
        press(keys)
        time.sleep(song.get_speed())
        if __playing_status__ is not True:
            break

    print('演奏完成！进程正在退出')

    return 0


if __name__ == '__main__':
    sys.exit(main())
