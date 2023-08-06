"""
Advertising processing file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import os
import random
from typing import Union
from .yyds import ToolClass, Api, AiHandler
import requests
import shutil
import time


class Ocr(Api):
    def __init__(self):
        self.__ocr_result = list()
        self.__text = dict()

    def run_ocr(self):
        """ocr 文字识别"""
        ocr_result = []
        ret = self.api('/screen-ocr')
        if ret:
            ocr_list_str = ret.split('\n')
            for line in ocr_list_str:
                if line.strip():
                    prob, text, pos_split = line.split('\t')
                    pos_split = pos_split.split(" ")
                    x1, y1 = pos_split[0].split(",")
                    x2, y2 = pos_split[1].split(",")
                    x3, y3 = pos_split[2].split(",")
                    x = (float(x2) - float(x1)) / 2 + float(x1)
                    y = (float(y3) - float(y1)) / 2 + float(y1)
                    ocr_result.append({"prob": prob, "text": text, "x": int(x), "y": int(y)})
        # print(ocr_result)
        self.__ocr_result = ocr_result

    def find_text(self, text: str, option: dict = None):
        res = dict()
        arr_res = text.split(".")
        text_len = len(arr_res)
        for i in self.__ocr_result:
            if text_len == 3:
                if arr_res[1] in i["text"]:
                    res = i
                    break
            elif text_len == 2:
                if arr_res[0] == "*":
                    if i["text"].endswith(arr_res[1]):
                        res = i
                        break
                elif arr_res[1] == "*":
                    if i["text"].startswith(arr_res[0]):
                        res = i
                        break
            else:
                if i["text"] == arr_res[0]:
                    res = i
                    break

        if option and res:
            region = option["region"]
            x1 = region[0]
            y1 = region[1]
            if len(region) == 4:
                x2 = x1 + region[2]
                y2 = y1 + region[3]
            else:
                x2 = 10000
                y2 = 10000
            if not (x1 < res["x"] < x2 and y1 < res["y"] < y2):
                res = dict()

        self.__text = res
        return self

    def click(self):
        if self.__text:
            res = self.__text
            self.api("/touch", {"x": res["x"], "y": res["y"]})
        self.__text = dict()
        return self

    def swipe(self, x1: Union[str, int, float], y1: Union[str, int, float],
              x2: Union[str, int, float], y2: Union[str, int, float],
              duration: Union[str, int]):
        """滑动"""
        self.api("/swipe", ({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2), "duration": int(duration)}))
        return self

    def sleep(self, delay: float):
        """延迟阻塞"""
        time.sleep(float(delay))
        return self

    def fn(self, fun):
        fun()
        return self

    def exists(self):
        return bool(self.__text)

    def get_result(self):
        return self.__text


class FindImages(Api):
    def __init__(self):
        self.data = list()
        self.save_data = list()
        self.__img_results = list()
        self.__img_res = dict()

    def __parse_data(self, path: str, save_path: str, data: dict):
        new_data = list()
        save_data = list()
        for value in data.values():
            for nd_value in value.values():
                new_data.append(path + nd_value["name"])
                save_data.append(save_path + nd_value["name"])
        self.data = new_data
        self.save_data = save_data

    def save_images(self, url: str, path: str, save_path: str, data: dict):
        self.__parse_data(path, save_path, data)
        p = ""
        for i in save_path.split('/'):
            if i:
                p += i
                if not os.path.exists(p):
                    os.mkdir(p)
                p += "/"

        for i in self.data:
            # print(url + i.split("/")[-1])
            res = requests.get(url + i.split("/")[-1], stream=True)
            with open(i, "wb") as f:
                res.raw.decode_content = True
                shutil.copyfileobj(res.raw, f)

    def run_find_images(self):
        img_result = list()
        templates = ""
        for img in self.data:
            templates += img + ";"
        templates = templates[:-1]
        result = self.api("/screen-find-images", {"templates": templates})
        result = result.split("\n")
        # print(result)
        for i in result:
            if not i:
                continue
            path, params = i.split("\t")
            name = path.split("/")[-1]
            prob, wh, point = params.split()
            width, height = wh.split(",")
            x, y = point.split(",")
            img_result.append({
                "name": name,
                "prob": float(prob),
                "width": float(width),
                "height": float(height),
                "x": float(x),
                "y": float(y)
            })
        self.__img_results = img_result

    def find_img(self, name_dict: dict, option: dict = None):
        res = dict()
        for i in self.__img_results:
            for j in name_dict.values():
                if i["name"] == j["name"]:
                    if not option:
                        if i["prob"] > 0.9:
                            res = i
                    elif option["region"] == 2:
                        if i["x"] > option["region"][0] and \
                                i["y"] > option["region"][1] and \
                                i["prob"] > option["prob"]:
                            res = i
                    elif option["region"] == 4:
                        if i["x"] > option["region"][0] and \
                                i["x"] + i["width"] > option["region"][0] + option["region"][2] and \
                                i["y"] > option["region"][1] and \
                                i["y"] + i["height"] > option["region"][1] + option["height"][3] and \
                                i["prob"] > option["prob"]:
                            res = i
        self.__img_res = res
        return self

    def click(self):
        if self.__img_res:
            res = self.__img_res
            self.api("/touch", {"x": int(res["x"]), "y": int(res["y"])})
        self.__img_res = dict()
        return self

    def swipe(self, x1: Union[str, int, float], y1: Union[str, int, float],
              x2: Union[str, int, float], y2: Union[str, int, float],
              duration: Union[str, int]):
        """滑动"""
        self.api("/swipe", ({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2), "duration": int(duration)}))
        return self

    def sleep(self, delay: float):
        """延迟阻塞"""
        time.sleep(float(delay))
        return self

    def fn(self, fun):
        fun()
        return self

    def exists(self):
        return bool(self.__img_res)

    def get_result(self):
        res = self.__img_res
        self.__img_res = dict()
        return res


class AdHandler:
    def __init__(self, project_name: str):
        self.__project_name = project_name
        self.__images_url = "http://114.107.236.224:9963/wagjzwwl/images/ad-"
        self.__images_path = "/sdcard/yyds.py/" + self.__project_name + "/ad/images/"
        self.__images_save_path = "ad/images/"
        self.__tool = ToolClass()
        self.__ai = AiHandler()
        self.__ocr = Ocr()
        self.__find_images = FindImages()
        self.__device_width = self.__tool.device_width
        self.__device_height = self.__tool.device_height
        self.__close_delay = [1, 5]
        self.__options = {
            "close": {
                "region": [self.__device_width * 0.05, 0,
                           self.__device_width * 0.95, self.__device_height * 0.3],
                "prob": 0.68
            },
            "small_close": {
                "region": [self.__device_width * 0.5, self.__device_height * 0.1,
                           self.__device_width * 0.5, self.__device_height * 0.4],
                "prob": 0.7
            },
            "eye": {
                "region": [0, self.__device_height * 0.3,
                           self.__device_width, self.__device_height * 0.4],
                "prob": 0.7
            },
            "blessing_get": {
                "region": [0, 0,
                           self.__device_width, self.__device_height * 0.3],
                "prob": 0.75
            },
            "appDetails": {
                "region": [self.__device_width * 0.2, self.__device_height * 0.3,
                           self.__device_width * 0.6, self.__device_height * 0.5],
                "prob": 0.6
            },
            "抓住奖励机会": {
                "region": [self.__device_width * 0.5, self.__device_height * 0.45,
                           self.__device_width * 0.4, self.__device_height * 0.25],
                "prob": 0.6
            },
            "拒绝": {
                "region": [0, self.__device_height * 0.5,
                           self.__device_width * 0.6, self.__device_height * 0.49],
                "prob": 0.5
            },
            "cancel": {
                "region": [self.__device_width * 0.4, self.__device_height * 0.3,
                           self.__device_width * 0.59, self.__device_height * 0.4],
                "prob": 0.7
            },
            "download": {
                "region": [self.__device_width * 0.2, 0,
                           self.__device_width * 0.8, self.__device_height],
                "prob": 0.8
            },
            "lockBagInstall": {
                "region": [0, self.__device_height * 0.6],
                "prob": 0.6
            },
            "accept": {
                "region": [0, self.__device_height * 0.75,
                           self.__device_width, self.__device_height * 0.25],
                "prob": 0.6
            },
            "look_again": {
                "region": [self.__device_width * 0.3, self.__device_height * 0.45,
                           self.__device_width * 0.4, self.__device_height * 0.3],
                "prob": 0.7
            },
            "baidu_logo": {
                "region": [self.__device_width * 0.85, self.__device_height * 0.85],
                "prob": 0.7
            },
            "jump": {
                "region": [self.__device_width * 0.75, 0,
                           self.__device_width * 0.25, self.__device_height * 0.3],
                "prob": 0.7
            },
            "pause": {
                "region": [self.__device_width * 0.3, 0,
                           self.__device_width * 0.4, self.__device_height * 0.7],
                "prob": 0.7
            },
            "blackBaidu": {
                "region": [0, self.__device_height * 0.5,
                           self.__device_width, self.__device_height * 0.5],
                "prob": 0.7
            },
            "get": {
                "region": [0, 100,
                           self.__device_width * 0.3, self.__device_height * 0.4],
                "prob": 0.75
            },
        }
        self.__images_data = {
            "close": {
                "close_1": {"name": "whiteClose.png", "option": self.__options["close"]},
                "close_2": {"name": "Close.png", "option": self.__options["close"]},
                "close_3": {"name": "Close1.png", "option": self.__options["close"]},
                "close_4": {"name": "Close2.png", "option": self.__options["close"]},
                "close_5": {"name": "Close11.png", "option": self.__options["close"]},
                "close_6": {"name": "blackClose.png", "option": self.__options["close"]},
            },
            "small_close": {
                "small_close_1": {"name": "smallClose.png", "option": self.__options["small_close"]},
                "small_close_2": {"name": "smallClose3.png", "option": self.__options["small_close"]},
                "small_close_3": {"name": "smallClose4.png", "option": self.__options["small_close"]},
                "small_close_4": {"name": "smallClose5.png", "option": self.__options["small_close"]},
                "small_close_5": {"name": "smallClose8.png", "option": self.__options["small_close"]},
                "small_close_6": {"name": "smallClose9.png", "option": self.__options["small_close"]},
            },
            "jump": {
                "jump_1": {"name": "jump1.png", "option": self.__options["jump"]},
                "jump_2": {"name": "jump2.png", "option": self.__options["jump"]},
                "jump_3": {"name": "jump3.png", "option": self.__options["jump"]},
                "jump_4": {"name": "jump4.png", "option": self.__options["jump"]},
                "jump_5": {"name": "jump7.png", "option": self.__options["jump"]}

            },
            "baidu_logo": {
                "baidu_logo_1": {"name": "baiduLogo1.png", "option": self.__options["baidu_logo"]},
                "baidu_logo_2": {"name": "baiduLogo2.png", "option": self.__options["baidu_logo"]},
                "baidu_logo_3": {"name": "baiduLogo3.png", "option": self.__options["baidu_logo"]},
                "baidu_logo_4": {"name": "baiduLogo4.png", "option": self.__options["baidu_logo"]}
            },
            "blessing_get": {
                "blessing_get_1": {"name": "blessingGet1.png", "option": self.__options["blessing_get"]},
                "blessing_get_2": {"name": "blessingGet2.png", "option": self.__options["blessing_get"]},
                "blessing_get_3": {"name": "blessingGet3.png", "option": self.__options["blessing_get"]}
            },
            "look_again": {
                "look_again_1": {"name": "lookAgain1.png", "option": self.__options["look_again"]},
                "look_again_2": {"name": "lookAgain2.png", "option": self.__options["look_again"]},
            },
            "get": {
                "get_1": {"name": "get1.png", "option": self.__options["get"]},
                "get_2": {"name": "get2.png", "option": self.__options["get"]},
            },
            "get_reward": {
                "get_reward_1": {"name": "getJL1.png", "option": self.__options["get"]},
                "get_reward_2": {"name": "getJL2.png", "option": self.__options["get"]},
            }
        }
        self.__point = dict()
        self.__get_point = dict()
        self.__jump_date = 0
        self.__find_images.save_images(self.__images_url, self.__images_path, self.__images_save_path,
                                       self.__images_data)

    def __full_screen_ocr(self):
        self.__ocr.run_ocr()
        if self.__ocr.find_text("*.立即获取.*", {"region": [790, 0, self.__device_width - 790, 200]}).exists():
            return True
        if self.__ocr.find_text("*.免费获取.*", {"region": [790, 0, self.__device_width - 790, 200]}).exists():
            return True
        if self.__ocr.find_text("*.后领取.*").exists():
            self.__tool.sleep(1).swipe(self.__device_width - random.randint(300, 700),
                                       self.__device_height - random.randint(300, 500),
                                       self.__device_width - random.randint(300, 700), random.randint(300, 500), 1)
            return True
        if self.__ocr.find_text("浏览页面25s领取奖励").exists():
            for _ in range(2):
                self.__tool.sleep(1).swipe(self.__device_width - random.randint(300, 700),
                                           self.__device_height - random.randint(300, 500),
                                           self.__device_width - random.randint(300, 700), random.randint(300, 500),
                                           1000)
            return True
        if self.__ocr.find_text("恭喜获得奖励").exists():
            return True
        if self.__ocr.find_text("奖励已领取").exists():
            self.__get_point = self.__ocr.get_result()
        if self.__ocr.find_text("不感兴趣").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("放弃下载").exists():
            # print(self.__ocr.get_result())
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("继续观看").exists():
            self.__tool.sleep(1).click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            for _ in range(5):
                self.__tool.swipe(self.__device_width * 0.5, self.__device_height * 0.8, self.__device_width * 0.5,
                                  self.__device_height * 0.2, 500).sleep(0.5)
                self.__tool.swipe(self.__device_width * 0.5, self.__device_height * 0.2, self.__device_width * 0.5,
                                  self.__device_height * 0.8, 500).sleep(0.5)
            return True
        if self.__ocr.find_text("拒绝").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("取消").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("禁止").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("残忍离开").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("抓住奖励机会").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("应用详情").exists():
            self.__tool.back()
            return True
        if self.__ocr.find_text("权限列表").exists():
            self.__tool.back()
            return True
        if self.__ocr.find_text("跳过"):
            if self.__tool.foreground()["currentPackageName"] == \
                    "com.bytedance.sdk.openadsdk.stub.activity.Stub_Standard_Portrait_Activity":
                if self.__jump_date - self.__jump_date > 30:
                    self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
                    return True
                else:
                    self.__jump_date = time.time()
            else:
                self.__jump_date = 0

    def __full_screen(self):
        self.__find_images.run_find_images()
        self.__ai.run_ai()
        # 百度
        if self.__find_images.find_img(self.__images_data["blessing_get"], self.__options["blessing_get"]).exists():
            if self.__find_images.get_result()["x"] > self.__device_width * 0.5:
                return True
            elif self.__find_images.get_result()["x"] < self.__device_width * 0.5:
                self.__ai.sleep(random.randint(self.__close_delay[0], self.__close_delay[0])).click("close",
                                                                                                    self.__options[
                                                                                                        "close"])
                return True
        if self.__find_images.find_img(self.__images_data["baidu_logo"], self.__options["baidu_logo"]).exists():
            if self.__point.get("text") == "跳过":
                self.__tool.sleep(random.randint(self.__close_delay[0], self.__close_delay[0])).click(self.__point["x"],
                                                                                                      self.__point["y"])
                return True
            elif self.__find_images.find_img(self.__images_data["jump"], self.__options["close"]).exists():
                self.__tool.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click(
                    self.__find_images.get_result()["x"], self.__find_images.get_result()["y"])
                return True
        # 穿山甲
        if self.__ai.exists("interact_look", self.__options["eye"]):
            for _ in range(2):
                self.__tool.sleep(1).swipe(self.__device_width - random.randint(300, 700),
                                           self.__device_height - random.randint(300, 500),
                                           self.__device_width - random.randint(300, 700), random.randint(300, 500),
                                           1000)
            return True
        # 再看一次
        if self.__find_images.find_img(self.__images_data["look_again"], self.__options["look_again"]).exists():
            self.__tool.click(self.__find_images.get_result()["x"], self.__find_images.get_result()["y"])
            return True
        # 关闭
        if self.__ai.exists("close", self.__options["close"]):
            self.__ai.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click("close",
                                                                                                self.__options["close"])
            return True
        if self.__find_images.find_img(self.__images_data["close"], self.__options["close"]).exists():
            self.__tool.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click(
                self.__find_images.get_result()["x"], self.__find_images.get_result()["y"])
            return True
        # 穿山甲10秒
        if self.__find_images.find_img(self.__images_data["get"], self.__options["get"]).exists():
            self.__tool.sleep(1).swipe(self.__device_width - random.randint(300, 700),
                                       self.__device_height - random.randint(300, 500),
                                       self.__device_width - random.randint(300, 700), random.randint(300, 500), 1000)
            return True
        if self.__find_images.find_img(self.__images_data["get_reward"], self.__options["get"]).exists() or \
                self.__get_point.get("text") == "奖励已领取":
            if self.__point.get("text") == "跳过":
                self.__tool.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click(self.__point["x"],
                                                                                                      self.__point["y"])
                return True
            elif self.__ai.exists("jump", self.__options["close"]):
                self.__ai.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click("jump",
                                                                                                    self.__options[
                                                                                                        "close"])
                return True
            elif self.__find_images.find_img(self.__images_data["jump"], self.__options["jump"]).exists():
                self.__tool.sleep(random.randint(self.__close_delay[0], self.__close_delay[1])).click(
                    self.__find_images.get_result()["x"], self.__find_images.get_result()["y"])
                return True
        # 广告验证
        if self.__ai.exists("interact_select"):
            a = self.__ai.find_name("interact_select")
            self.__tool.sleep(1).click(float(a["cx"]), float(a["cy"]) - 50)
            return True
        if self.__ai.exists("interact_swipe"):
            a = self.__ai.find_name("interact_swipe")
            self.__tool.sleep(1).swipe(float(a["x"]) + 100, a["cx"], float(a["x"]) + float(a["w"]) - 100, a["cy"], 500)
            return True

    def __half_screen_ocr(self):
        self.__ocr.run_ocr()
        if self.__ocr.find_text("*.获得奖励.*").exists():
            return True
        if self.__ocr.find_text("允许").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("取消").exists():
            self.__tool.click(self.__ocr.get_result()["x"], self.__ocr.get_result()["y"])
            return True
        if self.__ocr.find_text("应用详情").exists():
            self.__tool.back()
            return True
        if self.__ocr.find_text("权限列表").exists():
            self.__tool.back()
            return True

    def __half_screen_ai(self):
        self.__ai.run_ai()
        self.__ai.click("close", self.__options["small_close"])
        self.__ai.click("jump", self.__options["small_close"])

    def full_screen_ad(self):
        if self.__full_screen_ocr():
            return
        if self.__full_screen():
            return

    def half_screen_ad(self):
        if self.__half_screen_ocr():
            return
        if self.__half_screen_ai():
            return
