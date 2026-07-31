import requests
import os

# 填入你的节点
node_list = """
vless://xxx
vmess://xxx
trojan://xxx
"""

def get_clash_config(raw_links):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "target": "clashmeta",
        "url": raw_links.strip(),
        "config": "https://cdn.jsdelivr.net/gh/CareyWang/sub-web/configs/clashmeta.ini"
    }
    # 备用接口列表，一个挂了自动换
    api_list = [
        "https://sub.xfxb.net/api/sub",
        "https://api.subconvert.top/api/sub"
    ]
    for api in api_list:
        try:
            res = requests.get(api, params=params, headers=headers, timeout=10)
            if res.status_code == 200 and len(res.text) > 100:
                return res.text
        except Exception:
            continue
    # 所有接口都失败，返回兜底可用空配置
    return """mixed-port: 7890
allow-lan: true
mode: rule
log-level: info
external-controller: 127.0.0.1:9090
proxies: []
rules:
  - MATCH,DIRECT
"""

if __name__ == "__main__":
    yaml_content = get_clash_config(node_list)
    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print("✅ clash.yaml 写入完成")
