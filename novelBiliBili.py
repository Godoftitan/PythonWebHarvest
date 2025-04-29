import time
import random
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# —————— 配置 ——————
START_URL   = "https://www.linovelib.com/novel/4519/262012.html"
OUTPUT_FILE = "novel.txt"

# —————— 初始化 cloudscraper ——————
ua = UserAgent()
scraper = cloudscraper.create_scraper(browser={"custom": ua.random})

def safe_get(url, max_retries=5):
    """用 cloudscraper 安全获取页面，自动处理 Cloudflare 限制。"""
    for i in range(max_retries):
        resp = scraper.get(url, timeout=15)
        if resp.status_code == 200:
            return resp
        wait = 2 ** i
        print(f"[WARN] {url} 返回 {resp.status_code}, 等待 {wait}s 重试…")
        time.sleep(wait)
    raise RuntimeError(f"无法获取页面：{url}")

def download_full_novel(start_url, output_path):
    """从 start_url 开始，抓取每一页章节标题与正文，直至无“下一页”。"""
    url = start_url
    with open(output_path, "w", encoding="utf-8") as fw:
        while True:
            print(f"抓取：{url}")
            try:
                resp = safe_get(url)
            except Exception as e:
                print(f"[ERROR] 停止抓取，原因：{e}")
                break

            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "lxml")

            # 1) 定位章节主容器
            main = soup.find("div", id="mlfy_main_text")
            if not main:
                print(f"[ERROR] 未找到章节容器：{url}")
                break

            # 2) 提取并写入标题
            h1 = main.find("h1")
            if h1:
                title = h1.get_text(strip=True)
                fw.write(f"{title}\n\n")

            # 3) 提取正文段落
            content = main.find("div", id="TextContent", class_="read-content8")
            if not content:
                print(f"[ERROR] 未找到正文容器：{url}")
                break
            paras = []
            for p in content.find_all("p"):
                txt = p.get_text(strip=True)
                if txt:
                    paras.append(txt)
            fw.write("\n\n".join(paras))
            fw.write("\n\n" + "="*40 + "\n\n")

            # 4) 查找“下一页”链接
            nav = soup.find("div", class_="mlfy_page")
            nxt = nav and nav.find("a", string="下一页")
            if nxt and nxt.get("href"):
                next_url = urljoin(url, nxt["href"])
                if next_url == url:
                    break
                url = next_url
                time.sleep(random.uniform(5, 15))
            else:
                break

    print(f"全部内容已保存至 {output_path}")

if __name__ == "__main__":
    download_full_novel(START_URL, OUTPUT_FILE)
