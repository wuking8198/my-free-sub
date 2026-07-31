import requests
import base64
import re
import os
import json
import urllib.parse
import subprocess
from concurrent.futures import ThreadPoolExecutor

# 内置全网更新最频繁的优质节点池
SUBSCRIBE_URLS = [
    "https://githubusercontent.com",
    "https://githubusercontent.com",
    "https://githubusercontent.com",
    "https://githubusercontent.com"
]

def extract_server(node):
    try:
        if node.startswith("vmess://"):
            b64 = node[8:].strip() + '=' * (-len(node[8:].strip()) % 4)
            config = json.loads(base64.b64decode(b64).decode('utf-8', errors='ignore'))
            return config.get("add")
        elif node.startswith("vless://") or node.startswith("trojan://"):
            return urllib.parse.urlparse(node).netloc.split('@')[-1].split(':')[0]
    except: return None

def test_node(node):
    server = extract_server(node)
    if not server: return None
    try:
        # 在 GitHub 的 Linux 环境下发送 1 个 ping 包，超时 2 秒
        res = subprocess.run(['ping', '-c', '1', '-w', '2', server], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0: return node
    except: pass
    return None

def run():
    all_nodes = []
    for url in SUBSCRIBE_URLS:
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if res.status_code != 200: continue
            text = res.text.strip()
            try:
                text += '=' * (-len(text) % 4)
                text = base64.b64decode(text).decode('utf-8', errors='ignore')
            except: pass
            nodes = re.findall(r'(vless://[^\s\"\'\<]+|vmess://[^\s\"\'\<]+|trojan://[^\s\"\'\<]+)', text)
            all_nodes.extend(nodes)
        except: pass
        
    unique_nodes = list(set(all_nodes))
    alive_nodes = []
    
    # GitHub 服务器性能强劲，直接拉满 50 线程并发测活
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(test_node, unique_nodes)
        for r in results:
            if r: alive_nodes.append(r)
            
    os.makedirs("sub", exist_ok=True)
    # 生成明文格式订阅（给手机 NekoBox、v2rayNG 剪贴板用）
    with open("sub/txt.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(alive_nodes))
    # 生成标准的 Base64 加密订阅（直接作为客户端自动更新链接）
    with open("sub/b64.txt", "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(alive_nodes).encode('utf-8')).decode('utf-8'))
        
    print(f"抓取完毕！共找到 {len(unique_nodes)} 个节点，测活存活 {len(alive_nodes)} 个。")

if __name__ == "__main__":
    run()
