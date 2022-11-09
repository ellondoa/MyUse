import datetime
from pytz import timezone
import requests
import re
from google_drive_downloader import GoogleDriveDownloader as gdd

headers = {
    'referer': 'https://www.sfzy888.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36 '

}

def get_new_article(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    urls = re.findall(r"<a class='read-more-btn' href='(.*)'>完整阅读<\/a>", response.text)
    print(urls)
    return urls


def get_gdid(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    ids = re.findall(r'<a href="https://drive.google.com/file/d/([\w-]*)/view"', resp.text)
    print(ids)
    return ids


if __name__ == '__main__':
    # https://www.sfzy888.com/search/label/免费节点
    url = 'https://www.sfzy888.com/search/label/%E5%85%8D%E8%B4%B9%E8%8A%82%E7%82%B9'
    urls = get_new_article(url)
    print(urls)
    ids = get_gdid(urls[1])
    if ids:
        gdd.download_file_from_google_drive(file_id=ids[0],
                                            dest_path='./WebSite/{}.yaml'.format(datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')),
                                            showsize=True, overwrite=True)

        gdd.download_file_from_google_drive(file_id=ids[0],dest_path='./newYaml/newestWB.yaml',showsize=True, overwrite=True)
        print("网站爬取成功")
        # requests.get('https://api.day.app/3TKmw24emfnWtLN6xyDaW9/网站爬取成功{}'.format(
        #     datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')))
    else:
        print("网站爬取失败")
        # requests.get('https://api.day.app/3TKmw24emfnWtLN6xyDaW9/网站爬取失败'.format(
        #     datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')))
