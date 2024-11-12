---
layout: home
title: Lab 0. Requirements (ja-jp)
nav_order: 3
---

[English](README.md)

# Lab 0. Requirements: ハンズオン環境設定

## 1. 環境を整えるための事前準備

### チェックリスト

{: .warning}
(Optional) Azure AI Document Intelligence を利用する場合は、 **East-US, West-US2, West-Europe** のいずれかに作成してください。他のリージョンではアクセスの制限がある可能性があります。
 ([Source](https://learn.microsoft.com/en-us/answers/questions/1514842/document-intelligence-ai-returns-404))

{: .note}
以下の Azure のサービスを作成および利用するのに、十分な権限およびクオータをお持ちであることをご確認ください:

- Azure OpenAI Service & GPT-4o のデプロイ
- (Optional) Azure AI Document Intelligence
- Azure Machine Learning Clusters (VM)
    - (Optional) Standard DSv2 Family Cluster (**[Standard_DS11_v2]**)
        - データ作成やアプリ開発の際に使用します。ローカル PC をご利用いただくことも可能ですが、ハンズオン環境を揃えるため、ご利用をお勧めいたします。
        - **事前にクオータ付与の申請が必要な場合があります。**
    - Standard NCADSA 100v4 Family Cluster (**[Standard_NC24ads_A100_v4]**)
        - LLM のトレーニングに使用します。 **事前にクオータ付与の申請が必要です。**
        - **[Low-priority VM]** の利用も可能
        - **24 コア** が必要になります
    - Standard NCSv3 Family Cluster (**[Standard_NC6s_v3]**)
        - ファインチューニングを行った LLM のデプロイメント (ホスティング) に使用します。**事前にクオータ付与の申請が必要です。**
        - **12 コア** が必要になります

### クオータの申請

Azure OpenAI Service および Azure Machine Learning CLuster を作成するのに充分なクオータがない場合は、クオータの引き上げ要求を申請する必要があります。予め以下の手順でクォータをご確認いただき、必要に応じて申請をお願いいたします。

- [Azure OpenAI Service のクォータを管理する: クォータの表示と要求](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/quota?tabs=rest#view-and-request-quota)
- [Azure Machine Learning を使用するリソースのクォータと制限の管理と引き上げ: クォータと制限の引き上げ要求](https://learn.microsoft.com/ja-jp/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2#request-quota-and-limit-increases)

### ハンズオンに必要なサービスの作成

{: .note}
以下をすべて新規作成する場合は、**East-US** を選択いただくと、同じリージョンでサービスをそろえることができます。

{: .warning}
Azure AI Studio および Azure ML Studio でサービス参照方法が異なるため、必ず以下の順番で作成を行ってください。

0. Azure Portal から **新規リソースグループ** を作成します。

1. Azure ML Studio から **新規ワークスペース** を作成します
    - リソースグループは Azure Portal で作成したハブを選択してください

2. Azure AI Studio から **新規プロジェクト** および **新規ハブ** を作成します
    - 新規ハブを選択して作成します
    - リソースグループは Azure Portal で作成したハブを選択、Azure AI リソースは新規作成 (または同じサブスクリプション内に作成済みのリソースを設定) を行ってください
    - 作成した (または設定した) Azure AI リソースで、GPT-4o mini モデルをデプロイしておきます

3. (Optional) Azure Portal から **Document Intelligence (旧称: Form Recognizer)** を作成します
    - リソースグループは、Azure Portal で作成したリソースグループを選択してください
    - リージョンは **East-US, West-US2, West-Europe** のいずれかを選択してください

## 2. ハンズオンのための環境セットアップ

- 1️⃣ コンピューティングインスタンスの作成
- 2️⃣ ハンズオンフォルダーのクローン
- 3️⃣ `.env` の設定
- 4️⃣ config.yml の設定
- 🚀 Get started to validate the setup 

### 1️⃣ コンピューティングインスタンスの作成

1. Azure ML Studio からコンピューティングインスタンスを作成します。作成済みのワークスペースを開き、**コンピューティング** のメニューを開きます。

2. **コンピューティング インスタンス** のタブから **[Standard_DS11_v2]** (Intel 2 cores, 14GB RAM, 28GB storage, CPU) を選択して作成します。コンピューティングインスタンスが作成されて、起動するのを確認してください。

3. **コンピューティング インスタンス** のタブから **[Standard_NC6s_v3]** (NVIDIA Tesla V100, 112GB RAM, 736 GB storage, GPU) を選択して作成します。コンピューティングインスタンスが作成されて、起動するのを確認してください。

4. **コンピューティング クラスター** のタブから **[Standard_NC24ads_A100_v4]** を選択して作成します。コンピューティングクラスターが作成されて、状態が **作成しました** と表示されることを確認してください。

### 2️⃣ ハンズオンフォルダーのクローン

1. コンピューティングインスタンスが起動していることを確認して、`JupyterLab` or `VS Code(Web)` からターミナルを開き、**code/user/(サインインユーザー名)** のディレクトリーに移動します。

2. 以下のコマンドで、インスタンス内の conda 環境を azureml_py310_sdkv2 に指定 (変更) して、SLM Innovator Lab のハンズオンフォルダーを Git clone し、requirements.txt の内容をインストールします。

```shell
conda activate azureml_py310_sdkv2
git clone https://github.com/Azure/slm-innovator-lab.git
cd slm-innovator-lab #クローンしたディレクトリーに移動
pip install -r requirements.txt
```

3. (Optional) PDF を解析する際に Unstructured Toolkit を利用する場合は, `startup_unstructured.sh` を起動し、コンピューティングインスタンスの起動コマンドにも追加しておきます。

```shell
./startup_unstructured.sh
```

### 3️⃣ `.env` の設定

user/(ユーザー名)/slm-innovator-lab にある `.env.sample` を `.env` にファイル名を変更し、 `.env` 内の設定を、ご自分の Azure サービスの値に書き換えます。

```shell
# .env
# this is a sample for keys used in this code repo. 
# Please rename it to .env before you can use it
AZURE_OPENAI_ENDPOINT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

AZURE_DOC_INTELLIGENCE_ENDPOINT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_DOC_INTELLIGENCE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```


### 4️⃣ config.yml の設定

`2_slm-fine-tuning-mlstudio/phi3/config.yml` を開き、設定をご自分の Azure サービスの値に書き換えます。

```yaml
config:
    AZURE_SUBSCRIPTION_ID: "<YOUR-SUBSCRIPTION-ID>" # Please modify to your subscription
    AZURE_RESOURCE_GROUP: "<YOUR-RESOURCE-GROUP>" # Please modify to your Azure resource group
    AZURE_WORKSPACE: "<YOUR-AZURE-WORKSPACE>" # Please modify to your Azure workspace
    AZURE_DATA_NAME: "hf-ultrachat" # Please modify to your AzureML data name
    DATA_DIR: "./dataset"
    CLOUD_DIR: "./cloud"
    HF_MODEL_NAME_OR_PATH: "microsoft/Phi-3.5-mini-instruct"
    IS_DEBUG: true
    USE_LOWPRIORITY_VM: true
    ...
```


### 🚀 セットアップ内容の確認

[Jupyter notebook](1_get_started.ipynb) を開き、実行を行って動作することを確認してください。


{: .warning}
確認が終わったら、余分な課金を避けるため、一旦 コンピューティングインスタンスを停止しておきます。

{: .note}
当ハンズオンのリソースが不要になった場合は削除してください。Azure Portal から作成したリソースグループを削除すると、含まれるリソースを一括で削除することができます。


[Azure OpenAI]: https://oai.azure.com/
[Azure ML]: https://ml.azure.com/
[Azure AI Studio]: https://ai.azure.com/
[Standard_DS11_v2]: https://learn.microsoft.com/azure/virtual-machines/sizes/memory-optimized/dv2-dsv2-series-memory
[Standard_E2as_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/memory-optimized/easv4-series
[Standard_NC24ads_A100_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nca100v4-series?tabs=sizebasic
[Standard_NC6s_v3]: https://learn.microsoft.com/azure/virtual-machines/sizes/gpu-accelerated/ncv3-series?tabs=sizebasic
[Low-priority VM]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-optimize-cost?view=azureml-api-2#low-pri-vm
[Azure ML reserves 20% of the quota for the deployment]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2


[^1]: This extra quota is reserved for system-initiated operations such as OS upgrades and VM recovery, and it won't incur cost unless such operations run.
