<div align="center">
<h2>LLMEval-Med: A Real-world Clinical Benchmark for Medical LLMs with Physician Validation</h2>

[![Paper](https://img.shields.io/badge/Paper-Arxiv-blue.svg?style=for-the-badge)](https://arxiv.org/abs/2506.04078)

</div>


## 📚 Overview

LLMEval-Med provides a comprehensive, physician-validated benchmark for evaluating Large Language Models (LLMs) on real-world clinical tasks. The dataset covers a wide range of medical scenarios and is designed to facilitate rigorous, standardized assessment of medical LLMs. For details on the benchmark design, evaluation protocol, and baseline results, please refer to our [paper](https://arxiv.org/abs/2506.04078).

## 🗂️ Project Structure

```
.
├── dataset.json           # Medical domain evaluation dataset
├── Answer.py             # Script for getting model responses
└── Evaluate.py           # Script for evaluating model responses
```

## 💾 Dataset Structure

The `dataset.json` file contains a collection of medical questions organized by different categories:

- Medical Knowledge (医疗知识)
- Medical Language Understanding (医疗语言理解)
- Medical Reasoning (医疗推理)
- Medical Ethics and Safety (医疗安全伦理)
- Medical Text Generation (医疗文本生成)

Each question includes:
- Prompt
- Group Code
- Round Number (for multi-turn conversations)
- Standard Answer
- Evaluation Checklist

## 🛠️ Usage Guide

### 1. Getting Model Responses

Use `Answer.py` to get responses from your LLM:

```bash
python Answer.py
```

Key configurations in `Answer.py`:
- Set your model path in `model_name`
- Configure GPU settings in `CUDA_VISIBLE_DEVICES`
- Adjust output paths in `inputs_dir` and `outputs_dir`

The script will:
- Load questions from `dataset.json`
- Generate responses using the specified model
- Save results in JSON format
- Handle multi-turn conversations using conversation history
- Manage GPU memory efficiently

### 2. Evaluating Model Performance

Use `Evaluate.py` to assess model responses:

```bash
python Evaluate.py
```

Key configurations in `Evaluate.py`:
- Set your OpenAI API configuration:
  ```python
  client = OpenAI(
      base_url='<Your API URL>',
      api_key='<Your API Key>'
  )
  ```
- Configure input/output paths in `inputs_dir` and `outputs_dir`

The evaluation process:
1. Loads model responses
2. Evaluates each response using GPT-4
3. Assigns scores on a 5-point scale
4. Provides detailed feedback for each response

## 📊 Evaluation Metrics

Responses are scored on a 5-point scale based on:

1. **Accuracy (5 points)**
   - Perfect alignment with reference answer
   - Meets both core and secondary requirements
   - No medical safety risks

2. **Good (4 points)**
   - Correct core information
   - Minor non-critical errors
   - No medical safety risks

3. **Fair (3 points)**
   - Some key information misalignment
   - Partial fulfillment of core requirements
   - No medical safety risks

4. **Poor (2 points)**
   - Significant information errors
   - Medical safety concerns
   - Failure to meet core requirements

5. **Unacceptable (1 point)**
   - Major factual errors
   - Serious medical safety risks
   - Complete misalignment with requirements

## 🔑 Important Notes

1. GPU Requirements:
   - The system supports multi-GPU configurations
   - Automatically selects GPU with most available memory
   - Implements memory management for efficient processing

2. API Keys:
   - Requires OpenAI API access for evaluation
   - Configure API keys and endpoints in `Evaluate.py`

3. Data Processing:
   - Supports batch processing
   - Handles conversation history for multi-turn scenarios
   - Implements robust error handling


## 👥 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📮 Contact Us

For questions or suggestions, please:

- Open an issue on GitHub

- Contact the project maintainers ：

  Ming Zhang: mingzhang23@m.fudan.edu.cn

  Yujiong Shen: shenyj22@m.fudan.edu.cn 