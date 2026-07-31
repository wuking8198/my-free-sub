import requests
import re
import os

# ===================== 已填好公开抓取源，直接使用 =====================
SUB_URLS = [
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub10.txt",
    "https://proxypool.link/vmess/sub",
    "https://proxypool.link/trojan/sub"
]

# 双转换接口兜底，防止单个挂掉
API_LIST = [
    "https://sub.xfxb.net/api/sub",
    "https://api.subconvert.top/api/sub"
]
# ======================================================================

def fetch_raw_nodes() -> str:
    all_links = set()
    link_pattern = re.compile(r"(vless|vmess|trojan)://[^\s\n\r]+")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

    for url in SUB_URLS:
        try:
            resp = requests.get(url, timeout=15, headers=headers)
            resp.raise_for_status()
            matches = link_pattern.finditer(resp.text)
            for match in matches:
                all_links.add(match.group())
        except Exception as e:
            print(f"源 {url} 抓取失败: {e}")
            continue

    return "\n".join(sorted(list(all_links)))

def convert_to_clash(raw_links: str) -> str:
    params = {
        "target": "clashmeta",
        "url": raw_links,
        "config": "https://cdn.jsdelivr.net/gh/CareyWang/sub-web/configs/clashmeta.ini"
    }
    for api in API_LIST:
        try:
            res = requests.get(api, params=params, timeout=20)
            if res.status_code == 200 and len(res.text.strip()) > 300:
                return res.text
        except Exception:
            continue

    # 全部接口失效兜底配置
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
    print("开始抓取公开节点...")
    node_content = fetch_raw_nodes()
    count = len(node_content.splitlines()) if node_content else 0
    print(f"本次共抓取到 {count} 条有效节点")

    print("开始转换为Clash Meta配置...")
    clash_config = convert_to_clash(node_content)

    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(clash_config)

    print("✅ 执行完成，clash.yaml 已生成")
