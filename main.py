import requests
import os

# ========== 1、粘贴你的所有节点，一行一条 ==========
node_list = """
vless://xxx
vmess://xxx
trojan://xxx
"""

def convert_to_clash_yaml(raw_links: str) -> str:
    """调用公开订阅转换接口，转为Clash配置"""
    api_url = "https://sub.xfxb.net/api/sub"
    params = {
        "target": "clashmeta",
        "url": raw_links,
        "config": "https://cdn.jsdelivr.net/gh/CareyWang/sub-web/configs/clashmeta.ini"
    }
    try:
        resp = requests.get(api_url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print("转换失败：", e)
        return ""

if __name__ == "__main__":
    # 清理换行空格
    clean_nodes = node_list.strip()
    # 转换
    clash_config = convert_to_clash_yaml(clean_nodes)

    # 写入文件到仓库根目录 clash.yaml
    os.makedirs("output", exist_ok=True)
    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(clash_config)

    print("✅ 已生成 clash.yaml Clash 专用配置文件")
