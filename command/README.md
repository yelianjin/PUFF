在文件夹下查询所有包含ACK的文件，具体见 blog.csdn.net/wu8439512/article/details/78642800
grep -rn "ACK" *
stanfordcorenlp使用
以conll格式输出
./corenlp.sh -annotators tokenize,ssplit,pos,lemma,ner -ssplit.eolonly -outputFormat conll -file 76w.txt.s
stanfordcorenlp使用--split-eolonly 应对换行句子问题
https://stackoverflow.com/questions/28337548/ssplit-eolonly-with-chinese-text
pip下不了的包
1.git clone https://github.com/xx.git
2.cd
python setup.py install
stanfordcorenlp java使用 将句子类型的input.txt 转化为 input.txt.conll,input.txt.conll以'\t'分隔
./corenlp.sh -annotators tokenize,ssplit,pos,lemma,ner -outputFormat conll -file input.txt
删除文件内包含line2 的一行
sed -i '/line2/d' example.txt
文件分隔符
awk -f '\t'  '{print $2,$4,$5}' example.txt >example1.txt 输入分隔符为 '\t'
awk -v OFS='\t' '{print $2,$4,$5}' example.txt >example1.txt 输出分隔符为'\t'
Python字符串操作
str.isalnum()判断str是否为字母和数字组成,返回true/false
str.islalpha()判读str是否为纯字母组成，返回true/false
str.isdigit()判断str是否为纯数字组成，返回true/false
str.islower()判断str是否为纯小写字母组成，返回true/false
str.isnumeric() str=u'123'转为unicode后判断str是否为纯数字组成，返回true/false,可以做汉字"四"
https://www.runoob.com/python/att-string-isnumeric.html
str.isspace()判断str是否为纯空格组成，返回true/false
str.istitle()判断str是否为Apllo，首字母大写，其余字母小写，返回true/false
str.isupper()判断str是否为大写，返回true/false
Tencent只能使用80/8080端口，所有要执行网页浏览器交互的都要走这个端口
查看端口被占用情况
netstat  -anp  |grep   端口号
Shell 写循环例子
SERVICES="80   22   25   110   8000   23   20   21   3306   " 
for   x   in   $SERVICES     
do      
  iptables   -A   INPUT   -p   tcp   --dport   $x   -m   state   --state   NEW   -j   ACCEPT      
done 
vim中 段落复制粘贴
复制粘贴段开始处 按v 进入可视模式
y进行复制
p进行粘贴
find pathname -options
寻找目录下所有.tags文件 合成 result.txt
find ./ -name "*.tags" | xargs -i cat {} > result.txt  /data/jackljye/
寻找目录下所有.tags文件 并复制至/data/jackljye/下
find ./ -name "*.tags" | xargs -i cp {} /data/jackljye/
统计example.txt 第一列中各项出现的次数
awk -F '\t' '{sum[$1]++}END{for(i in sum) print i "\t" sum[i]}' example.txt
统计当前目录下文件的个数（不包括目录）
ls -l | grep "^-" | wc -l
统计当前目录下文件的个数（包括子目录）
ls -lR| grep "^-" | wc -l
查看某目录下文件夹(目录)的个数（包括子目录）
ls -lR | grep "^d" | wc -l
vim /寻找的项 切换下一项 n 切换上一项N
按照文件名的顺序进行排序
ls | xargs stat -c "%n" | sort -n
ls -t 以修改时间排序（最新的在最前面）
ls -r 已修改时间排序（最晚的在最后面）
Pyhton后台启动
nohup python -u server.py params1 > nohup.out 2>&1 &
Spyder命令
分段执行cell
# %% cell 1
# %% cell 2
右击run cell 或Cntrl+Enter执行cell
常用Linux指令
cat XX.txt 从末行看文件
tac XX.txt 从首行看文件
head -n 10 XX.txt 看文件的前10行
tail -n 10 XX.txt 看文件的后10行

删掉XX.txt的最后一行
sed -i '$d' XX.txt

杀死node进程
ps -ef | grep node | grep -v grep | awk '{print $2}' | xargs kill -9

查找XX文件
find /-name XX.xx 


Python异常处理
try:
    function()
except:
    function()执行失败，走except

Python反复执行直到失败
while(1):
    try:
        function()
        break
    except:
        function()

Python反复执行(有上限)
count_while=0
while(1):
    try:
        function()
        count_while+=1
        break
    except:
        if(count_while满足终止条件):
            break
if(count_while满足终止条件):
    continue

Python 十六进制转化问题
https://blog.csdn.net/wen_1108/article/details/78274709

a = 'i am request,\xE6\x88\x91\xE6\x98\xAF\xE8\xAF\xB7\xE6\xB1\x82'.decode('utf-8').encode('utf-8')
print a

Git 用法
全局化git 的user

git config --global user.name  "jackljye"
git config --global user.email "jackljye@tencent.com"


本地已有项目要推到git上去

cd existing_folder
git init
git remote add origin http://git.code.oa.com/jackljye/excited.git
git add .
git commit
git push -u origin master

本地的项目修改后 要更新

git pull origin master
git add *
git commit -m 'xx'
git push