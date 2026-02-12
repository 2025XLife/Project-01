<p align="center">
  <img src="./src/xlife.png" width="300" alt="X-Life System Logo">
</p>

<div align="center">
</div>

## X-Life

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &nbsp; [![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/) &nbsp; [![PyTorch 2.6](https://img.shields.io/badge/PyTorch-2.6-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/) &nbsp; [![Paper](https://img.shields.io/badge/Paper-Read_Manuscript-success)](placeholder) &nbsp; [![BibTeX](https://img.shields.io/badge/BibTeX-Citation-lightgrey)](#citation)


X-Life is a multimodal framework capable of integrating continuous glucose monitoring (CGM), wearable sensor signals, self-reported behavioural information and contextual metadata  to deliver personalized lifestyle prescriptions in real time. 

## Table of Contents
- [X-Life](#x-life)
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Prerequisites \& Installation](#prerequisites--installation)
- [Core Modules Usage](#core-modules-usage)
  - [1. Metabolic World Model](#1-metabolic-world-model)
  - [2. Knowledge-Graph Guided Agents](#2-knowledge-graph-guided-agents)
  - [3. AR Deployment](#3-ar-deployment)
    - [1) Hardware / Platform](#1-hardware--platform)
    - [2) Software Environment (Recommended / Verified)](#2-software-environment-recommended--verified)
    - [3) Dependencies: What must be installed?](#3-dependencies-what-must-be-installed)
      - [A. Vuplex 3D WebView (Required, Not Included)](#a-vuplex-3d-webview-required-not-included)
      - [B. XREAL XR Plugin (Required, Already Configured)](#b-xreal-xr-plugin-required-already-configured)
      - [C. Unity Package Manager Dependencies (Auto-installed)](#c-unity-package-manager-dependencies-auto-installed)
    - [4) Project Setup (What You Need to Change Before Running)](#4-project-setup-what-you-need-to-change-before-running)
      - [4.1 Configure the WebView Initial URL](#41-configure-the-webview-initial-url)
      - [4.2 (Optional) Configure iFLYTEK Speech Recognition](#42-optional-configure-iflytek-speech-recognition)
    - [5) Build APK](#5-build-apk)
      - [5.1 Pre-build Checklist](#51-pre-build-checklist)
      - [5.2 Build Steps in Unity (Android)](#52-build-steps-in-unity-android)
      - [6) Troubleshooting](#6-troubleshooting)
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
- **Software Dependencies**: Python 3.10, Pytorch 2.6, JDK-17.0.18, Unity3D [2022.3.x]
- **Hardware Requirements**: NVIDIA A800 (for training),  Android 14+ (for AR)
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


1. Configure Neo4j database, remote LLM API and local models in `./kg_agents/config.json`:
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

2. Prepare guidelines following the descriptions in our paper.
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

3. Extract and embed entities (Make sure the Neo4j server has started):
```bash
cd kg_agents
# Extract knowledge from ./data
python -m core.build_kg_2_steps
# Import knowledge graph
python -m core.import_kg
# (Optional) Embedding knowledge graph
python -m core.embed_kg
```

> Test Generation & Assessment Pipelines

```bash
# Test diet prescription pipeline
python -m pipeline.diet_pipeline --bn 1 --vn 5 --query "I want a sandwich with just veggies, no meat." --use_vector --rag_topk 5
# Test exer prescription pipeline
python -m pipeline.exer_pipeline --bn 1 --vn 4 --query "I want to do some back exercises at the gym." --use_vector --rag_topk 5
```

5. Start Flask service:
```bash
python server.py
```

> Test service interfaces:

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

This Unity project targets **XREAL AR** devices to:
- Embed a web page as the main UI via **Vuplex 3D WebView** (WebView scene)
- Trigger **XREAL RGB Camera** capture / screen recording from the web page (camera capture scene)
- Send capture results (photos/videos, local file paths / local HTTP URLs, etc.) back to the web page via `postMessage`

#### 1) Hardware / Platform

- Target platform: Android
- Device: XREAL devices / runtimes that support XREAL XR Plugin (and any Android device that can install an APK)
- Debugging: USB cable + USB debugging enabled (required for Build & Run)

#### 2) Software Environment (Recommended / Verified)

- Unity: `2022.3.x` (this project uses `2022.3.61t8` in `ProjectSettings/ProjectVersion.txt`)
- Unity Hub modules: Android Build Support (SDK / NDK / OpenJDK)
- Optional: `adb` (usually not needed if you use Unity's Build & Run; needed for CLI install/debugging)
- Download: Please download the complete Unity project [XLIFE-AR.zip](https://drive.google.com/file/d/1Ul-z-lDQSRvFw9aqk6uxIVhMamKpvAJM/view?usp=sharing) 

#### 3) Dependencies: What must be installed?

> The two most common blockers are: **Vuplex (commercial, not included in the repo)** + **XREAL XR Plugin (provided as a local tar package)**.

##### A. Vuplex 3D WebView (Required, Not Included)

- Purchase and import (Unity Asset Store): [Vuplex 3D WebView for Android (with Gecko Engine)](https://assetstore.unity.com/packages/tools/network/vuplex-3d-webview-for-android-with-gecko-engine-245867)
- After importing, you should see: `Assets/Vuplex/WebView/...`, and be able to use `CanvasWebViewPrefab` in scenes
- Note: if you want to run WebView directly in the macOS/Windows Editor, you may need to install the native plugins for those platforms per Vuplex docs; building for Android only is fine

##### B. XREAL XR Plugin (Required, Already Configured)

- Included in this project: `Packages/com.xreal.xr.tar.gz`
- `Packages/manifest.json` references the local package: `"com.xreal.xr": "@com.xreal.xr.tar.gz"`
- To upgrade the plugin: replace `Packages/com.xreal.xr.tar.gz` and keep the `manifest.json` reference consistent

##### C. Unity Package Manager Dependencies (Auto-installed)

After opening the project, Unity resolves dependencies from `Packages/manifest.json` automatically (e.g., Input System / AR Foundation / XR Interaction Toolkit). In most cases you do not need to install anything manually in Package Manager.

#### 4) Project Setup (What You Need to Change Before Running)

##### 4.1 Configure the WebView Initial URL

1. Open the scene: `Assets/Scenes/WebView.unity`
2. Select `CanvasWebViewPrefab` in the scene hierarchy
3. Set `InitialUrl` to your web URL
   - Current example value: `https://xlife.chat/MainPage/AR`

##### 4.2 (Optional) Configure iFLYTEK Speech Recognition

**REQUIRED if you want to use speech recognition features.**

The speech recognition config file is: `Assets/Resources/XunfeiConfig.json`

1. Register at [iFLYTEK Open Platform](https://www.xfyun.cn/) and create an application
2. Obtain your API credentials (appId, apiKey, apiSecret)
3. Edit `Assets/Resources/XunfeiConfig.json` and fill in:
   - `appId`: Your application ID
   - `apiKey`: Your API Key
   - `apiSecret`: Your API Secret

Alternatively, you can create a ScriptableObject config in Unity Editor:

- Right-click in Project window → Create → XLIFE AR → Xunfei Speech Recognition Config
- Set the credentials in the Inspector
- Place the config asset in `Assets/Resources/` folder

#### 5) Build APK

##### 5.1 Pre-build Checklist

- Vuplex is imported correctly (otherwise you will see compilation errors like missing `Vuplex.WebView` namespace)
- `Packages/com.xreal.xr.tar.gz` exists and Unity Package Manager shows no errors
- Scenes are included in Build Settings (this project should already be configured, but double-check):
  - `Assets/Scenes/WebView.unity`
  - `Assets/Scenes/RGBCameraAndCapture.unity`

##### 5.2 Build Steps in Unity (Android)

1. `File -> Build Settings...`
2. Select `Android`, then click `Switch Platform`
3. In `Scenes In Build`, make sure `WebView` and `RGBCameraAndCapture` are enabled (recommended: put `WebView` first)
4. `Edit -> Project Settings -> XR Plug-in Management`
   - In the `Android` tab, enable **XREAL** (XREAL XR Loader)
5. `Player Settings -> Other Settings` (recommended values; adjust as needed)
   - `Scripting Backend`: IL2CPP
   - `Target Architectures`: ARM64
6. Connect an Android device (Developer Mode + USB debugging enabled), then click `Build And Run`
   - Or click `Build` to export an `.apk` and install it manually

> Note: this project includes a custom manifest at `Assets/Plugins/Android/AndroidManifest.xml`, which declares network/microphone/screen-capture related permissions, including the Android 14+ foreground service permission `FOREGROUND_SERVICE_MEDIA_PROJECTION`.

##### 6) Troubleshooting

- `The type or namespace name 'Vuplex' could not be found`: Vuplex 3D WebView is not imported
- WebView is blank / cannot load: check `InitialUrl`, device network, and whether cleartext HTTP is allowed (if using `http`)
- Camera / screen recording does not work in Editor: XREAL capture APIs typically only work on real Android devices (there is also a mock branch in scripts)
- Screen recording issues on Android 14+: make sure you did not overwrite/remove the foreground service permission declarations in `Assets/Plugins/Android/AndroidManifest.xml`

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

A minimal, de-identified sample dataset containing representative CGM traces and structured lifestyle logs is available at `src/sample_data_placeholder.zip`. The sample is specifically formatted for computational compatibility with the X-Life preprocessing and modeling pipelines, enabling code verification and functional demonstration. It is intended exclusively for testing and development purposes. Use of this sample for clinical inference, biomedical research, or any generalizable conclusion is strictly discouraged.

To train and evaluate the model, run:
```bash
cd metabolic_world_model
mv ../src/sample_data_placeholder.zip data/sample_data.zip
unzip -d data/ data/sample_data.zip
python ...
```

### Hardware Ecosystem
* CGM sensor (SIBIONICS CGM)
* Fit Bands that provide sleep analysis, heart rate monitoring, etc. 
* XREAL One Pro (XREAL, China, Shenzhen) 

## Citation
```bibtex
@article{XLife2026,
  title = {X-Life: A metabolic world model system for personalised lifestyle medicine},
  author = {Wu, Qian and Qin, Yiming and et al.},
  journal = {},
  year = {2026}
}
```
