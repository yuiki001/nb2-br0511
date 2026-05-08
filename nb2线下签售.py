import requests
import time
from datetime import datetime
import os
import getpass
import json
import subprocess  # 新增：用于执行 git 命令
import pandas as pd  # 新增：用于数据存储
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ================== Git 推送配置 ==================
GITHUB_REPO = "your_username/your_repo"        # 请替换为您的仓库名
GITHUB_BRANCH = "main"                          # 分支名（main 或 master）
# GitHub Personal Access Token 优先从环境变量 GITHUB_TOKEN 读取

# ========== 原有配置信息 ==========
api_url = "https://en.beatroad.co.kr/exec/front/order/Formproductmileage/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5     ",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://en.beatroad.co.kr",
    "Pragma": "no-cache",
    "Referer": "https://en.beatroad.co.kr/order/orderform.html?basket_type=A0000&delvtype=B",
    "X-Requested-With": "XMLHttpRequest"
}

# ========== Cookies ==========
cookies =  {
  "_fwb": "94mK8xDD6JnQlW1LJqHYl0.1761020662626",
  "CUK45": "cuk45_beatroad_s9gdqpddb7tjb52olvtpv9e4l5080n3p",
  "CUK2Y": "cuk2y_beatroad_s9gdqpddb7tjb52olvtpv9e4l5080n3p",
  "CFAE_CUK1Y": "CFAE_CUK1Y.beatroad_2.ONV2ASN.1761023056321",
  "CVID_Y": "CVID_Y.535755404a5a515d6c02.1778210831831",
  "siteLT": "a8d9089b-9ac1-9678-bf62-0179a8e9fa29",
  "analytics_longterm": "analytics_longterm.beatroad_2.D3352AE.1761023054369",
  "wcs_bt": "unknown:1772549984",
  "fb_event_id": "event_id.beatroad.2.6RTBGPOTGH8DXEITUOSA7G0GHUGQPEOT",
  "fb_external_id": "a3d3423af3cdf814a552c3d347bbb3b0f46c2dcd8d4810c17555cf5d0738a979",
  "siteSID": "e3a9656d-f06a-0301-5d72-fa95f687a5bb",
  "analytics_session_id": "analytics_session_id.beatroad_2.BB7A55F.1778210574003",
  "CVID": "CVID.535755404a5a515d6c02.1778210831831",
  "CID": "CIDR1550c1b572895ed87c5226a2f55511c2",
  "CIDR1550c1b572895ed87c5226a2f55511c2": "698c842b835671f707bcc3f692b728e6%3A%3A%3A%3A%3A%3Ahttps%3A%2F%2Fcn.bing.com%2F%3A%3ABING%3A%3A1%3A%3A%3A%3A%3A%3A%3A%3A%3A%3A%2F%3A%3A1778210573%3A%3A%3A%3Appdp%3A%3A1778210573%3A%3A%3A%3A%3A%3A%3A%3A",
  "vt": "1778210808",
  "ECSESSID": "ouso47581i8pf88h76m9odojqtgnh8hv",
  "basketcount_1": "0",
  "basketprice_1": "%26%238361%3B0",
  "wish_id": "9ec3b69d78b2b9863f6151ea32905086",
  "wishcount_1": "0",
  "isviewtype": "pc",
  "ec_ipad_device": "F",
  "CFAE_CID": "CFAE_CID.beatroad_2.A6HKXPO.1778210575153",
  "recent_plist2": "9886%7C9880%7C10015%7C10037%7C10391%7C10514%7C10564%7C10581%7C10591%7C10610%7C10613%7C10688%7C10756%7C10940%7C11070",
  "org_phpsess_id_2": "ouso47581i8pf88h76m9odojqtgnh8hv",
  "return_url": "%2Forder%2Forderform.html%3Fbasket_type%3DA0000%26delvtype%3DB",
  "login_provider_2": "%7B%22member_id%22%3A%22qq11580469617784%22%2C%22provider%22%3Anull%2C%22client_id%22%3Anull%7D",
  "iscache": "F",
  "ec_mem_level": "2",
  "PHPSESSVERIFY": "c52dca785a893bed15017307eaffffcf",
  "couponcount_2": "0",
  "atl_epcheck": "1",
  "atl_option": "1%2C1%2CH",
  "basketprice_2": "%26%2336%3B20.16",
  "ec_async_cache_avail_mileage_2": "0.00",
  "ec_async_cache_used_mileage_2": "0.00",
  "ec_async_cache_returned_mileage_2": "0",
  "ec_async_cache_unavail_mileage_2": "0",
  "ec_async_cache_used_deposit_2": "0",
  "ec_async_cache_all_deposit_2": "0",
  "ec_async_cache_deposit_refund_wait_2": "0",
  "ec_async_cache_member_total_deposit_2": "0",
  "wishcount_2": "0",
  "CFAE_LC": "CFAE_LC.beatroad_2.N8NNAMV.1778210808314",
  "basketcount_2": "1"
}

# ========== 本地日志输出配置 ==========
current_user = getpass.getuser()
if os.name == "nt":  # Windows
    LOG_FILE = fr"sui影通.csv"
else:  # Linux / macOS
    LOG_FILE = os.path.expanduser("~/yena线下签售.csv")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ========== requests 会话配置 ==========
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["POST"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)


# ================== Git 推送函数 ==================
def git_push_update():
    """
    将最新的 CSV 文件提交并推送到 GitHub
    """
    try:
        # 获取 GitHub Token（优先从环境变量读取）
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print("⚠️ 环境变量 GITHUB_TOKEN 未设置，跳过 Git 推送")
            return

        # 构建带认证的远程仓库 URL
        remote_url = f"https://{token}@github.com/{GITHUB_REPO}.git"

        # 添加 CSV 文件到暂存区
        subprocess.run(['git', 'add', LOG_FILE], check=True, capture_output=True)

        # 检查是否有文件变化（避免空提交）
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode != 0:
            # 有变化，提交
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"自动更新数据 {timestamp}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)

            # 推送到 GitHub（指定分支）
            subprocess.run(
                ['git', 'push', remote_url, f'HEAD:{GITHUB_BRANCH}'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ 已推送到 GitHub: {commit_msg}")
        else:
            print("⏭️ CSV 文件无变化，跳过推送")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e.stderr if e.stderr else e}")
    except Exception as e:
        print(f"❌ 推送过程中发生错误: {e}")


# ========== 写入本地CSV文件（改用pandas） ==========
def write_to_csv_file(time_str, product_name, stock_change, single_sale):
    """
    将监控结果写入本地CSV文件（使用pandas concat方式），并触发Git推送
    """
    try:
        # 定义列名
        columns = ["时间", "商品名称", "库存变化", "单笔销量"]

        # 1. 如果文件存在，读取现有数据；否则创建空DataFrame
        if os.path.exists(LOG_FILE):
            df_existing = pd.read_csv(LOG_FILE, encoding='utf-8-sig')
        else:
            df_existing = pd.DataFrame(columns=columns)

        # 2. 将新数据行转换为DataFrame并拼接
        new_row = pd.DataFrame([[time_str, product_name, stock_change, single_sale]], columns=columns)
        df_updated = pd.concat([df_existing, new_row], ignore_index=True)

        # 3. 保存回CSV（覆盖原文件），使用utf-8-sig编码
        df_updated.to_csv(LOG_FILE, index=False, encoding='utf-8-sig')

        # 4. 打印存储的内容（与原格式保持一致）
        print(f"{time_str} 商品[{product_name}] 库存变化: {stock_change}, 单笔销量: {single_sale}")

        # 5. 触发Git推送
        git_push_update()

    except Exception as e:
        print(f"❌ 写入CSV文件失败: {e}")


# ========== 获取库存 ==========
def get_stock_from_api():
    """调用 API 获取 Beatroad 商品库存"""
    try:
        response = session.post(api_url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        data = response.json()

        product_list = data.get("product", [])
        stocks = {}
        for product in product_list:
            product_no = product.get("product_no")
            product_name = product.get("product_name", "未知商品")
            stock = product.get("stock_number", None)
            if product_no and stock is not None:
                stocks[product_no] = {"name": product_name, "stock": int(stock)}

        return stocks

    except Exception as e:
        print(f"{datetime.now()} ❌ API请求失败: {e}")
        return {}


# ========== 主监控函数 ==========
def monitor_stock():
    print(f"📄 日志输出路径: {LOG_FILE}")

    previous_stocks = {}  # 上次库存记录
    initial_stocks = {}  # 初始库存记录

    while True:
        current_stocks = get_stock_from_api()
        if not current_stocks:
            print("⚠️ 无法获取库存数量")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for product_no, info in current_stocks.items():
                product_name = info["name"]
                current_stock = info["stock"]

                # 第一次记录初始库存
                if product_no not in initial_stocks:
                    initial_stocks[product_no] = current_stock
                    previous_stocks[product_no] = current_stock

                    # CSV存储（商品名称硬编码为"beatroad"，保持与原代码一致）
                    write_to_csv_file(current_time, "beatroad", str(current_stock), str(abs(current_stock)))

                    # 打印（打印时使用真实商品名称）
                    log_message = f"{current_time} 商品[{product_name}]({product_no}) 初始库存: {current_stock}"
                    print(log_message)

                # 检测库存变化
                elif current_stock != previous_stocks[product_no]:
                    stock_diff = previous_stocks[product_no] - current_stock

                    # CSV存储（商品名称硬编码为"beatroad"）
                    stock_change_str = f"{previous_stocks[product_no]} -> {current_stock}"
                    write_to_csv_file(current_time, "beatroad", stock_change_str, str(stock_diff))

                    # 打印（打印时使用真实商品名称）
                    change_message = (
                        f"{current_time} 商品[{product_name}]({product_no}) "
                        f"库存变化： {previous_stocks[product_no]} -> {current_stock}, 销量:{stock_diff}"
                    )
                    print(change_message)
                    previous_stocks[product_no] = current_stock

        time.sleep(10)


# ========== 程序入口 ==========
if __name__ == "__main__":
    print(f"启动监控，日志输出到: {LOG_FILE}")
    monitor_stock()