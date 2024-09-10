---
layout: default
title: Lab 3.4.1 Content Safety with Azure AI studio before production (KR)
permalink: /3_4_contentfilter_kr/
parent: Lab 3.4 Overview
---

# Lab 3.4 Content Safety with Azure AI studio before production

![LLMOps](images/content_filtering_api_support.jpg)
[Annotation availability in each API version](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cuser-prompt%2Cpython-new#:~:text=See%20the%20following%20table%20for%20the%20annotation%20availability%20in%20each%20API%20version%3A)

### Prerequisites

- An Azure subscription where you can create an AI Hub and AI project Resource
- Registered the Fine-tune model and deployed LLMs in Azure AI Studio


### Task

- I want to evaluate content filtering problematic answers to customer for the production
- I want to operate dev / staging / production with safe rollout processes 
- I want to monitor the service with metrics for the risk and cost management  


### TOC
- 1️⃣ Test your training dataset using content safety
- 2️⃣ Configure the content filter for your orchestration flows
- 3️⃣ Create a custom blocklist to manage inappropriate content
- 4️⃣ monitor the deployed application with metrics

### 1️⃣ Test your training dataset using content safety
1. Go to the Azure AI Studio > AI Services > Content Safety