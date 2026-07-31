import requests
import base64
import re
import os
import json
import urllib.parse
import subprocess
from concurrent.futures import ThreadPoolExecutor

# 替换为可用公共订阅源（定期更新，可用性更高）
SUBSCRIBE_URLS = [
    "https://raw.fastgit.org/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.fastgit.org/awesome-v2ray/v2ray-subscribe/main/sub",
    "https://v2cross.com/subscribe/v2ray"
]

def extract_server(node):
    try:
        if node.startswith("vmess://"):
            b64 = node[8:].strip() + '=' * (-len(node[8:].strip()) % 4)
            config = json.loads(base64.b64decode(b64).decode('utf-8', errors='ignore'))
            return config.get("add")
        elif node.startswith("vless://") or node.startswith("trojan://"):
            return urllib.parse.urlparse(node).netloc.split('@')[-1].split(':')[0]
    except:
        return None

def test_node(node):
    server = extract_server(node)
    if not server:
        return None
    try:
        # GitHub Actions Linux 环境 ping 检测存活
        res = subprocess.run(['ping', '-c', '1', '-w', '2', server],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            return node
    except:
        pass
    return None

def run():
    all_nodes = []
    for url in SUBSCRIBE_URLS:
        try:
            res = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }, timeout=15)
            if res.status_code != 200:
                continue
            text = res.text.strip()
            # 尝试base64解码订阅内容
            try:
                text += '=' * (-len(text) % 4)
                text = base64.b64decode(text).decode('utf-8', errors='ignore')
            except Exception:
                pass
            # 正则匹配三种节点链接
            nodes = re.findall(r'(vless://[^\s\"\'\<]+|vmess://[^\s\"\'\<]+|trojan://[^\s\"\'\<]+)', text)
            all_nodes.extend(nodes)
        except Exception as e:
            continue

    # 去重
    unique_nodes = list(set(all_nodes))
    alive_nodes = []

    # 并发测速存活检测
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(test_node, unique_nodes)
        for r in results:
            if r:
                alive_nodes.append(r)

    # 创建文件夹并写入文件
    os.makedirs("sub", exist_ok=True)
    content_plain = "\n".join(alive_nodes)
    # 明文txt
    with open("sub/txt.txt", "w", encoding="utf-8") as f:
        f.write(content_plain)
    # base64编码订阅
    b64_content = base64.b64encode(content_plain.encode('utf-8')).decode('utf-8')
    with open("sub/b64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"✅ 抓取完成：总量{len(unique_nodes)}，存活可用{len(alive_nodes)}")

if __name__ == "__main__":
    run()
