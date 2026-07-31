import base64
import os

# 手动粘贴节点，换行分隔
node_list = """
vless://xxx
vmess://xxx
trojan://xxx
"""

def run():
    content = node_list.strip()
    os.makedirs("sub", exist_ok=True)
    # 明文文件
    with open("sub/txt.txt", "w", encoding="utf-8") as f:
        f.write(content)
    # base64订阅文件
    b64_str = base64.b64encode(content.encode("utf-8")).decode()
    with open("sub/b64.txt", "w", encoding="utf-8") as f:
        f.write(b64_str)
    print("本地文件生成完成")

if __name__ == "__main__":
    run()
