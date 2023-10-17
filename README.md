# Selenium CSV Downloader

## 概要
指定されたウェブサイトにアクセスし、指定の手順に従ってCSVファイルをダウンロードするPythonスクリプト `download_from_xxx.py`。

## 目次

- [Selenium CSV Downloader](#selenium-csv-downloader)
  - [概要](#概要)
  - [目次](#目次)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [使い方](#使い方)
  - [jsonファイルの仕様](#jsonファイルの仕様)
  - [ライセンス](#ライセンス)
  - [注意事項](#注意事項)

## 前提条件

- Pythonがインストールされていること
- [Selenium](https://www.selenium.dev/)ライブラリがインストールされていること
- [chromedriver](https://chromedriver.chromium.org/downloads)をダウンロードし、`download_from_xxx.py`と同じフォルダに配置してください。

## インストール

```bash
pip install selenium==4.12.0
```

## 使い方

1. `config`フォルダにダウンロード手順を記述したjsonファイルを配置。
2. ターミナルでスクリプトを実行:

```bash
python download_from_xxx.py
```

3. 実行が終わると、`input`フォルダにダウンロードされたCSV、`output`フォルダに加工されたCSVがそれぞれ保存されます。

## jsonファイルの仕様

`config`ディレクトリ内のjsonファイルは以下の構造を持つ必要があります。

```json
{
  "url": "ダウンロードページのURL",
  "sequence": [
    {
      "actions": [
        {
          "type": "click/input",
          "by": "ID/CSS_SELECTOR/CLASS_NAME/...（SeleniumのByクラスの属性）",
          "selector": "セレクタの値",
          "value": "入力アクションの場合の入力値"
        },
        ...
      ],
      "filename": "ダウンロードされるCSVのファイル名",
      "encoding": "ファイルのエンコード（例：utf-8）"
    },
    ...
  ]
}
```

- `url`: ダウンロードページのURL。
- `sequence`: 操作の一連の手順を配列として定義。
  - `actions`: 各操作に関する情報。
    - `type`: "click"または"input"。
    - `by`: セレクタのタイプ（SeleniumのByクラスの属性に該当するもの）。
    - `selector`: セレクタの値。
    - `value`: "input"アクションの場合、入力するテキスト。
  - `filename`: ダウンロードされるCSVのファイル名。
  - `encoding`: ファイルのエンコード情報。

## ライセンス

このソフトウェアは、株式会社ズコーシャの内部使用のみを目的としています。外部での再配布や公開は禁止されています。詳細については、ライセンスファイルを参照してください。

## 注意事項

Seleniumと関連するパッケージのアップデートにより、このスクリプトの動作が保証されない場合があります。定期的な更新とテストを行ってください。

---