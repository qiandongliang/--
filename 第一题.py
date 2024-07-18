import requests
import pandas as pd


def fetch_bond_data(page_no):
    url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"

    data = {
        'pageNo': page_no,
        'pageSize': 15,
        'isin': '',
        'bondCode': '',
        'issueEnty': '',
        'bondType': '100001',
        'couponType': '',
        'issueYear': 2023,
        'rtngShrt': '',
        'bondSpclPrjctVrty': ''
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "iftp.chinamoney.com.cn",
        "Origin": "https://iftp.chinamoney.com.cn",
        "Referer": "https://iftp.chinamoney.com.cn/english/bdInfo/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def main():
    page_no = 1
    all_results = []

    while True:
        result = fetch_bond_data(page_no)
        print(result)
        all_results.extend(result['data']['resultList'])
        page_no += 1

        if page_no > result['data']['pageTotal']:
            break

    # 只保留需要的列
    columns = ['isin', 'bondCode', 'entyFullName', 'bondType', 'issueStartDate', 'issueEndDate','debtRtng']
    filtered_results = [{col: item[col] for col in columns} for item in all_results]

    # 保存到CSV
    save_to_csv(filtered_results, 'bond_data.csv')


if __name__ == "__main__":
    main()
