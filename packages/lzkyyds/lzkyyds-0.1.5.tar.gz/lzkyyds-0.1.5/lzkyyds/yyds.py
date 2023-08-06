"""
一个人失败的最大原因，就是对于自己的能力永远不敢充分信任，甚至自己认为必将失败无疑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import random
import shutil
import time
import requests
import os
import re
from typing import Union
from wjtool import ExportHandle as yydsExt
from java.util import HashMap


class Api:
    def api(self, uri: str, options=None):
        if options is None:
            options = {}
        params = HashMap()
        if options:
            for key in options.keys():
                params.put(key, str(options[key]))
        for _ in range(3):
            # noinspection PyBroadException
            try:
                res = yydsExt.http(uri, params)
                return res
            except Exception:
                print("插件错误，正在重试！")
                self.sleep(5)

    @staticmethod
    def sleep(delay: float):
        time.sleep(float(delay))

    @staticmethod
    def upload_err(name: str, msg: str):
        res = requests.post("http://114.107.236.224:9963/upload/err", {"name": name, "msg": msg})
        if res.status_code == 200:
            print("upload error msg success")
        else:
            print("upload error msg failed")


class ToolClass(Api):
    """
    Plug in extension processing class
    """

    def __init__(self):
        self.device_width: float = 0
        self.device_height: float = 0
        self.__get_screen_size()

    def __get_screen_size(self):
        res = self.api("/shell", {"cmd": "dumpsys window displays | grep init"})
        res = res.lstrip().split(" ")[0].split("=")[1].split("x")
        self.device_width = int(float(res[0]))
        self.device_height = int(float(res[1]))

    def version(self):
        """插件版本号"""
        return self.api("/version")

    def toast(self, content: str):
        """信息提示"""
        self.api("/toast", {"content": content})
        return self

    def click(self, x: Union[int, float], y: Union[int, float]):
        """点击"""
        self.api("/touch", {"x": int(x), "y": int(y)})
        return self

    def swipe(self, x1: Union[int, float],
              y1: Union[int, float],
              x2: Union[int, float],
              y2: Union[int, float],
              duration: Union[int, float]):
        """滑动"""
        self.api("/swipe", ({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2), "duration": int(duration)}))
        return self

    def back(self):
        """返回键"""
        self.api('/shell', {"cmd": "input keyevent 4"})
        return self

    def home(self):
        """home键"""
        self.api('/shell', {"cmd": "input keyevent 3"})
        return self

    def input_keyevent(self, key: Union[str, int]):
        """自定义input keyevent key"""
        self.api('/shell', {"cmd": f"input keyevent {key}"})
        return self

    def sleep(self, delay: float):
        """延迟"""
        super().sleep(delay)
        return self

    def paste(self, text: str):
        """粘贴"""
        self.api("/paste", {"text": text})
        return self

    def screenshot(self):
        """截图"""
        return self.api('/screenshot')

    def foreground(self):
        """当前信息"""
        result = self.api('/foreground')
        current_package_name = ""
        current_activity = ""
        pid = ""
        if result:
            current_package_name, current_activity, pid = result.split(" ")
        return {
            "currentPackageName": current_package_name.strip(),
            "currentActivity": current_activity.strip(),
            "pid": pid.strip(),
        }

    def is_net_online(self):
        return self.api("/is-net-online") == 'true'

    def start_app(self, name: Union[str, list], img):
        self.home().sleep(2).home()
        num = 0
        while True:
            self.sleep(1)
            if num >= 6:
                break
            num += 1
            self.sleep(1)
            if img.click(name).is_click(5):
                break
            else:
                self.swipe(self.device_width * 0.85, self.device_height * 0.5, self.device_width * 0.2,
                           self.device_height * 0.5, 250)


class OcrHandler(Api):
    """
    ocr character recognition processing class
    """

    def __init__(self):
        self.__ocrResSet = []
        self.__oneList = []
        self.__isClick = False

    def __ocr(self) -> None:
        """ocr 文字识别"""
        ret = self.api('/screen-ocr')
        ocr_result = []
        if ret:
            ocr_list_str = ret.split('\n')
            for line in ocr_list_str:
                if line.strip():
                    prob, text, pos_split = line.split('\t')
                    pos_split = pos_split.split(" ")
                    x1, y1 = pos_split[0].split(",")
                    x2, y2 = pos_split[1].split(",")
                    x3, y3 = pos_split[2].split(",")
                    x4, y4 = pos_split[3].split(",")
                    ocr_result.append(
                        {"prob": prob, "text": text, "x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2),
                         "x3": int(x3),
                         "y3": int(y3), "x4": int(x4), "y4": int(y4)})
        self.__ocrResSet = ocr_result

    def __find_text(self, text):
        self.__ocr()
        res = None
        if self.__ocrResSet:
            if type(text).__name__ == 'list':
                for i in text:
                    arr_res = i.split(".")
                    text_len = len(arr_res)
                    for o in self.__ocrResSet:
                        if text_len == 3:
                            if arr_res[1] in o["text"]:
                                res = o
                                break
                        elif text_len == 2:
                            if arr_res[0] == "*":
                                if o["text"].endswith(arr_res[1]):
                                    res = o
                                    break
                            elif arr_res[1] == "*":
                                if o["text"].startswith(arr_res[0]):
                                    res = o
                                    break
                            else:
                                if o["text"] == arr_res[0]:
                                    res = o
                                    break
                    if res:
                        break
            else:
                arr_res = text.split(".")
                text_len = len(arr_res)
                for o in self.__ocrResSet:
                    if text_len == 3:
                        if arr_res[1] in o["text"]:
                            res = o
                            break
                    elif text_len == 2:
                        if arr_res[0] == "*":
                            if o["text"].endswith(arr_res[1]):
                                res = o
                                break
                        elif arr_res[1] == "*":
                            if o["text"].startswith(arr_res[0]):
                                res = o
                                break
                    else:
                        if o["text"] == arr_res[0]:
                            res = o
                            break
        return res

    def click(self, text, top=None, deviation=None):
        """
        找字并点击
        @param text: 要查找的文字，一个或多个，多个传列表，多个找到一个剩下会跳过
        @param top: 传入数字，过滤从 0 到 top 的文字
        @param deviation: 点击时偏移
        如果想知道有没有点击，调用点击后调用 is_click 属性 -> ocr.click(xx).is_click()
        """
        self.__isClick = False
        res = self.__find_text(text)
        if res:
            x1 = res["x1"]
            x2 = res["x2"]
            y1 = res["y1"]
            y3 = res["y3"]
            if not top or (top and y1 > top):
                x = (x2 - x1) / 2 + x1
                y = (y3 - y1) / 2 + y1
                if deviation:
                    x += deviation[0]
                    y += deviation[1]
                self.api("/touch", {"x": int(x), "y": int(y)})
                self.__isClick = True
        return self

    def one_click(self, text: str):
        """点击成功一次后，重复调用不会点击"""
        if text not in self.__oneList and self.click(text).__isClick:
            self.__oneList.append(text)
        return self

    def is_click(self, delay=None) -> bool:
        """
        获取上一次是否有触发点击
        如果传入数字，那么成功触发点击后会延迟 x 秒
        """
        if delay and self.__isClick:
            self.sleep(delay)
        tmp = self.__isClick
        self.__isClick = False
        return tmp

    def exists(self, text) -> bool:
        """文字存不存在"""
        res = self.__find_text(text)
        return bool(res)

    def sleep(self, delay: float):
        """延迟"""
        super().sleep(delay)
        return self


class ImageHandler(Api):
    """
    Mapping processing class
    图片完整参数
    "img_name": {
        "name": "xxx.jpg",
        "region"?: [x, y, w, h],
        "prob"?: 0~10,
        "deviation"?: [1, 2, [3, 4]], 两个参数为固定偏移x,y,四个参数为随机 random(1,2) 偏移x,random(3,4) 偏移y
        "ad"?: bool
    }
    """

    def __init__(self, img_list: dict, img_url: str, project_name: str):
        self.click_count: int = 0
        self.__project_name: str = project_name
        self.__isClick: bool = False
        # 图片字典
        self.__img_dict: dict = img_list
        # 图片下载地址
        self.__img_url: str = img_url
        # 保存到 Yyds.Py 下的
        self.__to_path: str = "img/"
        # 图片读取地址
        self.__img_path: str = "/sdcard/Yyds.Py/" + project_name + "/img/"
        self.__download_save_img()

    def __download_save_img(self):
        """保存图片"""
        p = ""
        for i in self.__to_path.split('/'):
            if i:
                p += i
                if not os.path.exists(p):
                    os.mkdir(p)
                p += "/"
        nomedia_path = self.__to_path + ".nomedia"
        if os.path.exists(nomedia_path):
            os.mkdir(nomedia_path)
        for v in self.__img_dict.values():
            res = requests.get(self.__img_url + v["name"], stream=True)
            if res.status_code == 200:
                with open(self.__to_path + v["name"], "wb") as f:
                    res.raw.decode_content = True
                    shutil.copyfileobj(res.raw, f)

    def __screen_find_images(self, templates):
        return self.api("/screen-find-images", {"templates": templates})

    def __img_filter(self, img_list):
        result = dict()
        for item in img_list:
            name = item["img_name"].split('.')[0]
            img_data = self.__img_dict[name]
            prob = img_data.get("prob", 0.9)
            if prob > item["prob"]:
                continue
            region = img_data.get("region")
            if region and (region[0] > item["x"] or
                           region[1] > item["y"] or
                           (region[0] + region[2]) < (item["x"] + item["width"]) or
                           (region[1] + region[3]) < (item["y"] + item["height"])):
                continue
            result[name] = item
        return result

    def __find_images(self, img_name):
        # noinspection PyBroadException
        try:
            templates: str = ""
            if type(img_name).__name__ == 'list':
                for img in img_name:
                    templates += self.__img_path + self.__img_dict[img]["name"] + ";"
                templates = templates[:-1]
            else:
                templates += self.__img_path + self.__img_dict[img_name]["name"]
            res = self.__screen_find_images(templates)
            result = dict()
            temp_list = list()
            if res:
                img_res_list = res.split('\n')
                for line in img_res_list:
                    if line:
                        line = line.split('\t')
                        img_path = line[0]
                        img_params = line[1]
                        name = img_path.split('/')[-1]
                        params = img_params.split()
                        prob = params[0]
                        wh = params[1]
                        point = params[2]
                        width, height = wh.split(',')
                        x, y = point.split(',')
                        temp_list.append({
                            "img_name": name,
                            "prob": float(prob),
                            "width": int(width),
                            "height": int(height),
                            "x": int(x),
                            "y": int(y)
                        })
                result_dict = self.__img_filter(temp_list)
                if type(img_name).__name__ == 'list':
                    for name in img_name:
                        result = result_dict.get(name, dict())
                        if result:
                            break
                else:
                    result = result_dict.get(img_name, dict())
            return result
        except Exception as e:
            self.upload_err(self.__project_name, "找图错误 --> " + str(e))
            exit()

    def click(self, img_name):
        self.__isClick = False
        res = self.__find_images(img_name)
        if res:
            x = res["x"]
            y = res["y"]
            _name = res["img_name"].split('.')[0]
            image_obj = self.__img_dict.get(_name)
            if image_obj.get("ad"):
                self.click_count += 1
            else:
                self.click_count = 0
            deviation = image_obj.get("deviation", [])
            deviation_len = len(deviation)
            if deviation and deviation_len == 2 or deviation_len == 4:
                if deviation_len == 2:
                    x += int(deviation[0])
                    y += int(deviation[1])
                elif deviation_len == 4:
                    x += random.randint(int(deviation[0]), int(deviation[1]))
                    y += random.randint(int(deviation[2]), int(deviation[3]))
            else:
                height = res["height"]
                width = res["width"]
                y += height * 0.25 + random.randint(int(height * 0.25), int(height * 0.75))
                x += width * 0.25 + random.randint(int(width * 0.25), int(width * 0.75))
            self.api("/touch", {"x": int(x), "y": int(y)})
            self.__isClick = True
        return self

    def is_click(self, delay: float = None) -> bool:
        """
        获取上一次是否有触发点击
        如果传入数字，那么成功触发点击后会延迟 x 秒
        """
        if delay and self.__isClick:
            self.sleep(delay)
        tmp = self.__isClick
        self.__isClick = False
        return tmp

    def exists(self, img_name) -> bool:
        res = self.__find_images(img_name)
        return bool(res)

    def sleep(self, delay: float):
        super().sleep(delay)
        return self


class ControlHandler(Api):

    def __init__(self):
        self.__isClick = False

    def __find_control(self, options: dict):
        res = self.api('/u2-match', options)
        ret = list()
        if res:
            line = res.split("\n")
            for i in line:
                l1, l2, l3 = i.split(" ")
                x1, y1 = l1.split(",")
                x2, y2 = l2.split(",")
                w, h = l3.split(",")
                ret.append({x1: float(x1), y1: float(y1), x2: float(x2), y2: float(y2), w: float(w), h: float(h)})
        return res

    def scann_control(self):
        """扫描xml文档，打印文档"""
        res = self.api('/u2-dump-hierarchy')
        print(res)

    def click(self, options: dict):
        self.__isClick = False
        result = self.__find_control(options)
        if result:
            x = result[0].w / 2 + result[0].x1
            y = result[0].h / 2 + result[0].y1
            self.api("/touch", {"x": int(x), "y": int(y)})
            self.__isClick = True
        return self

    def exists(self, options: dict) -> bool:
        res = self.__find_control(options)
        return bool(res)

    def is_click(self, delay: float = None) -> bool:
        """
        获取上一次是否有触发点击
        如果传入数字，那么成功触发点击后会延迟 x 秒
        """
        if delay and self.__isClick:
            self.sleep(delay)
        tmp = self.__isClick
        self.__isClick = False
        return tmp


class AiHandler(Api):
    def __init__(self, high_mode=True):
        self.__highMode = high_mode
        self.__isClick = False
        self.__aiResult = ""

    def __ai(self):
        return self.api("/key-locate", {"use_gpu": self.__highMode})

    def run_ai(self):
        self.__aiResult = self.__ai()

    def __ai_filter(self):
        res = self.__aiResult
        li = list()
        s = res.split("\n")
        for line in s:
            if not line:
                continue
            reg = re.compile(r"[{}',]")
            s = reg.sub("", line)
            result = dict()
            for i in s.split(" "):
                i = i.split("=")
                result.update({i[0]: i[1]})
            li.append(result)
        return li

    def find_name(self, name: str, option: dict = None):
        res = self.__ai_filter()
        for i in res:
            if i.get("label") == name:
                if not option:
                    return i
                else:
                    x1 = option["region"][0]
                    y1 = option["region"][1]
                    if len(option) == 4:
                        x2 = x1 + option["region"][2]
                        y2 = y1 + option["region"][3]
                    else:
                        x2 = 10000
                        y2 = 10000

                    if x1 < float(i["cx"]) < x2 and y1 < float(i["cy"]) < y2:
                        return i
        return {}

    def click(self, name: str, option: dict = None):
        self.__isClick = False
        res = self.find_name(name, option)
        if res:
            self.api("/touch", {"x": int(float(res["cx"])), "y": int(float(res["cy"]))})
            self.__isClick = True
        return self

    def is_click(self, delay=None) -> bool:
        """
        获取上一次是否有触发点击
        如果传入数字，那么成功触发点击后会延迟 x 秒
        """
        if delay and self.__isClick:
            self.sleep(delay)
        tmp = self.__isClick
        self.__isClick = False
        return tmp

    def exists(self, name: str, option: dict = None):
        res = self.find_name(name, option)
        return bool(res)

    def sleep(self, delay: float):
        super().sleep(delay)
        return self

    def swipe(self, x1: Union[str, int, float],
              y1: Union[str, int, float],
              x2: Union[str, int, float],
              y2: Union[str, int, float],
              duration: Union[str, int]):
        """滑动"""
        self.api("/swipe", ({"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2), "duration": int(duration)}))
        return self
