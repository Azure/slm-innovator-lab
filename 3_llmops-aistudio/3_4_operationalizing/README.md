---
layout: default
title: Lab 3.4 Overview
permalink: /3_4_overview/
parent: Lab 3. LLMOps for SLM with Azure AI Studio
nav_order: 64
has_children: true
---

[日本語](README_ja.md)

# Lab 3.4 Scenario 4: Content Safety with Azure AI studio before production

## Overview
In this lab, you will experience how to ensure production deployment using content filter. This content filtering system is powered by Azure AI Content Safety, and it works by running both the prompt input and completion output through an ensemble of classification models aimed at detecting and preventing the output of harmful content. Variations in API configurations and application design might affect completions and thus filtering behavior.


![LLMOps](images/operation_requirements.jpg)

### 🔨Limitations
The content filtering models have been trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality can vary. In all cases, you should do your own testing to ensure that it works for your application.

### 🥇Other Resources
Here are the reference architectures, best practices and guidances on this topic. Please refer to the resources below. 

- https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-approach-gen-ai
- https://github.com/Azure-Samples/llm-evaluation
