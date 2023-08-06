# dingTalk Python SDK
# Documentation: https://open.dingtalk.com/document/robots/custom-robot-access

import json

import requests

class sendMessage():
    def __init__(self, webhook: str) -> None:
        """
        :param webhook: The webhook URL of the DingTalk robot
        :param type: Message type: text | link | markdown | actionCard | feedCard
        """

        self.headers = requests.utils.default_headers()
        self.headers.update(
            {
                "Content-Type": "application/json",
            })
        self.webhook = webhook

    def text(self, content: str, atMobiles: list=[], atUserIds: list=[], isAtAll: bool=False)->str:
        """
        :param content: What you want to send
        :param atMobiles: The list of mobile phone number of members in the dingtalk group
        :param atMobiles: The list of userID of members in the dingtalk group
        :param isAtAll: True or False; If True —— atMobiles & atMobiles will be invalid
        """

        self.formData = {
            "at": {
                "atMobiles": atMobiles,
                "atUserIds": atUserIds,
                "isAtAll": isAtAll
            },
            "text": {
                "content": content
            },
            "msgtype": "text"
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res

    def link(self, content: str, title: str, messageUrl: str, picUrl: str="")->str:
        """
        :param content: Message content. If it is too long it will only be displayed partially. 
        :param title: Message title
        :param messageUrl: Click the URL to jump to the web page. Default: use DingTalk client to open it, For other cases, please refer to https://open.dingtalk.com/document/app/message-link-description?spm=ding_open_doc.document.0.0.1d1c722fhyOfxl#section-7w8-4c2-9az
        :param picUrl: The URL of picture
        """
        self.formData = {
            "msgtype": "link",
            "link": {
                "text": content,
                "title": title,
                "picUrl": picUrl,
                "messageUrl": messageUrl
            }
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res

    def markdown(self, content: str, title: str, atMobiles: list=[], atUserIds: list=[], isAtAll: bool=False)->str:
        """
        :param content: Message content. Type: Markdown
        :param title: Message title
        :param atMobiles: The list of mobile phone number of members in the dingtalk group
        :param atMobiles: The list of userID of members in the dingtalk group
        :param isAtAll: True or False; If True —— atMobiles & atMobiles will be invalid
        """
        self.formData = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content,
            },
            "at": {
                "atMobiles": atMobiles,
                "atUserIds": atUserIds,
                "isAtAll": isAtAll
            }
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res

    def integralActionCard(self, content: str, title: str, singleTitle: str, singleURL: str, btnOrientation: int=0)->str:
        """
        :param content: Message content. Type: Markdown
        :param title: Message title
        :param singleTitle: The title of the single button. Notice: After setting this and singleURL, btns is invalid.
        :param singleURL: Click the message to jump to the URL 
        :param btnOrientation: 0: Buttons are arranged vertically; 1: Buttons arranged horizontally
        """
        self.formData = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": content,
                "singleTitle": singleTitle,
                "singleURL": singleURL,
                "btnOrientation": btnOrientation
            }
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res

    def independentActionCard(self, content: str, title: str, btns: list, btnOrientation: int=0)->str:
        """
        :param content: Message content. Type: Markdown
        :param title: Message title
        :param btns: [{"title": "button title", "actionURL": "URL triggered by button click"}, ...]
        :param btnOrientation: 0: Buttons are arranged vertically; 1: Buttons arranged horizontally
        """
        self.formData = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": content,
                "btns": btns,
                "btnOrientation": btnOrientation
            }
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res

    def feedCard(self, links: list)->str:
        """
        :param links: [{"title": "", "messageURL": "", "picURL": ""}, ...]
        """
        self.formData = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": links
            }
        }
        self.formData = json.dumps(self.formData, ensure_ascii=False).encode("utf-8")
        res = requests.post(url=self.webhook, data=self.formData, headers=self.headers)
        return res