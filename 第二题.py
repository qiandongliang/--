import re
from datetime import datetime


def reg_search(text, regex_dict):
    results = {}
    for key, regex in regex_dict.items():
        pattern = re.compile(regex)
        matches = pattern.findall(text)

        # 如果matches中的日期是xxxx年xx月xx日的格式，将其转换为xxxx-xx-xx的格式
        formatted_matches = []
        for match in matches:
            if isinstance(match, tuple):
                # 处理多个日期的情况
                formatted_match = []
                for date in match:
                    if '年' in date and '月' in date and '日' in date:
                        formatted_date = datetime.strptime(date, '%Y年%m月%d日').strftime('%Y-%m-%d')
                        formatted_match.append(formatted_date)
                    else:
                        formatted_match.append(date)
                formatted_matches.append(tuple(formatted_match))
            else:
                if '年' in match and '月' in match and '日' in match:
                    formatted_date = datetime.strptime(match, '%Y年%m月%d日').strftime('%Y-%m-%d')
                    formatted_matches.append(formatted_date)
                else:
                    formatted_matches.append(match)

        results[key] = formatted_matches
    return results


# 示例输入
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束之日满12个月后的第一个交易日起至可交换债券到期日止，即2023年6月2日至2027年6月1日止。
'''

regex_dict = {
    '标的证券': r'股票代码：(\d+\.SH)',
    '换股期限': r'(\d{4}年\d{1,2}月\d{1,2}日)至(\d{4}年\d{1,2}月\d{1,2}日)'
}

# 调用函数
results = reg_search(text, regex_dict)

# 格式化结果
formatted_results = {
    '标的证券': results['标的证券'][0] if results['标的证券'] else None,
    '换股期限': results['换股期限'][0] if results['换股期限'] else None
}

# 打印结果
print(formatted_results)
