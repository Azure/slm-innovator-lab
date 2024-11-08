# SLM Innovator Lab

Azure AI/ML Platform を基盤とする SLM Innovator Lab で、AI プロジェクトの可能性を最大限に引き出しましょう。このラボは、Azure での複数の SLM モデルの微調整とデプロイに優れたお客様や、RAG アプリケーションを作成するための微調整を通じて基本モデルのパフォーマンスを最適化することを目指しているお客様向けに設計されています。AI Studio の高度な機能により、効率的でスケーラブルな LLMOps を確立できます。

このハンズオンラボは、次の目的に適しています。

1. 1日ワークショップ(お客様により異なる4〜7時間) / LLMOpsハンズオンによる2日ワークショップ
2. ハッカソンスターターコード
3. SLMのfine-tuning&serving PoC/Prototypeのリファレンスガイド

ハンズオンガイド:https://azure.github.io/slm-innovator-lab/

## 新しいコンテンツ (2024 年 10 月 25 日)
 LLMOpsとpromptflow python SDK<br>
このハンズオンでは、Python SDK を使用して、新しいフローを作成し、チャット フロー構造を定義し、微調整されたモデル エンドポイントを統合する方法を学習します。また、フローを使用してモデルのパフォーマンスを比較および評価する方法についても学習します。これは、以前に Azure AI Studio UI に基づいて利用可能だったハンズオンに追加されるものです。
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/3_llmops-aistudio/3_2_prototyping/promptflow_with_code.ipynb">ノートブックに移動します</a>
<br><br>
 Microsoft Olive モデルの最適化 <br>
Microsoft Olive は、AI モデルのデプロイを効率化するために Microsoft が開発したハードウェア対応の AI モデル最適化ツールチェーンです。オリーブは、特にエッジデバイス、クラウド、およびさまざまなハードウェア構成で使用するために、AIモデルをより速く、より効率的にすることで、デプロイ用のAIモデルを準備するプロセスを簡素化します。このハンズオンでは、デバイス上またはハイブリッドのデプロイ シナリオを検討します。
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/2_slm-fine-tuning-mlstudio/phi3/3_optimization_olive.ipynb">ノートブックに移動します</a>
<br><br>
 Python SDK<br> によるコンテンツの安全性
このハンズオンでは、テキストブロックリストの管理、性的なコンテンツ、暴力、憎悪、自傷行為に関するテキストと画像の分析を、複数の深刻度レベルで行うことができます。また、Azure Open AI Service と統合する方法についても学習します: Azure Open AI Service を使用して、有害なコンテンツに対してコンテンツを書き換えます。
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/3_llmops-aistudio/3_4_operationalizing/contentsafety_with_code.ipynb">ノートブックに移動</a>

## 必要条件
開始する前に、次の要件を満たす必要があります。

- [Azure OpenAI Service へのアクセス](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure ML の概要](https://github.com/Azure/azureml-examples/tree/main/tutorials): [Azure ML] ワークスペースに接続し<WORKSPACE_NAME>、. <RESOURCE_GROUP> <SUBSCRIPTION_ID>
- [Azure AI Studio の概要](https://aka.ms/azureaistudio): プロジェクトを作成する
- [Azure AI ドキュメント インテリジェンス (v4.0 - 2024-02-29 プレビュー)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

- ***[Computing Instance - コード開発用]*** GPU を使用しないローエンド インスタンスをお勧めします: **[Standard_E2as_v4]** (AMD 2 コア、16 GB RAM、32 GB ストレージ) または **[Standard_DS11_v2]** (Intel 2 コア、14 GB RAM、28 GB ストレージ、GPU なし)  
- ***[Computing Cluster - SLM/LLM の微調整用]*** 単一の NVIDIA A100 GPU ノード (**[Standard_NC24ads_A100_v4]**) をお勧めします。専用のクォータがない場合、または予算が限られている場合は、**[低優先度 VM]** を選択します。
- ***[SLM/LLM の展開]*** 2 つの NVIDIA V100 GPU (**[Standard_NC6s_v3]**) または 2 つの NVIDIA A100 GPU (**[Standard_NC24ads_A100_v4]**) をお勧めします。 

**Note**
管理されたオンライン エンドポイントの場合、 [Azure ML では、デプロイのクォータの 20% が予約されています].[^1] デプロイ内の VM SKU に対して特定の数のインスタンスをリクエストする場合は、 `ceil(1.2 × number of instances requested for deployment) × number of cores for the VM SKU` エラーが発生しないように、使用可能なクォータが必要です。たとえば、 `Standard_NC6s_v3` デプロイで VM (6 コアが付属) の 1 つのインスタンスを要求する場合、12 コア (ceil(1.2 × 1 インスタンス) = 2, 2 × 6 コア) のクォータが使用可能である必要があります。  

上記の要件をまだお持ちでない場合は、まずラボの準備に進んでください。
### [Lab 0. ラボの準備](0_lab_preparation)

**アカウントに合わせてファイルを変更することを忘れないでください `.env` 。名前を変更する `.env.sample` `.env` か、コピーして使用します**

## 注意
このワークショップは、パブリック環境で設定し、インターネットにアクセスできることを前提としています。プライベート環境で構成している場合は、サービスにアクセスするためにプライベートネットワークの設定が必要になる場合があります。プライベート環境で構成するときに発生する可能性のある一般的な問題を次に示します。
-  [Azure ML] ワークスペースと [Azure AI スタジオ] プライベートネットワークを設定する場合、サービスにアクセスするためにVPNまたはプライベートリンクを設定する必要がある場合があります。
- 優先度の低い VM を使用している場合は、VM が使用可能になるまで待つ必要がある場合があります。VM の可用性は、リージョンによって異なる場合があります。
- BLOB ストレージがある場合は、それを使用してデータとモデルを格納できます。ただし、ワークスペース内の BLOB ストレージへの接続を設定する必要がある場合があります [Azure ML] 。
- クォータの問題がある場合は、VM または GPU のクォータの引き上げをリクエストする必要があります。
- ワークスペースでネットワークを設定すると [Azure ML] 、ネットワークを変更することはできません。ネットワークを変更する場合は、新しいワークスペースを作成する必要がある場合があります。
- ワークスペースと同じリージョンにないコンピューティング インスタンスを使用している場合は [Azure ML] 、サービスにアクセスするために VPN またはプライベート リンクの設定が必要になる場合があります。
- で作成したコンピュート・インスタンスを使用している場合 [Azure AI スタジオ]、そのコンピュート・インスタンスでトレーニング・ジョブを実行することはできません。ワークスペースに新しいコンピューティング インスタンスを作成する必要がある場合があります [Azure ML] 。
- 成果物のダウンロード時に PermissionMismatch エラーが発生した場合は、ワークスペースに適切なアクセス許可を割り当てなければならない場合があります [Azure ML] 。

## 使用を開始する方法 
1. コンピューティング インスタンスを に作成します [Azure ML]。コード開発には、 **[Standard_DS11_v2]** (2 コア、14 GB RAM、28 GB ストレージ、GPU なし) をお勧めします。
2. CIのターミナルを開き、次のコマンドを実行します。 
    ```shell
    git clone https://github.com/Azure/slm-innovator-lab.git
    cd slm-innovator-lab && conda activate azureml_py310_sdkv2
    pip install -r requirements.txt
    ```

## ハンズオンラボ

### [Lab 1. データ準備](1_synthetic-qa-generation)
### [Lab 2. LLMの微調整と提供](2_slm-fine-tuning-mlstudio)
### [Lab 3. LLMOpsの](3_llmops-aistudio)

## 参照

<details markdown="block">
<summary>Expand</summary>

### データ準備
- [Evolve-Instruct](https://arxiv.org/pdf/2304.12244)
- [GLAN (一般化命令チューニング)](https://arxiv.org/pdf/2402.13064)
- [Auto Evolve-Instruct](https://arxiv.org/pdf/2406.00770)
- [Azure Machine Learning の例](https://github.com/Azure/azureml-examples)

### SLMの微調整

#### Phi-3/Phi-3.5
- [Azure ML を使用した Small Language Model (SLM) Phi-3 の微調整](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/finetune-small-language-model-slm-phi-3-using-azure-machine/ba-p/4130399)
- [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct): これは Microsoft の公式 Phi-3-mini-4k-instruct モデルです。
- [microsoft/Phi-3-mini-128k-instruct](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct): これは Microsoft の公式 Phi-3-mini-128k-instruct モデルです。
- [microsoft/Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct): これは Microsoft の公式 Phi-3.5-mini-instruct モデルです。
- [microsoft/Phi-3.5-MoE-instruct](https://huggingface.co/microsoft/Phi-3.5-MoE-instruct): これは Microsoft の公式 Phi-3.5-MoE-instruct モデルです。
- [KMMLU、CLIcK、HAE-RAEデータセットを用いたLLM/SLMモデルの韓国語能力評価](https://github.com/daekeun-ml/evaluate-llm-on-korean-dataset)
- [daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1](https://huggingface.co/daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1)

#### Florence-2 
- [Azure ML Python SDK と MLflow を使用した VQA (Visual Question Answering) の Florence-2 の微調整](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/fine-tuning-florence-2-for-vqa-visual-question-answering-using/ba-p/4181123)
- [Hugging Face Blog - Finetune Florence-2 on DoCVQA](https://huggingface.co/blog/finetune-florence2)

### LLMOps
- [LLMOps with Prompt フロー (AI Studio と Azure Machine Learning の両方をサポート)](https://github.com/microsoft/llmops-promptflow-template)

</details>

## 貢献

このプロジェクトは、貢献と提案を歓迎します。 ほとんどのコントリビューションでは、同意する必要があります。
コントリビューターライセンス契約(CLA)は、お客様が当社に付与する権利を有し、実際に付与することを宣言します。
あなたの投稿を使用する権利。詳しくは https://cla.opensource.microsoft.com をご覧ください。

プルリクエストを送信すると、CLAボットが自動的に提供する必要があるかどうかを判断します
CLA を作成し、PR を適切に装飾します (ステータス チェック、コメントなど)。指示に従うだけです
ボットによって提供されます。この操作は、CLA を使用してすべてのリポジトリで 1 回だけ行う必要があります。

このプロジェクトでは、[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/) を採用しています。
詳細については、[行動規範に関するFAQ](https://opensource.microsoft.com/codeofconduct/faq/)または
[ 追加の質問やコメントがある場合は](mailto:opencode@microsoft.com)、opencode@microsoft.com にお問い合わせください。

## 商標

このプロジェクトには、プロジェクト、製品、またはサービスの商標またはロゴが含まれている場合があります。Microsoft の許可された使用
商標またはロゴは、
[Microsoft の商標およびブランド ガイドライン](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)。
このプロジェクトの変更されたバージョンで Microsoft の商標またはロゴを使用することは、混乱を引き起こしたり、Microsoft のスポンサーシップを暗示したりしてはなりません。
第三者の商標またはロゴの使用は、それらの第三者のポリシーの対象となります。

## ライセンスの概要

このサンプル コードは、MIT-0 ライセンスの下で提供されています。LICENSE ファイルを参照してください。

[SLMイノベーターラボ]: https://github.com/Azure/slm-innovator-lab
[Azure OpenAI]: https://oai.azure.com/
[Azure ML]: https://ml.azure.com/
[Azure AI スタジオ]: https://ai.azure.com/
[Azure の GenAI エコシステム]: https://azure.microsoft.com/en-us/products/machine-learning/generative-ai
[ラボ1。データ準備]: https://azure.github.io/slm-innovator-lab/1_synthetic_data/
[ラボ 2.微調整と提供]: https://azure.github.io/slm-innovator-lab/2_fine-tuning/
[ラボ 3.LLMOpsの]: https://azure.github.io/slm-innovator-lab/3_llmops-aistudio/README.html
[Standard_DS11_v2]: https://learn.microsoft.com/azure/virtual-machines/sizes/memory-optimized/dv2-dsv2-series-memory
[Standard_E2as_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/memory-optimized/easv4-series
[Standard_NC24ads_A100_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nca100v4-series?tabs=sizebasic
[Standard_NC6s_v3]: https://learn.microsoft.com/azure/virtual-machines/sizes/gpu-accelerated/ncv3-series?tabs=sizebasic
[低優先度 VM]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-optimize-cost?view=azureml-api-2#low-pri-vm

[^1]: この追加のクォータは、OS のアップグレードや VM の復旧など、システムが開始する操作用に予約されており、そのような操作が実行されない限り、コストは発生しません。