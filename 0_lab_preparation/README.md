---
layout: default
title: Requirements (Skip if you have already set up)
nav_order: 2
---

## 1. Requirements
### Hands-on Requirements
- Ensure you have access to Azure OpenAI Service.
- Set up your Azure ML workspace and get your <WORKSPACE_NAME>, <RESOURCE_GROUP> and <SUBSCRIPTION_ID>.
- create a project in Azure AI Studio.
- Use a low-end compute instance(Standard_DS11_v2) without GPU is recommended. 
- For LLM training, recommend a single NVIDIA A100 node (Standard_NC24ads_A100_v4)  or NVIDIA V100 GPU node(Standard_NC6s_v3). 
- Opt for Low-priority VMs if on a budget or without a dedicated quota.

### Cautions
- If configuring in a private environment, set up a private network or VPN to access services.
- Low-priority VM availability may vary by region.
- Set up connections for any blob storage used to store data and models within the Azure ML workspace.
- Request a quota increase if necessary for VMs or GPUs.
- Network config in Azure ML workspace cannot be changed post-setup; create a new workspace if required.
- Ensure compute instances are in the same region as the Azure ML workspace; otherwise, set up a VPN or private link.
- If using Azure AI Studio compute instances, note that training jobs cannot be executed on them.

Please ensure these points are followed to avoid common issues during the workshop.

## 2. Setup env file
Please do not forget to modify the `.env` file to match your account. Rename `.env.sample` to `.env` or copy and use it.
Modify the `.env` file to match Azure OpenAI Endpoint, OpenAI API key, AI Document Intelligence Endpoint, AI Document Intelligence Key, and other required details.

```shell
# .env
AZURE_OPENAI_ENDPOINT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation
OPENAI_API_VERSION=2024-05-01-preview
DEPLOYMENT_NAME=gpt-4o-mini

AZURE_DOC_INTELLIGENCE_ENDPOINT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_DOC_INTELLIGENCE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 3. Setup config.yml
Modify the `2_slm-fine-tuning-mlstudio/phi3/config.yml` file to match your Azure subscription, resource group, workspace, and data name. 


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
