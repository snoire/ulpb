#! /usr/bin/python3

import sys
from pypinyin import lazy_pinyin, Style

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

# https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict
lt1 = lazy_pinyin(sys.argv[1], style=style1, strict=False)
lt2 = lazy_pinyin(sys.argv[1], style=style2, strict=False)

for i in range(len(sys.argv[1])):
    if len(lt1[i]) > 0:
        print('{}'.format(ulpb1.get(lt1[i], lt1[i])), end='')
        print('{}'.format(ulpb2.get(lt2[i], lt2[i])), end='')
    else:
        print('{}'.format(ulpb3.get(lt2[i], lt2[i])), end='')

print()

