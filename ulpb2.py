#! /usr/bin/python3
# 用 shell 脚本反复调用 python 程序实在是太慢了，
# 处理十万多行数据居然花了九个多小时。。纯 python 脚本只要 10 秒

import sys, os, re
from pypinyin import lazy_pinyin, Style

if len(sys.argv) != 3:
    print("Usage: $0 <inputfile> <outputfile>", file=sys.stderr)
    os._exit(1)


# 声母转换表
ulpb1 = {'sh': 'u', 'ch': 'i', 'zh': 'v'}
# 韵母转换表
ulpb2 = {'iu': 'q', 'ei': 'w', 'uan': 'r', 'ue': 't',
        'un': 'y', 'uo': 'o', 'ie': 'p',
        'ong': 's', 'iong': 's', 'ai': 'd', 'en': 'f', 'eng': 'g',
        'ang': 'h', 'an': 'j', 'uai': 'k', 'ing': 'k', 'uang': 'l', 'iang': 'l',
        'ou': 'z', 'ua': 'x', 'ia': 'x', 'ao': 'c',
        'ui': 'v', 'in': 'b', 'iao': 'n', 'ian': 'm'}
# 零声母转换表
ulpb3 = {'a': 'aa', 'e': 'ee', 'o': 'oo', 'ang': 'ah', 'eng': 'eg'}

style1 = Style.INITIALS
style2 = Style.FINALS

# 将汉字转换成双拼
def ulpb(key):
    # https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict
    lt1 = lazy_pinyin(key, style=style1, strict=False)
    lt2 = lazy_pinyin(key, style=style2, strict=False)

    for i in range(len(key)):
        if len(lt1[i]) > 0:         # 有声母
            try:
                value += ulpb1.get(lt1[i], lt1[i]) + ulpb2.get(lt2[i], lt2[i])
            except:
                value = ulpb1.get(lt1[i], lt1[i]) + ulpb2.get(lt2[i], lt2[i])
        else:                       # 无声母
            value = value + ulpb3.get(lt2[i], lt2[i]) if 'value' in dir() else ulpb3.get(lt2[i], lt2[i])
    return value



regex = r"^\$ddcmd\((.+?),.+?\)\s+(?=\w+$)"       # 匹配一条记录，不包括最后的全拼
pattern = re.compile(regex)

with open(sys.argv[1], 'r', encoding='utf-8-sig') as f1:                 # 输入文件
    with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f2:   # 输出文件
        for line in f1:                                                  # 逐行处理
            matcher = re.search(pattern, line)
            if matcher != None:                   # 匹配
                outputstr = matcher.group(0) + ulpb(matcher.group(1)) + '\n'
            else:                                 # 不匹配
                outputstr = line
            #print(outputstr, end='')
            f2.write(outputstr)
