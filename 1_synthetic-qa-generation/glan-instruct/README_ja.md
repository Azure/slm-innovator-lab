---
layout: default
title: GLAN
permalink: /1_3_glan/
parent: Lab 1. Generate Synthetic QnAs from Real-world Data
nav_order: 4.3
---

[English](README.md)

# GLAN (Generalized Instruction Tuning) 

## 概要
GLANは、人間の知識と能力の体系的な分類法を使用して、さまざまな分野にわたる大規模な合成命令データを生成します。
これは、シードの例や既存のデータセットに頼らずに、ゼロからデータを生成する方法です。

GLANは、人間の学習システムの体系的な構造を模倣し、さまざまな分野や技術をカバーする幅広い指導データを生成します。特定の領域に限定されず、すべての分野にわたるさまざまなタスクを網羅できます。
この手法は、数学的推論、コーディング、学術的テスト、論理的推論など、多くの面で優れた性能を発揮し、特定の課題に対する学習データがなくても有効です。

## 実装
このオープンソースの実装は、論文 https://arxiv.org/pdf/2402.13064 の内容に基づいています。

### 主な機能
- `glan_instruction_generation()`: GLANパイプライン

### サブ機能
- `generate_taxonomy()`: 人間の知識と能力の分類法を生成します。分類法から派生した分野は、主題を作成するために使用されます。
GPTに自動でディシプリンを作成させることもできます(この場合は人間による検証が必要)、作成したディシプリン（`disciplines.txt`）を使用することもできます。
- `generate_subjects()`: 特定の分野の科目のリストを生成します。論文のセクション2.2を参照してください。
- `generate_syllabus()`: 特定の科目のシラバスを特定のレベルで生成します。論文のセクション2.3を参照してください。
- `sample_class_sessions_and_key_concepts()`:サンプルクラスセッションと主要な概念を使用して、さまざまな難易度の問題を生成します。
- `generate_questions()`: LangChain パイプラインを使用して、クラス セッションと主要な概念に基づいて質問を生成します。論文のセクション2.4を参照してください。
- `generate_answers()`: LangChain パイプラインを使用して質問に対する回答を生成します。論文のセクション2.4を参照してください。


## データセットの作成方法
サンプルデータセットは、この[フォルダ](samples)に配置されます。最初に最小限の例を試し、調整可能なパラメーターを参照してデータセットを構成してください。

### 例

テスト用のデバッグ - パラメーターを変更する必要があります
```shell
chmod +x run_debug.sh
./run_debug.sh
```

各分野に対して大量のデータを生成する (推奨)
```shell
chmod +x run_each_discipline.sh
./run_each_discipline.sh
```

大量のデータを生成する
```shell
chmod +x run.sh
./run.sh
```


### 調整可能なパラメータ

#### QnA ジェネレーション
詳細については、 `generate.py` を参照してください。

```python
parser.add_argument("--generate_disciplines", type=bool, default=False)
parser.add_argument("--generate_question_only", type=bool, default=False)

parser.add_argument("--disciplines_filepath", type=str, default="disciplines_sample.txt")
parser.add_argument("--language", type=str, default="Korean")
parser.add_argument("--model_name", type=str, default="gpt-4o")
parser.add_argument("--model_name_for_answer", type=str, default="gpt-4o")

parser.add_argument("--max_number_of_fields", type=int, default=1)
parser.add_argument("--max_number_of_subjects", type=int, default=2)
parser.add_argument("--max_number_of_subtopics", type=int, default=5)
parser.add_argument("--max_number_of_session_name", type=int, default=3)

parser.add_argument("--num_iterations", type=int, default=2)
parser.add_argument("--num_questions_per_iteration", type=int, default=5)

parser.add_argument("--question_max_tokens", type=int, default=768)
parser.add_argument("--question_batch_size", type=int, default=5)
parser.add_argument("--answer_max_tokens", type=int, default=2048)
parser.add_argument("--answer_batch_size", type=int, default=5)

parser.add_argument("--output_dir", type=str, default="outputs")
parser.add_argument("--logfile_name", type=str, default="logfile.log")
```

#### 回答の生成
詳細については、`generate_answer_only.py` を参照してください。

```
parser.add_argument("--questions_filepath", type=str, default="[YOUR JSONL]")
parser.add_argument("--model_name_for_answer", type=str, default="gpt-4o")
parser.add_argument("--answer_max_tokens", type=int, default=2048)
parser.add_argument("--answer_batch_size", type=int, default=5)
```