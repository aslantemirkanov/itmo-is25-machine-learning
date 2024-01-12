import csv
import time
import pandas as pd

import requests
from tqdm import tqdm


def send_request(url, params):
    while True:
        try:
            response = requests.get(url=url, params=params)
            time.sleep(1)
            if response.status_code == 200 and 'error' not in response.json():
                return response.json()

        except Exception:

            print('Ошибка при выполнении запроса')
            time.sleep(1)


def get_posts(count, offset):
    params = {
        'access_token': access_token,
        'owner_id': group_id,
        'filter': 'owner',
        'count': count,
        'offset': offset,
        'v': '5.131'
    }
    url = domain + "wall.get?"

    return send_request(url, params)


def get_count_posts(req_json):
    return req_json['response']['count']


def get_posts_id(req_json):
    return [x['id'] for x in req_json['response']['items']]


def get_comments(count, offset, post_id):
    params = {
        'access_token': access_token,
        'owner_id': group_id,
        'post_id': post_id,
        'count': count,
        'offset': offset,
        'extended': 1,
        'v': '5.131'
    }
    url = domain + "wall.getComments?"

    return send_request(url, params)


def get_count_comments(req_json):
    return req_json['response']['current_level_count']


def get_comments_data(req_json):
    return [x for x in req_json['response']['items'] if "deleted" not in x and x["from_id"] >= 0]


def save_csv(data):
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(data)


domain = "https://api.vk.com/method/"
# я удалил свой токен, но вы можете добавить свой
access_token = ''
group_id = 43189072
max_count = 100
csv_file = "dellin_vk_com.csv"

count_posts = get_count_posts(get_posts(1, 0))

posts_id = []

cur_offset = 0

pbar = tqdm('count posts ids received', total=count_posts)
while len(posts_id) < count_posts:
    cur_ids = get_posts_id(get_posts(max_count, cur_offset))
    posts_id = posts_id + cur_ids
    pbar.update(len(cur_ids))
    cur_offset += max_count

pbar.close()

for i in tqdm(range(len(posts_id)), desc='posts parsed'):
    cur_offset = 0
    count_comments = get_count_comments(get_comments(1, 0, posts_id[i]))
    cur_count = 0

    while cur_count < count_comments:
        cur_comments = get_comments(max_count, cur_offset, posts_id[i])
        cur_comments_data = get_comments_data(cur_comments)

        for comment in cur_comments_data:
            text = comment['text']
            save_csv([text])
        cur_offset += max_count
        cur_count += max_count
    pbar.close()
pbar.close()

file_path = 'dellin_vk_com.csv'
df = pd.read_csv(file_path, delimiter=";")
comments_df = df.iloc[:, 1]
comments_df.head()

comments_df = comments_df.rename("Comment")
output_file_path = 'dataset.csv'
comments_df.to_csv(output_file_path, index=False)
