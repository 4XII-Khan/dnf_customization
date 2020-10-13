import urllib.request
from bs4 import BeautifulSoup
import pandas
from collections import defaultdict


def load_execl(file_path_str, sheet_name_str):
    """
    加载 execl
    :param file_path_str:  相对、绝对路径
    :param sheet_name_str:  sheet页名称
    :param column_list: 列名
    :return:
    """
    base_sheet = pandas.read_excel(file_path_str, sheet_name=sheet_name_str)
    if len(base_sheet) != 0:
        num = base_sheet.count()[0]
        sheet_row = base_sheet.loc[:]
        sheet_row_dicts = sheet_row.to_dict()
        to_excel_dict = {}
        for index in range(0,num):
            _to_excel = {}
            _key = ""
            for row_name in base_sheet.keys():
                _to_excel[row_name] = sheet_row_dicts[row_name][index]
                if row_name not in ["时间","购买链接"]:
                    _key += str(sheet_row_dicts[row_name][index])
            to_excel_dict[_key] = _to_excel
        return to_excel_dict
    else:
        return {}

def align(text, length = 25):
    blank = length - len(str(text))
    if blank < 0:
        return text
    else:
        return str(text) + " "*blank

def gold_list(ratio,new_time):
    url = "https://search.7881.com/list.html?pageNum=1&gameId=G10&gtid=100001&carrierId=0&groupId=G10P009&serverId=G10P009001&mobileGameType=&faceId=&tradeType=&tradePlace=0&shopSortTypeCode=1&sortType=default&listSearchKeyWord=&mainSearchKeyWord=&minPrice=&maxPrice=&otherFilterValue=&rentalByHourStart=&rentalByHourEnd=&propertiess=&chiledPropertiess=&platformId=&platformName=&order=&loginMethod=&rGameId=&tagValue=&priceTag=&instock=false&quickChoose="
    response = urllib.request.urlopen(url)
    #创建一个BeautifulSoup解析对象
    html_doc = response.read()
    # print(html_doc)
    soup = BeautifulSoup(html_doc,"lxml")
    # print(soup)
    h5_title = [item.text for item in soup.find_all(['h5']) if  item.text and item.text != '立即购买' ]
    h5_buy = [str(item).split("(")[1].split(")")[0].split(",") for item in soup.find_all(name='a',class_="list-btn") if   item.text == '立即购买']

    gold_title = [float(item.text.split("万金")[0].split("】")[1]) for item in soup.find_all(['span']) if  item.text and "=" in item.text ]
    span_title = [item.text for item in soup.find_all(['span']) if  item.text and "=" in item.text ]

    rate = []
    gold = []
    for i in range(len(h5_title)):
        if i % 2 == 0 :
            rate.append(h5_title[i].split()[1])
        else:
            gold.append(float(h5_title[i].split()[3]))
    gold_dict = defaultdict(dict)
    for index in range(len(gold)):
        _gold = gold[index]
        if _gold >= ratio:
            _key = span_title[index] + str(int(_gold)) + str(rate[index]) + str(gold_title[index])
            gold_dict[_key]["时间"] = new_time
            gold_dict[_key]["产品名称"] = span_title[index]
            gold_dict[_key]["收购比例"] = _gold
            gold_dict[_key]["收购金额RMB"] = rate[index]
            gold_dict[_key]["收购金币数量"] = gold_title[index]
            gold_dict[_key]["购买链接"] = "https://trade.7881.com/trade-{0}.html?pernum={1}&price={2}&random=0.8852590712885373".format(h5_buy[index][0],h5_buy[index][1],h5_buy[index][2])

            log = "商品名称：{0}, 收购比例：{1}万金币/元,  收购金额RMB：{2}元, 收购金币：{3}万金币, 购买链接：{4}".format(align(span_title[index],24),
                                                                                         align(str(_gold),6),
                                                                                         align(str(rate[index]),8),
                                                                                         align(str(gold_title[index]),7),
                                                                                         align(str(gold_dict[_key]["购买链接"]),140))

            if ratio + 2 > _gold >= ratio + 1:
                print("{0}[1;36;1m{1}{2}[0m".format(chr(27), log, chr(27)))
                continue
            elif _gold >= ratio + 2:
                print("{0}[1;35;1m{1}{2}[0m".format(chr(27), log, chr(27)))
                continue
            else:
                print("{0}[1;32;1m{1}{2}[0m".format(chr(27), log, chr(27)))

        if index >= 2:
            break

    print("{0}[1;33;1m{1}{2}[0m".format(chr(27), "="*220, chr(27)))
    return dict(gold_dict)

if __name__ == "__main__":
    import time
    _gold_dict = defaultdict(dict)
    gold_threshold = 68
    num = 0
    gold_header = ["时间","产品名称","收购比例","收购金额RMB","收购金币数量","购买链接"]
    excel_path = "金币涨跌追踪.xlsx"
    sheet_name = "金币跌涨追踪记录"

    while True:
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("{0}[33;1m{1}{2}[0m".format(chr(27), "="*74 + "【时间】：{0}, 【跨区】：{1}, 【金币比例阈值】:{2}0,000金币/元 ".format(new_time,"跨六",gold_threshold) + "="*74, chr(27)) )

        gold_dict = gold_list(gold_threshold, new_time)

        for _k, _v in gold_dict.items():
            _gold_dict[_k] = _v
        # 每2秒缓存一次数据
        if num % 10 == 0:
            # 加载历史数据
            history_excel = load_execl(excel_path, sheet_name)
            # 更新新增数据
            for _k, _v in _gold_dict.items():
                history_excel[_k] = _v
            # 构造excel数据结构
            to_execl_list = []
            for md5, content in history_excel.items():
                to_execl_list.append([content["时间"], content["产品名称"], content["收购比例"], content["收购金额RMB"], content["收购金币数量"],content["购买链接"]])

            df = pandas.DataFrame(to_execl_list)
            # 写excel
            writer = pandas.ExcelWriter(excel_path)
            df.to_excel(writer, sheet_name=sheet_name, header=gold_header, index=False, startrow=0,startcol=0)
            writer.save()

            print("{0}[1;34;1m{1}{2}[0m".format(chr(27), "已将当前数据缓存至《历史金币涨跌轨迹追溯表.xlsx》, 缓存数据数量：（新增缓存：{0},历史缓存：{1}）".format(len(_gold_dict.keys()),len(to_execl_list)), chr(27)))
            # 初始化新增缓存数据
            _gold_dict = defaultdict(dict)
        num += 1
        time.sleep(60)

