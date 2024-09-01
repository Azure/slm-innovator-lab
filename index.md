---
nav_order: 1
---
# SLM Innovator Lab

Unlock the full potential of your AI projects with the SLM Innovator Lab, powered by the Azure AIML Platform. Our lab is tailored for customers who excel in fine-tuning and deploying multiple SLM models on Azure, as well as those aiming to optimize base model performance through fine-tuning to create RAG applications. With the advanced capabilities of AI Studio, you can establish efficient and scalable LLMOps.

This hands-on lab is suitable for the following purposes:

1. 1-day workshop / 2-day workshop
2. Hackathon starter code
3. Reference guide for SLM fine-tuning&serving PoC/Prototype

## Requirements
Before starting, you have met the following requirements:

- [Access to Azure OpenAI Service](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure ML getting started](https://github.com/Azure/azureml-examples/tree/main/tutorials): Connect to Azure ML workspace and get your <WORKSPACE_NAME>, <RESOURCE_GROUP> and <SUBSCRIPTION_ID>.
- [Azure AI Studio getting started](https://aka.ms/azureaistudio): Create a project
- [Azure AI Document Intelligence (v4.0 - 2024-02-29 preview)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

- ***[Compute instance - for code development]*** A low-end instance without GPU is recommended: `Standard_DS11_v2` (2 cores, 14GB RAM, 28GB storage, No GPUs).
- ***[Compute cluster - for LLM training]*** A single NVIDIA A100 GPU node (`Standard_NC24ads_A100_v4`) and a single NVIDIA V100 GPU node (`Standard_NC6s_v3`) is recommended. If you do not have a dedicated quota or are on a tight budget, choose Low-priority VM.

Please do not forget to modify the `.env` file to match your account. Rename `.env.sample` to `.env` or copy and use it

## How to get started 
1. Create your compute instance in Azure ML Studio. For code development, we recommend `Standard_DS11_v2` (2 cores, 14GB RAM, 28GB storage, No GPUs).
2. Open the terminal of the CI and run: 
    ```shell
    git clone https://github.com/Azure/slm-innovator-lab.git
    conda activate azureml_py310_sdkv2
    pip install -r requirements.txt
    ```

## Table of contents

### [Lab 1. Data preparation](1_synthetic-qa-generation)
### [Lab 2. LLM fine-tuning and serving](2_slm-fine-tuning-mlstudio)
### [Lab 3. LLMOps](3_llmops-aistudio)

## References

### Data preparation
- [Evolve-Instruct](https://arxiv.org/pdf/2304.12244)
- [GLAN (Generalized Instruction Tuning)](https://arxiv.org/pdf/2402.13064)
- [Auto Evolve-Instruct](https://arxiv.org/pdf/2406.00770)
- [Azure Machine Learning examples](https://github.com/Azure/azureml-examples)

### SLM fine-tuning
- [Azure Machine Learning examples](https://github.com/Azure/azureml-examples)
- [Finetune Small Language Model (SLM) Phi-3 using Azure ML](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/finetune-small-language-model-slm-phi-3-using-azure-machine/ba-p/4130399)
- [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct): This is Microsoft's official Phi-3-mini-4k-instruct model.
- [daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1](https://huggingface.co/daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1)
- [Hugging Face Blog - Finetune Florence-2 on DoCVQA](https://huggingface.co/blog/finetune-florence2)

### LLMOps
- [LLMOps with Prompt flow (Supports both AI Studio and Azure Machine Learning](https://github.com/microsoft/llmops-promptflow-template)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

## License Summary

This sample code is provided under the MIT-0 license. See the LICENSE file.