import requests
import csv



def write_csv(data):
    with open('videos.csv', 'a', encoding='utf-8') as f:
        order = ['title', 'url']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'x-youtube-client-name': '1',
        'x-youtube-client-version': '2.20210128.02.00'
    }
    token_page = requests.get(url, headers=headers)
    nextDataToken = token_page.text.split('"nextContinuationData":{"continuation":"')[1].split('","')[0]
    sleep = False
    while not sleep:
        service = 'https://www.youtube.com/browse_ajax'
        params = {
            "ctoken": nextDataToken,
            "continuation": nextDataToken
        }
        r = requests.post(service, params=params, headers=headers)
        html = r.json()[1]
        html_json = html['response']
        html_jsonResponse = html_json['continuationContents']['gridContinuation']
        try:  # пробуем найти токен
            nextDataToken = html_jsonResponse["continuations"][0]["nextContinuationData"]["continuation"]
        except:
            # токен не найден. Значит, далее запроса не будет. Остается собрать оставшийся контент
            sleep = True

        for content in html_jsonResponse['items']:
            title = content['gridVideoRenderer']['title']['accessibility']['accessibilityData']['label']
            url = 'https://www.youtube.com/' + content['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']



            data = {'title': title, 'url': url}
            write_csv(data)







def main():
    url = 'https://www.youtube.com/c/MrMarmok/videos'
    print(get_html(url))


if __name__ == '__main__':
    main()