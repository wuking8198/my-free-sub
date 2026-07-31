import requests
import os

# 在这里粘贴你真实节点，一行一个
node_list = """
vless://xxx
vmess://xxx
trojan://xxx
"""

def convert_clash(raw_text):
    api = "https://sub.xfxb.net/api/sub"
    param = {
        "target": "clashmeta",
        "url": raw_text,
        "config": "https://cdn.jsdelivr.net/gh/CareyWang/sub-web/configs/clashmeta.ini"
    }
    try:
        res = requests.get(api, params=param, timeout=20)
        res.raise_for_status()
        return res.text
    except Exception as err:
        print("转换失败:", err)
        return "# 转换接口异常\nmixed-port: 7890\nallow-lan: true\nmode: rule\nrules:\n  - MATCH,DIRECT"

if __name__ == "__main__":
    content = node_list.strip()
    clash_data = convert_clash(content)

    # 写入根目录clash.yaml
    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(clash_data)
    print("clash.yaml 生成完毕")
