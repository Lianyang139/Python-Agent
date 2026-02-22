import csv

# 原始数据（模拟从字符串读取）
data_str = """source,info
黑马程序员,Python是世界上最好的编程语言
传智教育,股票代码003032
黑马程序员,LangChain极大地方便了大模型开发
黑马程序员,AI和Python是下一个十年的风口
传智教育,Python学起来很简单的
黑马程序员,学习Python键盘敲烂月薪过万
黑马程序员,努力带来成就，Python助力辉煌
黑马程序员,学习Python的时候也要记得好好休息打打篮球
黑马程序员,明天晚上吃啥子呀
黑马程序员,如何快速减肥呢"""

# 将字符串按行分割
lines = data_str.strip().split('\n')

# 解析为列表的列表（每行一个列表）
rows = [line.split(',', 1) for line in lines]  # split(..., 1) 防止 info 中有逗号被误切

# 写入 CSV 文件
with open('info.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("CSV 文件已保存为 info.csv")