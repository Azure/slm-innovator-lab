---
layout: default
title: Generate Coverage dataset (seed data)
permalink: /1_1_seed/
parent: Lab 1. Generate Synthetic QnAs from Real-world Data
nav_order: 4.1
---

# Generate Coverage dataset (seed data)

## 概要
タスクは、この異種データを前処理し、微調整またはRAGに適した構造化形式に変換することです。これには、さまざまなファイル形式からのテキストの抽出とクリーニング、必要に応じて Azure AI Services を使用したテーブルと画像のテキストへの変換が含まれます。このデータセットは、微調整やRAGのシードデータセットとして使用され、ドメイン固有のユースケースのパフォーマンスを向上させるためのベースラインとして使用されます。

{: .note}
この実装は、アイデア出しのベースラインにすぎず、本番環境のベースラインではありません。独自のデータ用にコードをカスタマイズする必要があります。

## はじめ

![図1](../imgs/diagram1.png)

与えられた生データを、Azure OpenAI GPT-4o を使用したモデルのトレーニング/RAG/評価に使用できるデータに変換します。 `make_qa_multimodal_pdf_docai.ipynb` が最も推奨されます。ただし、このコードのロジックが複雑だと感じた場合や、ファイルの内容が画像やテキストのみで構成されている場合は、まず他の Jupyter Notebook を試してみてください。
シード フォルダーで Jupyter ノートブックを実行します **[](seed)** 。

#### PDFで見る
- `make_qa_multimodal_pdf_docai.ipynb`: (推奨) Azure AI Document Intelligence を使用して、複雑な PDF から QnA 合成データセットを生成します。
- `make_qa_multimodal_pdf_oss.ipynb`: オープンソースを使用して、複雑な PDF から QnA 合成データセットを生成します (このハンズオン用の非構造化ツールキット)。このファイルを実行するには、まず必要なパッケージを `startup_unstructured.sh`.インストールには数分かかります。
- `make_qa_only_image_multiple_pdf.ipynb`: 複数の PDF から QnA 合成データセットを生成します - 画像の多い PDF。
- `make_qa_only_image_pdf.ipynb`: PDF から QnA 合成データセットを生成します - 画像の多い PDF。

#### CSVファイル
- `make_qa_csv.ipynb`: これは一般的なケースです。CSVLoader で読み取ってチャンクすることで QnA データセットを作成することは難しくありません。