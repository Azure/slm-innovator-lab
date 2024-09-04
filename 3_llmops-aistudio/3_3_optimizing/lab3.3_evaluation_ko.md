---
layout: default
title: Lab3.3 Evaluate your models using Prompt Flow to keep optimizing
permalink: /3_3_optimizing/
---

# Lab3.3 Evaluate your models using Prompt Flow to keep optimizing

## Overview
In this lab, you will explore your model in Azure AI studio and conduct A/B testing with your LLM nodes to evaluate the performance of prompt and LLM. You will learn how to create your variants which can help you test the model’s behavior under different conditions, such as different wording, formatting, context, temperature, or top-k, compare and find the best prompt and configuration that maximizes the model’s accuracy, diversity, or coherence.

![LLMOps](images/3.3_evaluation_sample.png)


### Prerequisites

- An Azure subscription where you can create an AI Hub and AI project Resource
- Registered the Fine-tune model and deployed LLMs in Azure AI Studio


### Task

- I want to quantitatively verify how well the model and RAG are answering questions 
- I want to benchmark in bulk data before production to find bottlenecks and improve 


### TOC
- 1️⃣ Manual evaluations to review outputs of the selected model
- 1️⃣ Create QnA Relevance Evaluation flow 
- 2️⃣ Review the QnA Relevance Evaluation flow 
- 3️⃣ View Test Result of the Evaluation flow
- 4️⃣ Automated evaluation for Korean and English math questions

### 1️⃣ Manual evaluations to review outputs of the selected model
1. Go to the Azure AI Studio and select the model you want to evaluate.
2. Click on the "Test" button to test the model with a prompt.
3. Review the output and check if the model is answering the question correctly.
4. Repeat the process with different prompts and check the model's performance.

### 2️⃣ Create QnA Relevance Evaluation flow  
1. Go to the Azure AI Studio and select the model you want to evaluate.
2. Click on the "Evaluation" tab to create an evaluation flow.
3. Create a QnA Relevance Evaluation flow with variants.
4. Review the Evaluation flow and variants.


### 3️⃣ View Test Result of the Evaluation flow
- 

### 4️⃣ Automated evaluation for Korean and English math questions
