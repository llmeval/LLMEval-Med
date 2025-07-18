<div align="center">
<h2>LLMEval-Med: A Real-world Clinical Benchmark for Medical LLMs with Physician Validation</h2>

[![Paper](https://img.shields.io/badge/Paper-Arxiv-blue.svg?style=for-the-badge)](https://arxiv.org/abs/2506.04078)

</div>

> **Note:** For the Chinese version of this README, please refer to [README_zh.md](README_zh.md).

## 📚 Overview

LLMEval-Med provides a comprehensive, physician-validated benchmark for evaluating Large Language Models (LLMs) on real-world clinical tasks. The dataset covers a wide range of medical scenarios and is designed to facilitate rigorous, standardized assessment of medical LLMs. For details on the benchmark design, evaluation protocol, and baseline results, please refer to our [paper](https://arxiv.org/abs/2506.04078).

## 🗂️ Project Structure

```
.
├── dataset/
│   └── dataset.json       # Medical domain evaluation dataset
├── evaluate/
│   ├── Answer.py          # Script for getting model responses
│   └── Evaluate.py        # Script for evaluating model responses
```

## 💾 Dataset Structure

The `dataset/dataset.json` file contains a **test set** of 667 medical questions, organized by different categories:

- Medical Knowledge 
- Medical Language Understanding 
- Medical Reasoning 
- Medical Ethics and Safety 
- Medical Text Generation 

Each question in the test set is a JSON object with the following fields:

- **category1**: Primary category of the question (e.g., "Medical Knowledge").
- **category2**: Secondary category, providing more specific grouping.
- **scene**: Scenario or context for the question.
- **round**: Round number, used for multi-turn conversations (1 for single-turn).
- **problem**: The medical question or prompt presented to the model.
- **groupCode**: Group identifier for the question.
- **sanswer**: The standard (reference) answer provided by medical experts.
- **difficulty**: Difficulty level.
- **checklist**: Key points or criteria for evaluation, ensuring the answer covers essential aspects.
> **Note:**  
> The scoring prompts for each category (e.g., Medical Knowledge, Medical Language Understanding, Medical Reasoning, Medical Ethics and Safety, Medical Text Generation) are defined directly in `evaluate/Evaluate.py`.  
> Each prompt is carefully designed to guide the evaluation process and ensure consistency across different types of questions.

Example:
```json
{
  "category1": "Medical Knowledge",
  "category2": "Basic Medical Knowledge/Medical Exam",
  "scene": "Basic Medical Knowledge/Medical Exam_Traditional Chinese Medicine",
  "round": 1,
  "problem": "Why is β-OH anthraquinone more acidic than α-OH anthraquinone?",
  "groupCode": 5,
  "sanswer": "The stronger acidity of β-OH anthraquinone compared to α-OH anthraquinone is mainly due to resonance effects, hydrogen bonding, and steric hindrance...",
  "difficulty": "Medium",
  "checklist": "Core requirements:\n1. Explain the enhanced resonance effect, reduced hydrogen bonding, and steric hindrance for β-OH anthraquinone acidity.\n2. Detail how the β-OH position stabilizes the anion via resonance, and how the α-OH position's intramolecular hydrogen bond reduces acidity.\n\nSecondary requirements:\n1. Emphasize the role of the conjugated system and electron-withdrawing effects."
}
```

## 🛠️ Usage Guide

### 1. Getting Model Responses

Use `evaluate/Answer.py` to get responses from your LLM:

```bash
python evaluate/Answer.py
```

Key configurations in `Answer.py`:
- Set your model path in `model_name`
- Configure GPU settings in `CUDA_VISIBLE_DEVICES`
- Adjust output paths in `inputs_dir` and `outputs_dir`

The script will:
- Load questions from `dataset/dataset.json`
- Generate responses using the specified model
- Save results in JSON format
- Handle multi-turn conversations using conversation history
- Manage GPU memory efficiently

### 2. Evaluating Model Performance

Use `evaluate/Evaluate.py` to assess model responses:

```bash
python evaluate/Evaluate.py
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
