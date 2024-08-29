#!/bin/bash

set -e

# Run sudo commands as root
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:alex-p/tesseract-ocr5 -y
sudo apt-get update -y
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-eng tesseract-ocr-kor -y
sudo apt-get install libgl1-mesa-glx libglib2.0-0 -y
sudo apt-get install libreoffice -y

# Switch to azureuser and run the rest of the commands
sudo -u azureuser bash <<'EOF'
source ~/.bashrc

# Find and source conda initialization script

CONDA_DIR=/anaconda
source "$CONDA_DIR/etc/profile.d/conda.sh"

ENVIRONMENT=azureml_py310_sdkv2
conda activate "$ENVIRONMENT"

pip install --upgrade pip
pip install -U unstructured[all-docs]
pip install -r requirements.txt

EOF