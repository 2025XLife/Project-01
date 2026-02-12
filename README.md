<p align="center">
  <img src="./src/X-Life_large.png" width="200" alt="X-Life System Logo">
</p>

<div align="center">
</div>

## A metabolic world model system for personalised lifestyle medicine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &nbsp; [![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/) &nbsp; [![PyTorch 2.6](https://img.shields.io/badge/PyTorch-2.6-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/) &nbsp; [![Paper](https://img.shields.io/badge/Paper-Read_Manuscript-success)](placeholder) &nbsp; [![BibTeX](https://img.shields.io/badge/BibTeX-Citation-lightgrey)](#citation)


X-Life is a multimodal framework capable of integrating continuous glucose monitoring (CGM), wearable sensor signals, self-reported behavioural information and contextual metadata  to deliver personalized lifestyle prescriptions in real time. 
<!-- [[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/license/mit) | Python Version | [`Paper`](placeholder) | [[`BibTeX`](#Citation)]| Pytorch] -->
---

## Table of Contents
- [A metabolic world model system for personalised lifestyle medicine](#a-metabolic-world-model-system-for-personalised-lifestyle-medicine)
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Prerequisites \& Installation](#prerequisites--installation)
- [Core Modules Usage](#core-modules-usage)
  - [1. Metabolic World Model](#1-metabolic-world-model)
  - [2. Knowledge-Graph Guided Agents](#2-knowledge-graph-guided-agents)
    - [Knowledge-Graph Configuration](#knowledge-graph-configuration)
    - [Setup Knowledge Graph](#setup-knowledge-graph)
    - [Test Generation \& Assessment Pipelines](#test-generation--assessment-pipelines)
    - [Start Flask service:](#start-flask-service)
  - [3. AR Deployment](#3-ar-deployment)
    - [Download Link](#download-link)
    - [Deployment](#deployment)
  - [4. Omics Integration](#4-omics-integration)
    - [Omics Data Preparation](#omics-data-preparation)
    - [Training Model](#training-model)
    - [Evaluate Model](#evaluate-model)
- [Data Availability](#data-availability)
  - [Hardware Ecosystem](#hardware-ecosystem)
- [Citation](#citation)

---
## Overview

This repository contains code, package and sample dataset for the paper "A metabolic world model system for personalised lifestyle medicine".

## Prerequisites & Installation
- **Software Dependencies**: Python 3.10, Pytorch 2.6, JDK-17.0.18, Unity3D [Version]
- **Hardware Requirements**: NVIDIA A800 (for training), Windows 10 (for AR)
- **Environment Setup**:

1. Clone the repository:
```bash
git clone git@github.com:2025XLife/Project-01.git
cd Project-01
```

2. Create and activate the environment (
We recommend using `conda` to manage the environment and dependencies):
```bash
conda create -n xlife python=3.10 -y
conda activate xlife
```


3. Install python dependencies:
```bash
pip install -r requirements.txt
```


4. Install Neo4j Service:
```bash
# Install JDK
sudo apt install openjdk-11-jdk
# check the version of the installed JDK
java -version
```

Download the latest Neo4j tarball from [Neo4j Deployment Center](https://neo4j.com/deployment-center/?gdb-selfmanaged) and start the service:
```bash
tar zxf neo4j-community-5.26.21-unix.tar.gz
cd neo4j-community-5.26.21/bin/
./neo4j start
```

## Core Modules Usage

### 1. Metabolic World Model

The **Metabolic World Model (MWM)** is a Time-Series Transformer-based simulation engine trained on over 460 million CGM time-points. Functioning as a metabolic "digital twin," it tracks continuous latent states to perform counterfactual inference, enabling the precise simulation and evaluation of physiological responses to potential diet and exercise interventions.


1. Data Preparation.
Prepare the user metadata and physiological trajectory in the following format:
```bash
```
Prepare the diet images in the following folder:
```
```
1. Training Model
```bash
cd metabolic_world_model/
```
1. Evaluate Model
```bash
```

### 2. Knowledge-Graph Guided Agents

The Knowledge-Graph Guided Agents `./kg_agents/` generate personalized diet and exercise prescriptions by grounding LLM outputs in a hybrid vector-graph metabolic knowledge base, safeguarded by a security module that enforces clinical safety through semantic auditing and deterministic constraints.


#### Knowledge-Graph Configuration
Configure Neo4j database, remote LLM API and local models in `./kg_agents/config.json`:
```json
{
    "neo4j": { # Neo4j configuration
        "uri": "bolt://127.0.0.1:7687",
        "username": "your_username",
        "password": "your_password"
    },
    "api_model": { # Remote LLM API for knowledge graph setup
        "api_key": "your_api_key",
        "base_url": "your_base_url",
        "model": "your_api_model"
    },
    "local_model_path": "your_local_LLM_path", # Local LLM path for generation
    "local_emb_path": "your_local_embedding_model_path" # Local Embedding model path for RAG
}
```

#### Setup Knowledge Graph
1. Prepare guidelines following the descriptions in our paper.
```bash
.
├── data/
│   ├── diet/
│   │   ├── diet_guideline_1.pdf
│   │   └── ...
│   │
│   └── exer/
│       ├── exer_guideline_1.pdf
│       └── ...
```
Extract and embed entities (Make sure the Neo4j server has started):
```bash
cd kg_agents
# Extract knowledge from ./data
python -m core.build_kg
# Import knowledge graph
python -m core.import_kg
# (Optional) Embedding knowledge graph
python -m core.embed_kg
```


#### Test Generation & Assessment Pipelines
```bash
# Test diet prescription pipeline
python -m pipeline.diet_pipeline --bn 1 --vn 5 --query "I want a sandwich with just veggies, no meat." --use_vector --rag_topk 5
# Test exer prescription pipeline
python -m pipeline.exer_pipeline --bn 1 --vn 4 --query "I want to do some back exercises at the gym." --use_vector --rag_topk 5
```
Pipeline Arguments:
- `--bn`: Number of base plans to generate by LLM.
- `--vn`: Number of variants per base plan.
- `--query`: User user preference query.
- `--use_vector`: Enable vector-based GraphRAG.
- `--rag_topk`: Number of top-K results to retrieve from GraphRAG.


#### Start Flask service:
```bash
python server.py
```
Test service interfaces:
```bash
# diet prescriptions generation
curl -X POST http://localhost:5000/api/v1/diet/generate-only -H "Content-Type: application/json" -d '{args}'
# exercise prescriptions generation
curl -X POST http://localhost:5000/api/v1/exercise/generate-only -H "Content-Type: application/json" -d '{args}'
# security module assess prescription
curl -X POST http://localhost:5000/api/v1/safety/evaluate -H "Content-Type: application/json" -d '{
    "plan_type": "diet/exercise",
    "user_metadata": {detailed_metadata},
    "plan": {plan_to_assess}
}'
```


### 3. AR Deployment

#### Download Link
To deploy the AR system, download our compiled package from google drive [AR package](https://drive.google.com/file/d/1wsCSKbhp4-D_9PP9yDsjLwHc_rho2jWU/view?usp=sharing), and install it on (写好系统版本):

#### Deployment
```bash
cd ar_deployment/
```


### 4. Omics Integration
(这块可能需要按照组学代码修改，这里我让AI乱写的)
As a supplementary layer for enhanced personalization, X-Life supports the integration of multi-omics data. The system can ingest **gut microbiome profiles** and **metabolomics data** to refine its predictive accuracy. By correlating specific bacterial strains (e.g., *P. copri*) and metabolic markers with glycemic responses, the model can tailor interventions to the user's unique biological microbiome signature.

#### Omics Data Preparation
```bash
```
#### Training Model
```bash
cd omics_model/
```
#### Evaluate Model
```bash
```

## Data Availability
X-Life was trained on a dataset comprising 1.28 million lifestyle records and 0.46 billion continuous glucose monitoring (CGM) readings, collected from 834,360 individuals across multiple cohorts in China and the UK. The complete training corpus underlying the Metabolic World Model is accessible to researchers upon formal application to the respective cohort management committees, subject to applicable data privacy regulations and institutional approvals.

A minimal, de-identified sample dataset containing representative CGM traces and structured lifestyle logs is available at `src/sample_data_placeholder.zip`.. The sample is specifically formatted for computational compatibility with the X-Life preprocessing and modeling pipelines, enabling code verification and functional demonstration. It is intended exclusively for testing and development purposes. Use of this sample for clinical inference, biomedical research, or any generalizable conclusion is strictly discouraged.

To train and evaluate the model, run:
```bash
cd metabolic_world_model
mv ../src/sample_data_placeholder.zip data/sample_data.zip
unzip -d data/ data/sample_data.zip
python ...
```

### Hardware Ecosystem
* CGM sensor (SIBIONICS CGM)
* Fit Bands that provide sleep analysis and heart rate monitoring. 
* XREAL One Pro (XREAL, China) 

## Citation
```bibtex
@article{XLife2026,
  title = {X-Life: A metabolic world model system for personalised lifestyle medicine},
  author = {Wu, Qian and Qin, Yiming and et al.},
  journal = {},
  year = {2026}
}
```
