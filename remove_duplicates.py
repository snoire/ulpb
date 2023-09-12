#! python3

import sys, os, re

if len(sys.argv) != 3:
    print("Usage: {} <inputfile> <outputfile>".format(sys.argv[0]), file=sys.stderr)
    os._exit(1)


# 匹配一条记录，把其中的拼音取出来（group(1)）
regex_line = r"^\$ddcmd\(.+?,.+?(?:\\\\2|_).+?\)\s+(\w+)$"
pattern_line = re.compile(regex_line)


data = ['---config', '---config']
with open(sys.argv[1], 'r', encoding='utf-8-sig') as f1:
    for i, line in enumerate(f1):
        if i < 2:
            continue
        matcher = re.search(pattern_line, line)
        data.append(matcher.group(1))

duplicate = True

with open(sys.argv[1], 'r', encoding='utf-8-sig') as f1:                 # 输入文件
    with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f2:   # 输出文件
        for i, line in enumerate(f1):
            if i % 2 != 0:
                # 如果拼音唯一，就不需要辅助码
                if duplicate:
                    f2.write(line)
                continue

            if data.count(data[i]) == 1:
                duplicate = False
            else:
                duplicate = True

            f2.write(line)
