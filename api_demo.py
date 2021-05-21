import time
import json
import hashlib
import string
import random
import requests

# 线上文档：https://openapi.wul.ai/docs/latest/saas.openapi.v2/openapi.v2.html#operation/GetBotResponse

HOST = 'https://openapi.wul.ai'
PUBKEY = "XXX"
SECRET = "XXX"

CHAR_LIST = []
[[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
[[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
[[CHAR_LIST.append(e) for e in string.digits] for i in range(0, 2)]


def get_chars(length):
    random.shuffle(CHAR_LIST)
    return "".join(CHAR_LIST[0:length])


def get_headers():
    secret = SECRET
    pubkey = PUBKEY
    # 秒级别时间戳
    timestamp = str(int(time.time()))
    nonce = get_chars(32)
    sign = hashlib.sha1(
        (nonce + timestamp + secret).encode("utf-8")).hexdigest()
    data = {
        "pubkey": pubkey,
        "sign": sign,
        "nonce": nonce,
        "timestamp": timestamp
    }
    headers = {}
    for k, v in data.items():
        headers["Api-Auth-" + k] = v
    return headers


def send_request(url, data):
    resp = requests.post(url=url, json=data, headers=get_headers())
    result = resp.json()
    return result


def create_user(user_id, nickname, imgurl: str = ''):
    """
    创建用户
    """
    data = {"user_id": user_id, "avatar_url": imgurl, "nickname": nickname}
    url = HOST + "/v2/user/create"
    return send_request(url, data)


def get_bot_response(user_id, content, extra: str = ''):
    """
    获取机器人回复
    """
    data = {
        "msg_body": {
            "text": {
                "content": content,
            },
        },
        "user_id": user_id,
        "extra": ""
    }
    url = HOST + "/v2/msg/bot-response"
    return send_request(url, data)


def msg_sync():
    """
    同步用户发的消息
    """
    data = {
        "user_id": "string",
        "extra": "string",
        "bot": {
            "qa": {
                "knowledge_id": 0,
                "standard_question": "string",
                "question": "string",
                "is_none_intention": True
            }
        },
        "msg_ts": "string",
        "msg_body": {
            "text": {
                "content": "测试文本消息"
            }
        },
        "answer_id": 0
    }
    url = HOST + "/v2/msg/sync"
    return send_request(url, data)


if __name__ == "__main__":
    user_id = 'testuserid'  # 用户唯一标识, 接入方保证唯一, 不超过64字节.
    nickname = 'testnickname'  # 用户昵称
    msg_content = '文本内容'  # 用户话术
    res = create_user(user_id, nickname)
    # res = get_bot_response(user_id, msg_content)
    # res = msg_sync()
    res = json.dumps(res, ensure_ascii=False)
    print(res)
