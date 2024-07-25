# Lab 2. SLM/LLM Fine-tuning on Azure ML Studio

This hands-on walks you through fine-tuning an open source LLM on Azure and serving the fine-tuned model on Azure. It is intended for Data Scientists and ML engineers who have experience with fine-tuning but are unfamiliar with Azure ML and Mlflow.

## Use cases

- ### [Phi-3 Fine-tuning](phi3)

- ### [Florence-2 Fine-tuning on DoCVQA](florence2-VQA)

## How to get started 
1. Create your compute instance. For code development, we recommend `Standard_DS11_v2` (2 cores, 14GB RAM, 28GB storage, No GPUs).
2. Open the terminal of the CI and run: 
    ```shell
    git clone https://github.com/Azure/azure-llm-fine-tuning.git
    conda activate azureml_py310_sdkv2
    pip install -r requirements.txt
    ```
3. Choose the model to use for your desired use case.
    - [Phi-3](phi3)
        - [Option 1. MLflow] Run `1_training_mlflow.ipynb` and `2_serving.ipynb`, respectively.
        - [Option 2. Custom] Run `1_training_custom.ipynb` and `2_serving.ipynb`, respectively.
        - *(Optional)* If you are interested in LLM dataset preprocessing, see the hands-ons in `phi3/dataset-preparation` folder.
    - [Florence2-VQA](florence2-VQA)
        - Run `1_training_mlflow.ipynb` and `2_serving.ipynb`, respectively.
    - Don't forget to edit the `config.yml`.

## References

- [Azure Machine Learning examples](https://github.com/Azure/azureml-examples)

### Phi-3
- [Finetune Small Language Model (SLM) Phi-3 using Azure ML](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/finetune-small-language-model-slm-phi-3-using-azure-machine/ba-p/4130399)
- [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct): This is Microsoft's official Phi-3-mini-4k-instruct model.
- [daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1](https://huggingface.co/daekeun-ml/Phi-3-medium-4k-instruct-ko-poc-v0.1)

### Florence-2
- [Hugging Face Blog - Finetune Florence-2 on DoCVQA](https://huggingface.co/blog/finetune-florence2)
