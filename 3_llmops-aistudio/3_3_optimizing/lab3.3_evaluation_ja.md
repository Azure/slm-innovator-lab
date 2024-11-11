---
layout: default
title: Lab 3.3.1 Evaluate your models using Prompt Flow (UI)
permalink: /3_3_1_evaluation/
parent: Lab 3.3 Overview
grand_parent: Lab 3. LLMOps for SLM with Azure AI Studio
nav_order: 631
---

# Lab 3.3.1 Evaluate your models using Prompt Flow (UI)

![LLM
](images/evaluation-monitor-flow.png)
[生成AIアプリケーションの評価とモニタリング](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-approach-gen-ai#evaluating-and-monitoring-of-generative-ai-applications)

### 前提 条件

- AI Hub と AI プロジェクト リソースを作成できる Azure サブスクリプション
- Azure AI Studio にデプロイされた gpt-4o モデル


### タスク

- モデルとRAGがどれだけ疑問に答えているかを定量的に検証します
- 本番環境で一括データをベンチマークし、ボトルネックを見つけて改善します


### 目次
- 1️⃣ 選択したモデルの出力を確認するための手動評価
- 2️⃣ LLMバリアントでA/Bテストを実施
- 3️⃣ バリアントによる自動評価の作成
- 4️⃣ プロンプトフローでカスタム評価フローを作成

### 1️⃣ 選択したモデルの出力を確認するための手動評価 
1. Azure AI Studio の > Tools > Evaluation に移動します。
2. 「手動評価」タブをクリックして、AIアプリケーションのパフォーマンスを評価および比較するための手動評価を作成します。
![新しいマニュアル評価](images/new_manual_evaluation.jpg)

3. 構成でテストするモデルを選択し、以下のシステムメッセージを更新します。 
```
You are a math assistant, and you are going to read the context which includes simple math questions and answer with numbers only. 
```
4. 「テストデータのインポート」ボタンをクリックして、テストデータをインポートします。コンテキストを使用してモデルをテストする場合は、データを追加することもできます。

5. モデルでテストするデータセットを選択します。
![データセットの選択](images/import_test_data_select_dataset.jpg)

6. テストデータをマップします。入力として question を選択し、出力として answer を選択します。追加ボタンをクリックして、テストデータをインポートします。
![マップデータ](images/import_test_data_map_data.jpg)

7. [実行] ボタンをクリックして、テスト データを使用してモデルをテストします。テストが完了したら、結果を表示してエクスポートしたり、結果を期待される回答と比較したりすることもできます。親指を上または下に使用して、モデルのパフォーマンスを評価します。この結果は手動評価用であるため、結果データセットを自動評価に引き継いで、モデルを一括データで評価できます。
![テストの実行](images/manual_eval_run_test.jpg)

### 2️⃣ LLMバリアントでA/Bテストを実施
バリアントを使用した新しいチャットフローを作成する 
1. Azure AI Studio > プロンプト フロー > [+ 作成] をクリックして新しいフローを作成します
![新しいフローを作成する](../3_2_prototyping/images/create_new_flow.jpg)

2. ユーザーフレンドリーなチャットインターフェースを取得するには、[チャットフロー]を選択します
![チャットフローを選択します](../3_2_prototyping/images/create_new_chat_flow.jpg)

3. Promptflowファイルを保存するフォルダ名を入力し、[作成]ボタンをクリックします
![フォルダ名を入力してください](../3_2_prototyping/images/put_folder_name.jpg)

4. RAWファイルモデルとして変更して、基本的なチャットフローを変更します
![フォルダ名を入力してください](../3_2_prototyping/images/change_raw_file_mode.jpg)

5. flow.dag.yamlを修正し、以下のソースコードを添付してください。 
```
id: chat_variant_flow
name: Chat Variant Flow
inputs:
  question:
    type: string
    is_chat_input: true
  context:
    type: string
    default: >
      The Alpine Explorer Tent boasts a detachable divider for privacy, 
      numerous mesh windows and adjustable vents for ventilation, and 
      a waterproof design. It even has a built-in gear loft for storing 
      your outdoor essentials. In short, it's a blend of privacy, comfort, 
      and convenience, making it your second home in the heart of nature!
    is_chat_input: false
  firstName:
    type: string
    default: "Jake"
    is_chat_input: false
outputs:
  answer:
    type: string
    reference: ${chat_variants.output}
    is_chat_output: true
nodes:
- name: chat_variants
  type: llm
  source:
    type: code
    path: chat_variants.jinja2
  inputs:
    deployment_name: gpt-4o
    temperature: 0.7
    top_p: 1
    max_tokens: 512
    context: ${inputs.context}
    firstName: ${inputs.firstName}
    question: ${inputs.question}
  api: chat
  provider: AzureOpenAI
  connection: ''
environment:
  python_requirements_txt: requirements.txt
```
6. Raw ファイル・モードを再度変更し、デプロイされた LLM モデルを呼び出すように LLM ノードの接続パラメーターを追加し、[Validate and parse input] をクリックします。LLM ノードへの入力を所定の位置に確認します。
![接続パラメータを追加する](images/add_gpt4o_node2.jpg)

7. 以下のプロンプトをchat_variantsノードに添付して、デプロイされたモデルをリクエストします。 

```
system:
You are an AI assistant who helps people find information. As the assistant, 
you answer questions briefly, succinctly, and in a personable manner using 
markdown and even add some personal flair with appropriate emojis.

Add a witty joke that begins with “By the way,” or “By the way. 
Don't mention the customer's name in the joke portion of your answer. 
The joke should be related to the specific question asked.
For example, if the question is about tents, the joke should be specifically related to tents.

Respond in your language with a JSON object like this.
{
  “answer": 
  “joke":
}

# Customer
You are helping {{firstName}} to find answers to their questions.
Use their name to address them in your responses.

# Context
Use the following context to provide a more personalized response to {{firstName}}:
{{context}}

user:
{{question}}
```

8. 変更したフローを保存します。更新されたチャット フローを実行するためにコンピューティング インスタンスが実行されていることを確認します
![新しいフローを作成する](../3_2_prototyping/images/save_and_run_compute_session.jpg)

9. チャットウィンドウで現在のフローをテストしてみましょう
![フローをテストする](images/test_current_flow.jpg)

10. これで、バリアントを生成し、日本語で書かれたプロンプトと結果を比較できます。「generate variant (バリアントの生成)」ボタンをクリックして、新しいバリアントを作成します。
![バリエーションを追加](images/add_variants.jpg)

11. 以下に、バリアント名と日本語のプロンプトを追加します。保存ボタンをクリックして、バリアントを保存します。

```
system:
あなたは、人々が情報を見つけるのを助けるAIアシスタントです。
アシスタントとしては、正確で簡潔、かつパーソナライズされた方法で質問に答えることが求められます。
回答にはマークダウンを使用し、シンプルで分かりやすくし、適切な絵文字で親しみを加えることができます。

「ところで」で始まる機知に富んだジョークを追加します。ただし、ジョークの部分では回答に名前を使用しないでください。
ジョークは、尋ねられる特定の質問に関連したものでなければなりません。
例えば、質問がテントについての場合、ジョークもテントに関連したものであるべきです。

以下のJSONオブジェクトを使用して日本語で応答してください: 
{
  "answer": 
  "joke":
}

# Customer
あなたは私がこの質問に対する答えを見つけるのを手伝っています。
答えに名前を使用して、相手に言及します。

# Context
次のコンテキストを使用して、よりパーソナライズされた応答を {{firstName}} に提供します。日本語でお答えください:
{{context}}

user:
{{question}}
```

12. これで、チャットウィンドウでバリアントの1つをデフォルトとして設定して、バリアントをテストできます。「実行」ボタンをクリックして、バリアントをテストします。 


### 3️⃣ バリアントを使用した QnA 関連性評価フローの作成
1. Azure AI Studio の > Tools > Evaluation に移動します。

2. [自動評価] タブの [+ 新しい評価] をクリックして作成します。 

3. 「プロンプトフロー」をクリックして、その出力を評価するフローを選択します。
![新しい評価](images/new_promptflow_evaluation.jpg)

4. 評価の基本情報を追加します。評価の名前を「variant1_en」として入れ、評価するフローを選択します。評価シナリオとして [コンテキストを使用した質問と回答] を選択します。「次へ」ボタンをクリックして続行します。
![基本情報](images/evaluation_basic_info.jpg)

5. データセットとして 'simple_qna_data_en.jsonl' を追加し、question、firstName、context、dataset 列をマップします。「次へ」ボタンをクリックして続行します。
![マップデータ](images/evaluation_map_data.jpg)

6. 「評価メトリック」を選択します。モデルを評価する指標を選択できます。接続モデルとデプロイモデルを入力して [次へ] ボタンをクリックし、最終的な設定を確認して [送信] ボタンをクリックして評価を開始/待機します。
![メトリクスの選択](images/evaluation_select_metrics.jpg)
![評価の実行](images/evaluation_running.jpg)

>  +ご参考までに<br>
エバリュエーターは、評価を実行するために使用できるアセットです。SDK でエバリュエーターを定義し、評価を実行して 1 つ以上のメトリックのスコアを生成できます。プロンプトフローSDKでAI支援の品質および安全性エバリュエーターを使用するには、[プロンプトフローSDKによる評価](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/flow-evaluate-sdk) を確認してください。 
