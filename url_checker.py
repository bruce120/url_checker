import requests
import multiprocessing
import os
import signal
from tqdm import tqdm

# 創建argparse物件
import argparse
parser = argparse.ArgumentParser(prog='urlcheck.py', description='連線檢查工具')
parser.add_argument('-f', '--file', help='輸入文件路徑', required=True)

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def open_file(file):
    try:
        with open(file, 'r') as f:
            return [line.strip() for line in f if line.strip()]  # 只加入非空白行
    except IOError:
        print("[-] 匯入檔案失敗，文件不存在、無法讀取或開啟")
        exit(1)  # 終止程式執行

def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            return None
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return None

def process_urls(urls, f):
    pool = multiprocessing.Pool(multiprocessing.cpu_count()*3, init_worker)  # 根據CPU數量設定進程池大小
    print("使用進程：" + str(multiprocessing.cpu_count()*3))
    print(f"[+] 開始檢查 {len(urls)} 個網址")
    try:
        for result in tqdm(pool.imap(check_url, urls), total=len(urls)):
            if result:
                f.write(result + "\n")
    except KeyboardInterrupt:
        print("[-] 使用者中斷操作，等待所有進程安全退出...")
        pool.terminate()  # 立即停止所有的子進程
        pool.join()
    except Exception as e:  # 捕獲並處理其他可能的異常
        print(f"[-] 產生了異常：{str(e)}")
        pool.terminate()
        pool.join()
    else:
        print(f"[+] 檢查完成，結果已寫入 live.txt")

if __name__ == '__main__':
    args = parser.parse_args()
    with open('live.txt', 'w') as f:
        urls = open_file(args.file)
        process_urls(urls, f)
