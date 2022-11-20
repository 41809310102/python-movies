import time

from dao.Movie import Movie
from mapper import movieMapper

movice = []


# 加载爬取的网站数据
def read_file():
    with open("../../service/moviesky.txt", "r", encoding="utf-8") as f:  # 打开文件
        line = f.readline()  # 调用文件的 readline()方法，一次读取一行
        while line:
            res = eval(str(line))
            movice.append(res)
            line = f.readline()
        f.close()


# 将爬好的数据封装传到数据库中进行管理
def get_insert_data():
    read_file()
    type_list = ['喜剧', '爱情', '剧情', '惊悚', '动作', '奇幻', '战争', '动画', '冒险']
    for obj in movice:
        count = 1
        for type in type_list:
            if str(obj['type']).find(type)!=-1:
                node = Movie()
                node.setMovie_type(count)
                node.setMovie_title(obj['title'])
                node.setMovie_uptime(obj['up_year'])
                node.setMovie_douban(get_douban_grade(obj['douban_grade']))
                node.setMovie_country(obj['create_local'])
                node.setMovie_time_total(get_time_long(obj['time_total']))
                movieMapper.add_Movie(node)
                count = 1
                time.sleep(2)
                break
            else:
                count += 1


# # 获取类别编号
# def get_type_id(data):
#     type_list = ['喜剧', '爱情', '剧情', '惊悚', '动作', '奇幻', '战争', '动画', '冒险']
#     count = 1
#     for k in type_list:
#         if str(data).find(k)


# 获取豆瓣分数
def get_douban_grade(douban):
    data = str(douban)
    start = data.find('.') - 1
    end = start + 3
    grade = data[start:end]
    return grade


# 获取时长
def get_time_long(time_data):
    datas = str(time_data)
    time_long = 0
    if datas.find('片') != -1:
        end = str(datas).find('分')
        start = str(datas).find('长') + 2
        try:
            time_long = int(datas[start:end])
        except:
            time_long = 90  # 筛选错误，默认为90
    else:
        time_long = 90
    return time_long


if __name__ == '__main__':
    get_insert_data()
