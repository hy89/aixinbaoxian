import re

import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
# }
# resp = requests.get('http://m.axbxw.com/case.php?p=100&proid=1&t=moreagent', headers=headers)
# print(type(resp.content.decode('gbk')))

# with open('地区.html', 'wb') as f:
#     f.write(resp.content)


# p = re.compile(r'.*sf(\d+).*')
# ret = p.search('/agent/sf12-cs77-gs')
# print(ret.group(1))

# a = '北京'
# b = '河南(全部)'
# a = a.replace('(全部)', '')
# b = b.replace('(全部)', '')
# print(a)
# print(b)
# h3 = '高凤霄 业务主任'
# name, position = h3.split(' ')
# print(name)

# city = '保定'
# a, b = city.split(' ', maxsplit=1)
# print(a)
# print(b)

a = '资格证号：'
a = '资格证号：00201203410100003018'
a = '资格证号：null'
print(a.split('：'))

b = 'http://m.axbxw.com/'
print(len(b))