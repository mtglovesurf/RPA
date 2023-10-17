# selenium==4.12.0で動作確認しました。
# pip install selenium
import os
import re
import shutil
import tempfile
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_webdriver(download_dir):
    options = webdriver.ChromeOptions()
    options.binary_location = './chromedriver'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    return webdriver.Chrome(options=options)

def process_element(driver, action_type, by_method, selector, input_value=None):
    if action_type == "click":
        click_element(driver, by_method, selector)
    elif action_type == "input":
        input_element(driver, by_method, selector, input_value)

def click_element(driver, by_method, selector, wait_time=10):
    wait = WebDriverWait(driver, wait_time)
    time.sleep(1)
    element = wait.until(EC.element_to_be_clickable((by_method, selector)))
    element.click()
    time.sleep(2)

def input_element(driver, by_method, selector, input_text, wait_time=10):
    wait = WebDriverWait(driver, wait_time)
    time.sleep(1)
    element = wait.until(EC.element_to_be_clickable((by_method, selector)))
    element.send_keys(input_text)
    time.sleep(1)

def wait_for_download_start(download_dir, filename, timeout=300):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if os.path.exists(os.path.join(download_dir, filename)) or \
           os.path.exists(os.path.join(download_dir, filename + '.crdownload')):
            return True
        time.sleep(1)
    return False

def execute_actions(driver, action_list, download_dir):
    for export_info in action_list:
        for action in export_info["actions"]:
            process_element(driver, action["type"], action["by"], action["selector"], action[""])
        
        if "filename" in export_info:
            if not wait_for_download_start(download_dir, export_info["filename"]):
                print(f"{export_info['filename']}のダウンロード開始がタイムアウトしました。")

def replace_newlines_in_quotes(match):
    return match.group(0).replace('\n', '\\n')

def process_csv_file(input_file, output_file, encoding='utf-8'):
    with open(input_file, 'r', encoding=encoding, errors='replace') as f:
        content = f.read()
    content_modified = re.sub(r'\"(.*?)\"', replace_newlines_in_quotes, content, flags=re.DOTALL)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content_modified)

def process_export_info(driver, download_dir, csv_export_paths):
    for export_info in csv_export_paths["sequence"]:
        for action in export_info["actions"]:
            if "input" in action["type"]:
                process_element(driver, action["type"], action["by"], action["selector"], action["value"])
            else:
                process_element(driver, action["type"], action["by"], action["selector"])

        if "filename" in export_info:
            if not wait_for_download_start(download_dir, export_info["filename"]):
                print(f"{export_info['filename']}のダウンロード開始がタイムアウトしました。")

def load_export_info_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert string representation of "By" to the actual By class attribute
    for item in data["sequence"]:
        for action in item["actions"]:
            action["by"] = getattr(By, action["by"])

    return data


def main():

    if not os.path.exists('./input'):
        os.mkdir('./input')
    if not os.path.exists('./output'):
        os.mkdir('./output')

    download_dir = tempfile.mkdtemp()
    driver = initialize_webdriver(download_dir)

    # configフォルダ内のすべてのjsonファイルを取得
    export_infos = [f for f in os.listdir('config') if os.path.isfile(os.path.join('config', f)) and f.endswith('.json')]
    for export_info_file in export_infos:
        export_info = load_export_info_from_json('config/'+export_info_file)
        login_url = export_info["url"]
        driver.get(login_url)
        time.sleep(1)
        process_export_info(driver, download_dir, export_info)

        # download dir から input dirに移動
        for filename in os.listdir(download_dir):
            src_path = os.path.join(download_dir, filename)
            dst_path = os.path.join('./input', filename)
            shutil.move(src_path, dst_path)

        # "sequence"の中の各アイテムから"filename"と"encoding"を抽出
        filenames_and_encodings = [(item['filename'], item['encoding']) for item in export_info['sequence'] if 'filename' in item and 'encoding' in item]
        for filename, encoding in filenames_and_encodings:
            # 改行をエスケープ
            process_csv_file('input/'+filename, 'output/'+filename, encoding)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()
