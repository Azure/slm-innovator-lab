# SLM Innovator Lab

Unlock the full potential of your AI projects with the SLM Innovator Lab, powered by the Azure AI/ML Platform. Our lab is tailored for customers who excel in fine-tuning and deploying multiple SLM models on Azure, as well as those aiming to optimize base model performance through fine-tuning to create RAG applications. With the advanced capabilities of AI Studio, you can establish efficient and scalable LLMOps.

This hands-on lab is suitable for the following purposes:

1. 1-day workshop (4-7 hours depending on customer) / 2-day workshop with LLMOps hands-on
2. Hackathon starter code
3. Reference guide for SLM fine-tuning&serving PoC/Prototype

Hands-on guide: https://azure.github.io/slm-innovator-lab/

## New content (25-Oct-2024)
🔥LLMOps with promptflow python SDK<br>
In this hands-on, you will learn how to create a new flow, define the chat flow structure, and integrate the fine-tuned model endpoint using Python SDK. You will also learn how to compare and evaluate the model's performance using the flows. This is in addition to the hands-on that was previously available based on the Azure AI Studio UI. 
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/3_llmops-aistudio/3_2_prototyping/promptflow_with_code.ipynb">Go to notebook</a>
<br><br>
🔥Microsoft Olive model optimization <br>
Microsoft Olive is a hardware-aware AI model optimization toolchain developed by Microsoft to streamline the deployment of AI models. Olive simplifies the process of preparing AI models for deployment by making them faster and more efficient, particularly for use on edge devices, cloud, and various hardware configurations. This hands-on considers on-device or hybrid deployment scenarios.
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/2_slm-fine-tuning-mlstudio/phi3/3_optimization_olive.ipynb">Go to notebook</a>
<br><br>
🔥Content Safety with python SDK<br>
In this hands-on, you will be able to: manage text blocklist, analyze text and images for sexual content, violence, hate, and self-harm with multi-severity levels. You will also learn how to integrate with Azure Open AI Service: Use the Azure Open AI Service to rewrite the content for harmful content.
<br>
<a href="https://github.com/Azure/slm-innovator-lab/blob/main/3_llmops-aistudio/3_4_operationalizing/contentsafety_with_code.ipynb">Go to notebook</a>

## Requirements
Before starting, you should meet the following requirements:

- [Access to Azure OpenAI Service](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure ML getting started](https://github.com/Azure/azureml-examples/tree/main/tutorials): Connect to [Azure ML] workspace and get your <WORKSPACE_NAME>, <RESOURCE_GROUP> and <SUBSCRIPTION_ID>.
- [Azure AI Studio getting started](https://aka.ms/azureaistudio): Create a project
- [Azure AI Document Intelligence (v4.0 - 2024-02-29 preview)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)

- ***[Compute instance - for code development]*** A low-end instance without GPU is recommended: **[Standard_E2as_v4] (AMD 2 cores, 16GB RAM, 32GB storage) or **[Standard_DS11_v2]** (Intel 2 cores, 14GB RAM, 28GB storage, No GPUs)  
- ***[Compute cluster - for SLM/LLM fine-tuning]*** A single NVIDIA A100 GPU node (**[Standard_NC24ads_A100_v4]**) is recommended. If you do not have a dedicated quota or are on a tight budget, choose **[Low-priority VM]**.
- ***[Compute cluster - for SLM/LLM deployment]*** A single NVIDIA V100 GPU node (**[Standard_NC6s_v3]**) or A single NVIDIA A100 GPU node (**[Standard_NC24ads_A100_v4]**) is recommended.

In case you don't have any of the above requirements ready yet, please go to Lab preparation first.
### [Lab 0. Lab preparation](0_lab_preparation)

**Please do not forget to modify the `.env` file to match your account. Rename `.env.sample` to `.env` or copy and use it**

## Cautions
This workshop assumes that you are configuring in a public environment and you have access to the internet. If you are configuring in a private environment, you may need to set up a private network to access the services. The following are some common issues you may encounter when you configure in a private environment:
- If you set up the [Azure ML] workspace and [Azure AI Studio] in private network, you may need to set up a VPN or a private link to access the services.
- If you are using a low-priority VM, you may need to wait for the VM to be available. The availability of the VMs may vary by region.
- If you have blob storage, you can use it to store the data and models. However, you may need to set up the connection to the blob storage in the [Azure ML] workspace.
- If you have a quota issue, you may need to request a quota increase for the VMs or GPUs.
- Once you configure the network in [Azure ML] workspace, you can not change it. You may need to create a new workspace if you want to change the network.
- If you are using a compute instance which is not in the same region as the [Azure ML] workspace, you may need to set up a VPN or a private link to access the services.
- If you are using a compute instance which created in [Azure AI Studio], you can't execute training jobs in the compute instance. You may need to create a new compute instance in [Azure ML] workspace.
- If you run into an PermissionMismatch error when you download the artifacts, you may need to asign the correct permission to the [Azure ML] workspace.

## How to get started 
1. Create your compute instance in [Azure ML]. For code development, we recommend **[Standard_DS11_v2]** (2 cores, 14GB RAM, 28GB storage, No GPUs).
2. Open the terminal of the CI and run: 
    ```shell
    git clone https://github.com/Azure/slm-innovator-lab.git
    cd slm-innovator-lab && conda activate azureml_py310_sdkv2
    pip install -r requirements.txt
    ```

## Hands-on Labs

### [Lab 1. Data preparation](1_synthetic-qa-generation)
### [Lab 2. LLM fine-tuning and serving](2_slm-fine-tuning-mlstudio)
### [Lab 3. LLMOps](3_llmops-aistudio)

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

[SLM Innovator Lab]: https://github.com/Azure/slm-innovator-lab
[Azure OpenAI]: https://oai.azure.com/
[Azure ML]: https://ml.azure.com/
[Azure AI Studio]: https://ai.azure.com/
[GenAI ecosystem in Azure]: https://azure.microsoft.com/en-us/products/machine-learning/generative-ai
[Lab 1. Data preparation]: https://azure.github.io/slm-innovator-lab/1_synthetic_data/
[Lab 2. Fine-tuning and serving]: https://azure.github.io/slm-innovator-lab/2_fine-tuning/
[Lab 3. LLMOps]: https://azure.github.io/slm-innovator-lab/3_llmops-aistudio/README.html
[Standard_DS11_v2]: https://learn.microsoft.com/azure/virtual-machines/sizes/memory-optimized/dv2-dsv2-series-memory
[Standard_E2as_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/memory-optimized/easv4-series
[Standard_NC24ads_A100_v4]: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nca100v4-series?tabs=sizebasic
[Standard_NC6s_v3]: https://learn.microsoft.com/azure/virtual-machines/sizes/gpu-accelerated/ncv3-series?tabs=sizebasic
[Low-priority VM]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-optimize-cost?view=azureml-api-2#low-pri-vm