# genshin-piano-player
## 介绍：
这是一个基于`Python`以及`keyboard`模块的原神风物之琴/镜花只琴自动演奏器

本程序理论仅能运行在`Windows`环境下，暂不考虑对其他系统的支持

**注意：使用这个项目有可能会带来潜在的封禁的风险，请在游戏中使用时三思而后行！**

## 开始使用
```shell
python3 -m pip install requirements.txt 
python3 player.py <曲谱所在路径>
```
此外，请拷贝一份配置文件从`config.default.yml`到`config.yml`，否则程序会报错

## 制谱规范
可以参考以下文本，或者参考`songs/demo.txt`
```text
歌曲名称 字符串
歌曲作者 字符串
谱师 字符串
1 # 每行之间演奏速度，以秒为单位
附言（支持使用{newline}换行） 字符串
---（本行不读）
d1 d2 d3 # 在一行内的音符视为同时演奏的音符
d1 # 末尾不要留空格，不然会有bug，也不要加注释，是方便讲解的
d1
d1
# 空行视为休止符

d3
```

## 配置文件讲解
```yaml
enable_driver: false # 是否启用驱动级控制
enable_browser: true # 是否启用浏览器预览
browser_live_url: 'https://yuxiangwang0525.github.io/Windsong-piano/' # 浏览器预览地址

```

## TODO
[] midi转换器支持

[] bpm支持

[] 驱动级硬件模拟

[] argparse支持

[] 提升程序健壮性

[] 自 助 选 歌 系 统
