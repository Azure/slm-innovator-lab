---
layout: default
title: Lab 3.4.1 Content Safety with Azure AI studio before production
permalink: /3_4_contentfilter_en/
parent: Lab 3.4 Overview
grand_parent: Lab 3. LLMOps for SLM with Azure AI Studio
nav_order: 641
---

# Lab 3.4 Content Safety with Azure AI studio before production

![LLMOps](images/content_filtering_api_support.jpg)
[Annotation availability in each API version](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#:~:text=See%20the%20following%20table%20for%20the%20annotation%20availability%20in%20each%20API%20version%3A)

### 前提 条件

- AI Hub と AI プロジェクト リソースを作成できる Azure サブスクリプション
- Fine-tune モデルを登録し、Azure AI Studio に LLM をデプロイしました

### タスク

- エンドユーザーからの問題のあるプロンプトをフィルタリングしたい 
- LLMを呼び出す前に、プロンプトのhamfulキーワードを書き換えたいと思います 
- リスクとコスト管理のメトリックを使用してサービスを監視したい  


### 目次
- 1️⃣ コンテンツの安全性を使用してトレーニングデータセットをテストする
- 3️⃣ カスタムブロックリストを作成して、プロンプト内の不適切なキーワードを管理します
- 2️⃣ オーケストレーション フローの有害なコンテンツにフィルター処理するようにコンテンツ セーフティを構成する
- 4️⃣ デプロイされたアプリケーションをメトリクスで監視する

### クエリレート
- Content Safety 機能には、1 秒あたりのリクエスト数 (RPS) または 10 秒あたりのリクエスト数 (RP10S) のクエリレート制限があります。各機能のレート制限については、次の表を参照してください。link: [Content Safety のクエリ率](https://learn.microsoft.com/ko-kr/azure/ai-services/content-safety/overview)

| 価格レベル | モデレーションAPI<br>(テキストと画像) | プロンプトシールド | 保護材料<br>検出 | 接地検出<br>(プレビュー) | カスタム カテゴリ <br>(急速) (プレビュー) | カスタム カテゴリ <br>(標準) (プレビュー) | マルチ モーダル     |
| ------------ | ----------------------------------- | -------------- | ------------------------------- | ----------------------------------- | -------------------------------------- | ----------------------------------------- | -------------- |
| F0 キー           | 5 RPSの                               | 5 RPSの          | 5 RPSの                           | 該当なし                                 | 5 RPSの                                  | 5 RPSの                                     | 5 RPSの          |
| S0           | 1000 RP10Sの                          | 1000 RP10Sの     | 1000 RP10Sの                      | 50 RPSの                              | 1000 RP10Sの                             | 5 RPSの                                     | 10 RPSの<br><br> |

### Jupyter Notebookを通じて作業
- Python sdkを使用して、jupyter notebookでContent Safetyを作成して実行してみましょう。有害なコンテンツにフィルタリングする方法を学び [ますcontentsafety_with_code.ipynb](pcontentsafety_with_code.ipynb)