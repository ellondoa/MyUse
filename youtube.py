import datetime

import requests
import re
from google_drive_downloader import GoogleDriveDownloader as gdd
from pytz import timezone

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'YSC=FZAqgHLfdCM; CONSENT=YES+cb.20210420-15-p1.zh-CN+FX+732; GPS=1; VISITOR_INFO1_LIVE=v2aixc6NJXI; PREF=tz=Asia.Shanghai',
    'referer': 'https://www.youtube.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'x-client-data': 'CI+2yQEIpLbJAQjEtskBCKmdygEIlqzKAQiIucoBCPjHygEI1uvKAQjjnMsBCKmdywEI6J3LAQigoMsBGOGaywE='

}

#爬取到视频主页，获取视频的播放ID
def getIDs(url,headers):
    response = requests.get(url, headers=headers, timeout=None, verify=False)
    response.encoding = 'utf-8'
    print(response.status_code)
    ids = re.findall(r"(/watch\?v=.+?)\042",response.text)
    return ids

#获取视频播放页的详情
def getSfzy(url, headers):
    web = 'https://www.sfzy888.com/2021/08/2185clash-clash.html'
    response = requests.get(url, headers=headers, timeout=None, verify=False)
    response.encoding = 'utf-8'
    #print(response.text)
    #file_ids = re.findall(r"https://www.sfzy888.com/(.*)",response.text)
    file_ids = re.findall(r"去这里获取免费节点：https://www.sfzy888.com/(.*),?",response.text)
    #html = etree.HTML(response.text)
    #file_ids = html.xpath('//div[@id="description-inner"][1][2]//a/@href')
    print("getSfzy:")
    # for i in file_ids:
    #   print(i)
    return web
    # print(file_ids[0])

def get_ggid(url):
    resp = requests.get(url, headers=headers)
    ids = re.findall(r'<a href="https://drive.google.com/(.*)" target="_blank">', resp.text)
    print("get_ggid():")
    node_url = ids[0].split('=')[2].split('"')[0]
    print(node_url)
    return node_url

if __name__ == '__main__':
    url = 'https://www.youtube.com/channel/UCOQ5AdvDNOfyEAJY5SDXVZg/videos'
    # print('https://www.youtube.com'+getIDs(url,headers)[0][:-2])
    ids = getIDs(url, headers)
    #获取最新一期的播放地址
    video_url = "https://www.youtube.com"+ids[0]
    nodeUrl = getSfzy(video_url, headers)
    googleDrive_ids = get_ggid(nodeUrl)
    if googleDrive_ids:
        gdd.download_file_from_google_drive(file_id=googleDrive_ids,
                                            dest_path='./YT/{}.yaml'.format(datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')),
                                            showsize=True, overwrite=True)
        gdd.download_file_from_google_drive(file_id=googleDrive_ids,
                                            dest_path='./newYaml/newestYT.yaml',showsize=True, overwrite=True)
        # requests.get("https://api.day.app/3TKmw24emfnWtLN6xyDaW9/YouTube节点爬取成功{}".format(datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')))
    else:
        print("YouTube节点爬取失败")
        # requests.get("https://api.day.app/3TKmw24emfnWtLN6xyDaW9/YouTube节点爬取失败{}".format(
        #     datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')))
    # downYaml(url,headers)
    # print("down")
