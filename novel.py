import time
import random
import requests
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# ———— 配置 ————
TOC_URL = "https://trxs.cc/tongren/4196.html"
OUTPUT = "novel.txt"

# 随机 UA
ua = UserAgent()

# 可以不使用代理或自行填充代理列表
PROXIES = []
proxy_cycle = cycle(PROXIES) if PROXIES else None

def make_session():
    """返回一个带随机 UA、可选代理的 Session"""
    s = requests.Session()
    s.headers.update({
        "User-Agent": ua.random,
        "Referer": TOC_URL,
        "Accept-Language": "zh-CN,zh;q=0.9"
    })
    if proxy_cycle:
        s.proxies.update(next(proxy_cycle))
    return s

# ——定制化的目录抓取部分——
def get_chapter_links(toc_url):
    sess = make_session()
    resp = sess.get(toc_url, timeout=10)
    resp.encoding = "gbk"
    soup = BeautifulSoup(resp.text, "lxml")

    chapters = []
    # 这里用新选择器：div.book_list.clearfix ul li a
    for a in soup.select("div.book_list.clearfix ul li a"):
        title = a.get_text(strip=True)
        link  = urljoin(toc_url, a["href"])
        chapters.append((title, link))
    return chapters


def get_chapter_text(chapter_url: str) -> str:
    """抓取单章正文，返回纯文本"""
    sess = make_session()
    resp = sess.get(chapter_url, timeout=10)
    resp.encoding = "gbk"  # 强制 GBK 解码
    soup = BeautifulSoup(resp.text, "lxml")

    # 1) 定位到 <div class="read_chapterDetail"> 容器
    content_div = soup.find("div", class_="read_chapterDetail")
    if not content_div:
        raise RuntimeError(f"正文容器未找到：{chapter_url}")

    # 2) 删除脚本、样式和广告标签
    for tag in content_div(["script", "style", "ins"]):
        tag.decompose()

    # 3) 提取所有文本行
    paras = []
    for p in content_div.find_all("p"):
        text = p.get_text(strip=True)
        if not text:
            continue
        paras.append(text)

    # 4) 合并为一个纯文本块，用双换行分隔段落
    return "\n\n".join(paras)

def download_novel(toc_url, output_path):
    """主流程"""
    chapters = get_chapter_links(toc_url)
    total = len(chapters)
    print(f"共 {total} 章，开始抓取…")

    with open(output_path, "w", encoding="utf-8") as fw:
        for idx, (title, link) in enumerate(chapters, start=1):
            try:
                text = get_chapter_text(link)
            except Exception as e:
                print(f"[跳过] 第{idx}/{total}章《{title}》失败：{e}")
                continue

            # 写入标题与正文
            #fw.write(f"第 {idx} 章  {title}\n\n")
            fw.write(text)
            fw.write("\n\n" + "="*40 + "\n\n")
            print(f"[{idx}/{total}] 已写入：{title}")

            # 随机延迟 1~2 秒
            #time.sleep(random.uniform(1, 2))

    print(f"全部章节已保存到：{output_path}")

if __name__ == "__main__":
    download_novel(TOC_URL, OUTPUT)
