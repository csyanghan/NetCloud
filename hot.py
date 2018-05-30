import os, re, requests, json
import pandas as pd
url = 'http://api.map.baidu.com/geocoder/v2/'
ak = 'xK1KEl5txXo2cYSsaI5vDoMQZRynNgHq'

def mapclassify(s):
    pattern = '-\s(.*)市'
    pattern1 = '(.*)市'
    pattern2 = '-\s(.*)州'
    city = re.search(pattern, s)
    if city:
        return city.group(1)
    else:
        city = re.search(pattern1, s)
        if city:
            return city.group(1)
        else:
            city = re.search(pattern1, s)
            if city:
                return city.group(1)
            else:
                return ''

def load_userInfo_csv():
    userInfo_path = os.path.join('raw_data', 'userInfo.csv')
    userInfo_df = pd.read_csv(userInfo_path, encoding='utf-8-sig')
    return userInfo_df

def map():
    user_region = load_userInfo_csv().dropna(subset=['region'])
    classify = pd.Series([mapclassify(s) for s in user_region.region])
    user_region['classify'] = classify
    user_region = user_region.groupby('classify').size()
    array = user_region.index.values
    array2 = user_region.values
    data = []
    for i in range(1, 295):
        params = {
            'address': array[i],
            'output': 'json',
            'ak': ak
        }
        res = requests.get(url, params)
        res = json.loads(res.text)
        lng = res['result']['location']['lng']
        lat = res['result']['location']['lat']
        item = {
            "lng": lng,
            "lat": lat,
            "count": array2[i]
        }
        data.append(item)

    print(data)

map()