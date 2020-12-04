#! /bin/zsh

if ((# != 2)) {
    print -u2 "Usage: $0 <inputfile> <outputfile>"
    return 1
}

INPUTFILE=$1
OUTPUTFILE=$2
EXEC='./ulpb.py'


# 进度条
float count_bar=1.0
total_lines=$(wc -l $INPUTFILE)
total_lines=${total_lines[(w)1]}
width=$(stty size)                      #获取屏幕宽度
width=${width[(w)2]}                    #取第二个数字（宽度）
width=$((width-16))                     #除了#号，还要预留几个位置给其他字符

progress_sign=""
printfmt="[%-"$((width*7/8))"s] %6d %6.2f%% %c\r"  #这样写就可以自适应了
arry=("\\" "\\" "|" "|" "/" "/" "-" "-")           #4个太快了，换成8个，\\是转义


count=0
>$OUTPUTFILE </dev/null                 # 清空文件

for i (${(f)"$(<$INPUTFILE)"}) {        # 逐行处理
    str=${i//}                        # 删掉 \r 字符

    if [[ $i =~ '^\$ddcmd\(.*,.*\)[[:space:]]' ]] {   # 以 $ddcmd 这种格式开头，正则匹配
        target=${str#*\(}                             # 删掉 '（' 左边内容
        target=${target%%,*}                          # 删掉 '，' 右边内容，取出要转换的汉字
        target=$($EXEC $target)                       # 调用 python 程序获取转换后的结果

        [[ $outputstr != "" ]] && outputstr+='\n'
        outputstr+=${(q)${str%\)*}}')\t'$target       # 删掉 ')' 及之后的内容，为字符串中的特殊符号添加转义符号，再加上 ')' 和结果
        (( count++ ))

        if (( count > 255 )) {                        # 多行字符串一次性写入，提高效率
            print $outputstr >> $OUTPUTFILE
            outputstr=""
            count=0
        }
    } else {                           # 否则不进行转换，原样输出
        echo $str >> $OUTPUTFILE
    }

    # 打印进度条
    (( index=count_bar%8 ))
    printf $printfmt "$progress_sign" $count_bar "$((count_bar*100/total_lines))" "${arry[$index]}"
    # 每隔多少个，进度条增加一
    if (( count_bar%(total_lines/(width*7/8)) == 0 )) {
        progress_sign+="#"
    }
    (( count_bar++ ))
}
printf "\n"

[[ $outputstr != "" ]] && print $outputstr >> $OUTPUTFILE
sed -i '1s/^\xEF\xBB\xBF//' $OUTPUTFILE               # 删除 utf-8 的 BOM
print "Done."

