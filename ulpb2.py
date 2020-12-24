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
ulpb2 = {'iu': 'q', 'ei': 'w', 'uan': 'r', 'ue': 't', 've': 't',
        'un': 'y', 'uo': 'o', 'ie': 'p',
        'ong': 's', 'iong': 's', 'ai': 'd', 'en': 'f', 'eng': 'g',
        'ang': 'h', 'an': 'j', 'uai': 'k', 'ing': 'k', 'uang': 'l', 'iang': 'l',
        'ou': 'z', 'ua': 'x', 'ia': 'x', 'ao': 'c',
        'ui': 'v', 'in': 'b', 'iao': 'n', 'ian': 'm'}
# 零声母转换表
ulpb3 = {'a': 'aa', 'e': 'ee', 'o': 'oo', 'ang': 'ah', 'eng': 'eg'}


# 将汉字转换成双拼
def ulpb(key, quanpin):
    if len(key) == 1:               # 单字
        matcher = re.search(pattern_pinyin, quanpin)
        lt1 = [matcher.group(1) if matcher.group(1) != None else '']
        lt2 = [matcher.group(2)]
    else:                           # 词语
        # https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict
        lt1 = lazy_pinyin(key, style=Style.INITIALS, strict=False)        # 取声母
        lt2 = lazy_pinyin(key, style=Style.FINALS, strict=False)          # 取韵母

    for i in range(len(key)):
        if len(lt1[i]) > 0:         # 有声母
            try:
                value += ulpb1.get(lt1[i], lt1[i]) + ulpb2.get(lt2[i], lt2[i])
            except:
                value = ulpb1.get(lt1[i], lt1[i]) + ulpb2.get(lt2[i], lt2[i])
        else:                       # 无声母
            value = value + ulpb3.get(lt2[i], lt2[i]) if 'value' in dir() else ulpb3.get(lt2[i], lt2[i])
    return value



# 匹配一条记录，把其中的汉字（group(2)）、辅码（group(3)）和拼音取出来（group(4)）
regex_line = r"^(\$ddcmd\((.+?),.+?(?:\\\\2|_)([a-z]).+?\)\s+)(\w+)$"
pattern_line = re.compile(regex_line)

# 匹配声母和韵母
regex_pinyin = (r"(zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?"
        r"(iang|ang|eng|iong|ing|ong|uang|uai|uan|iao|ian"
        r"|iu|ei|ue|un|uo|ie|ai|en|an|ou|ua|ia|ao|ui|in|[aoeiuv])")
pattern_pinyin = re.compile(regex_pinyin)

lines_seen = set()

with open(sys.argv[1], 'r', encoding='utf-8-sig') as f1:                 # 输入文件
    with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f2:   # 输出文件
        for line in f1:                                                  # 逐行处理
            matcher = re.search(pattern_line, line)
            if matcher != None:                   # 匹配
                outputstr = matcher.group(1) + ulpb(matcher.group(2), matcher.group(4))
                outputstr += '\n' + outputstr + matcher.group(3) + '\n'
            else:                                 # 不匹配
                outputstr = line
            if outputstr not in lines_seen:       # 去除重复行
                f2.write(outputstr)
                lines_seen.add(outputstr)

