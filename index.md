---
layout: home
title: SLM Innovator Lab
nav_order: 1
permalink: /
---
# SLM Innovator Lab
{: .no_toc }

[Agenda](#agenda){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub][SLM Innovator Lab]{: .btn .fs-5 .mb-4 .mb-md-0 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. Overview

Unlock the full potential of your AI projects with the [SLM Innovator Lab], powered by the Azure AIML Platform. Our lab is tailored for customers who excel in fine-tuning and deploying multiple SLM/LLM models on Azure, as well as those aiming to optimize base model performance through fine-tuning to create RAG applications. With the advanced capabilities of [AI Studio], you can establish efficient and scalable LLMOps.

This hands-on lab is suitable for the following purposes:

1. 1-day workshop (4-7 hours depending on customer) / 2-day workshop with LLMOps hands-on
2. Hackathon starter code
3. Reference guide for SLM fine-tuning&serving PoC/Prototype

## 2. Prerequisites

{: .note}
Please do not forget to modify the `.env` file to match your account. Rename `.env.sample` to `.env` or copy and use it

Before starting, you have met the following requirements:

- [Access to Azure OpenAI Service](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure ML getting started](https://github.com/Azure/azureml-examples/tree/main/tutorials): Connect to Azure ML workspace and get your `<WORKSPACE_NAME>`, `<RESOURCE_GROUP>` and `<SUBSCRIPTION_ID>`.
- [Azure AI Studio getting started](https://aka.ms/azureaistudio): Create a project
- [Azure AI Document Intelligence (v4.0 - 2024-02-29 preview)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

- ***[Compute instance - for code development]*** A low-end instance without GPU is recommended: **[Standard_DS11_v2]** (2 cores, 14GB RAM, 28GB storage, No GPUs).
- ***[Compute cluster - for SLM/LLM fine-tuning]*** A single NVIDIA A100 GPU node (**[Standard_NC24ads_A100_v4]**) is recommended. If you do not have a dedicated quota or are on a tight budget, choose **[Low-priority VM]**.
- ***[SLM/LLM deployment]*** Two NVIDIA V100 GPUs (**[Standard_NC6s_v3]**) or two NVIDIA A100 GPUs (**[Standard_NC24ads_A100_v4]**) are recommended. 

## 3. How to get started 
1. Create your compute instance in [Azure ML]. For code development, we recommend **[Standard_DS11_v2]** (2 cores, 14GB RAM, 28GB storage, No GPUs).
2. Open the terminal of the CI and run: 
    ```shell
    git clone https://github.com/Azure/slm-innovator-lab.git
    cd slm-innovator-lab && conda activate azureml_py310_sdkv2
    pip install -r requirements.txt
    ```

## 4. Agenda
- **[Background. Why Azure and Fine-tuning?]**: Before we get into the hands-on, we explain to participants exactly what the SLM Innovator Lab is all about and give them an overview of the [GenAI ecosystem in Azure]. 

- **[Lab 0. Requirements (Skip if you have already set up)]**: If you are not familiar with the Azure environment, be sure to check it out!

- **[Lab 1. Data preparation]**: Participants will dive into the critical first step of the GenAI pipeline. The session will focus on how to prepare data from real-world scenarios to create high-quality datasets necessary for fine-tuning models. Participants will learn how to process QnA (Questions & Answers) data and generate synthetic data to augment the training set, ensuring the model can handle a wide range of domain, including those in non-English languages. By the end of this lab, participants will have hands-on experience in transforming raw data into a format ready for effective AI model training. 

- **[Lab 2. Fine-tuning and serving]**: This lab guides participants through the process of fine-tuning SLMs and deploying them using [Azure ML]. The focus will be on simplifying the fine-tuning process, enabling participants to fine-tune pre-trained SLMs with their own datasets quickly and efficiently. The session will also demonstrate how to use Azure ML’s tools to serve these models as scalable APIs (Application Programming Interfaces), allowing them to be integrated into real-world applications with ease.  

- **[Lab 3. LLMOps]**: In this lab, participants will delve into the critical aspects of managing and optimizing SLMs within [Azure AI Studio], with a particular emphasis on content safety and model evaluation. As organizations increasingly deploy GenAI models in production environments, ensuring that these models operate safely and effectively is paramount. This lab provides participants with the critical skills needed to ensure that their LLMs are not only technically robust but also safe and aligned with the ethical and operational standards of their organizations 

- **Key takeaways**: The final session of the program will be a reflective and strategic discussion focused on the next steps in the participants' GenAI journey. After gaining hands-on experience, participants will have the opportunity to share their insights, challenges, and aspirations. This session will emphasize the importance of listening to the customer’s voice, understanding their specific needs, and collaboratively defining the next actions to move towards successful Proof of Concept (PoC), Minimum Viable Product (MVP), and full production deployments. The goal is to ensure that each participant leaves with a clear roadmap for their AI projects, aligned with their business objectives and supported by the technical capabilities they have developed during the program. 

## 5. Objectives
- **Platform Stickiness**: When customers are tuning SLMs using [Azure ML] and [AI Studio], they initially develop the SLM/LLMOps through AI Studio and tools like [Prompt flow], [LangChain], [LlamaIndex], or [Semantic Kernel]. This forms the initial approach for the SLM Innovator Lab. However, the primary goal is to migrate compute workloads to an Azure-native platform. Specifically, this involves integrating [Azure AKS] (containerization with multi-GPU node pools), [Azure Blob Storage], [Azure SQL Database], [Azure Data Lake], [Microsoft Fabric], [Azure Monitor] and [Log Analytics], while working closely with various technical support teams within Microsoft to address the anticipated challenges of launching into production. The hands-on experience shows the practical benefits of using [Azure ML] and [Azure AI Studio], encouraging long-term commitment to the platform. 

- **Ease of Use and Accessibility**: The lab is designed to lower the barriers to entry for customers interested in SLM/LLM fine-tuning. It simplifies the setup process by providing a pre-configured environment that omits the need for complex configurations, making it easier for customers to get started quickly. 

- **Earn trust**: The lab is designed to build and solidify customer trust throughout the GenAI journey, from Proof of Concept (PoC) to Minimum Viable Product (MVP) and to Production. By deeply engaging with customers to understand their unique requirements and challenges, and by collaboratively navigating the complexities of data preparation, model fine-tuning, serving, and evaluation, the SLM Innovator Lab ensures that customers see tangible results and feel confident in the partnership. This trust is crucial for successfully launching GenAI projects, as it fosters stronger relationships and collaboration, ensuring that both the customer's goals and technical needs are met at every stage of the project. The lab's success in earning this trust is key to achieving long-term success and deeper integration in AIML projects. 

## References

<details markdown="block">
<summary>Expand</summary>

### Data preparation
- [Evolve-Instruct](https://arxiv.org/pdf/2304.12244)
- [GLAN (Generalized Instruction Tuning)](https://arxiv.org/pdf/2402.13064)
- [Auto Evolve-Instruct](https://arxiv.org/pdf/2406.00770)
- [Azure Machine Learning examples](https://github.com/Azure/azureml-examples)

### SLM fine-tuning

#### Phi-3/Phi-3.5
- [Finetune Small Language Model (SLM) Phi-3 using Azure ML](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/finetune-small-language-model-slm-phi-3-using-azure-machine/ba-p/4130399)
- [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct): This is Microsoft's official Phi-3-mini-4k-instruct model.
- [microsoft/Phi-3-mini-128k-instruct](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct): This is Microsoft's official Phi-3-mini-128k-instruct model.
- [microsoft/Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct): This is Microsoft's official Phi-3.5-mini-instruct model.
- [microsoft/Phi-3.5-MoE-instruct](https://huggingface.co/microsoft/Phi-3.5-MoE-instruct): This is Microsoft's official Phi-3.5-MoE-instruct model.
- [Korean language proficiency evaluation for LLM/SLM models using KMMLU, CLIcK, and HAE-RAE dataset](https://github.com/daekeun-ml/evaluate-llm-on-korean-dataset)
- [daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1](https://huggingface.co/daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1)

#### Florence-2
- [Fine-tuning Florence-2 for VQA (Visual Question Answering) using the Azure ML Python SDK and MLflow](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/fine-tuning-florence-2-for-vqa-visual-question-answering-using/ba-p/4181123)
- [Hugging Face Blog - Finetune Florence-2 on DoCVQA](https://huggingface.co/blog/finetune-florence2)

### LLMOps
- [LLMOps with Prompt flow (Supports both AI Studio and Azure Machine Learning](https://github.com/microsoft/llmops-promptflow-template)

</details>

[SLM Innovator Lab]: https://github.com/Azure/slm-innovator-lab
[Azure OpenAI]: https://oai.azure.com/
[Azure ML]: https://ml.azure.com/
[Azure AI Studio]: https://ai.azure.com/
[AI Studio]: https://ai.azure.com/
[GenAI ecosystem in Azure]: https://azure.microsoft.com/en-us/products/machine-learning/generative-ai
[Background. Why Azure and Fine-tuning?]: https://azure.github.io/slm-innovator-lab/0_lab_preparation/why_finetune.html
[Lab 0. Requirements (Skip if you have already set up)]: https://azure.github.io/slm-innovator-lab/0_lab_preparation/README.html
[Lab 1. Data preparation]: https://azure.github.io/slm-innovator-lab/1_synthetic_data/
[Lab 2. Fine-tuning and serving]: https://azure.github.io/slm-innovator-lab/2_fine-tuning/
[Lab 3. LLMOps]: https://azure.github.io/slm-innovator-lab/3_llmops-aistudio/README.html
[Standard_DS11_v2]: https://learn.microsoft.com/azure/virtual-machines/sizes/memory-optimized/dv2-dsv2-series-memory
[Standard_NC24ads_A100_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nca100v4-series?tabs=sizebasic
[Standard_NC6s_v3]: https://learn.microsoft.com/azure/virtual-machines/sizes/gpu-accelerated/ncv3-series?tabs=sizebasic
[Low-priority VM]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-optimize-cost?view=azureml-api-2#low-pri-vm
[Prompt flow]: https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/overview-what-is-prompt-flow
[LangChain]: https://www.langchain.com/
[LlamaIndex]: https://www.llamaindex.ai/
[Semantic Kernel]: https://learn.microsoft.com/semantic-kernel/overview/
[Azure AKS]: https://learn.microsoft.com/azure/aks/
[Azure Blob Storage]: https://azure.microsoft.com/products/storage/blobs
[Azure SQL Database]: https://azure.microsoft.com/products/azure-sql/database
[Azure Data Lake]: https://azure.microsoft.com/solutions/data-lake
[Microsoft Fabric]: https://www.microsoft.com/en-us/microsoft-fabric
[Azure Monitor]: https://azure.microsoft.com/en-us/products/monitor
[Log Analytics]: https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-tutorial