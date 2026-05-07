<p align="center">
  <img src="llmeval-logo.png" width="200">
</p>

<h2 align="center">LLMEval-Med: A Real-world Clinical Benchmark for Medical LLMs with Physician Validation</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2506.04078"><img src="https://img.shields.io/badge/Paper-Arxiv-blue.svg?style=for-the-badge" alt="Paper"></a>
  <a href="https://huggingface.co/datasets/HuayuSha/LLMeval-Med"><img src="https://img.shields.io/badge/Dataset-HuggingFace-yellow.svg?style=for-the-badge" alt="Dataset"></a>
  <a href="https://github.com/llmeval"><img src="https://img.shields.io/badge/Org-LLMEval-green.svg?style=for-the-badge" alt="LLMEval"></a>
</p>

> 🎉 **News:** Our paper has been accepted at **EMNLP 2025 Findings**!

> **Note:** For the Chinese version of this README, please refer to [README_zh.md](README_zh.md).

## 📚 Overview

LLMEval-Med provides a comprehensive, physician-validated benchmark for evaluating Large Language Models (LLMs) on real-world clinical tasks. The dataset covers a wide range of medical scenarios and is designed to facilitate rigorous, standardized assessment of medical LLMs. For details on the benchmark design, evaluation protocol, and baseline results, please refer to our [paper](https://arxiv.org/abs/2506.04078). The dataset is also available on [Hugging Face](https://huggingface.co/datasets/HuayuSha/LLMeval-Med).

## 🗂️ Project Structure

```
.
├── dataset/
│   └── dataset.json       # Medical domain evaluation dataset
├── evaluate/
│   ├── Answer.py          # Script for getting model responses
│   ├── Evaluate.py        # Script for scoring model responses (1-5 per question)
│   └── Aggregate.py       # Script for aggregating scores into Usability Rate / OP
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

### 3. Aggregating into Overall Performance (OP)

`evaluate/Evaluate.py` only produces per-question 1–5 scores. Use `evaluate/Aggregate.py` to turn those scores into the per-category Usability Rate and Overall Performance (OP) numbers reported in Table 2 of the paper:

```bash
# Single judging run
python evaluate/Aggregate.py path/to/dataset_processed_score.json

# Three judging runs (the paper's protocol): per-question scores are
# averaged across runs before the >=4 usability threshold is applied.
python evaluate/Aggregate.py run1.json run2.json run3.json --out summary.json
```

A response is counted as **usable** when its averaged 0–5 score is ≥ 4 (for MK / MLU / MR / MSE). For MTG the paper additionally maps a 5-dimension human evaluation through the Appendix D piecewise formula (threshold ≥ 5, with `Safety = 1` as a hard veto); a helper `mtg_score_from_human_eval` is provided in `Aggregate.py` for that case. **OP** is the sample-count-weighted usability rate across all questions.

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

## 📝 Citation

If you find this benchmark useful, please cite our paper:

```bibtex
@inproceedings{zhang-etal-2025-llmeval,
    title = "{LLME}val-{M}ed: A Real-world Clinical Benchmark for Medical {LLM}s with Physician Validation",
    author = "Zhang, Ming  and
      Shen, Yujiong  and
      Li, Zelin  and
      Sha, Huayu  and
      Hu, Binze  and
      Wang, Yuhui  and
      Huang, Chenhao  and
      Liu, Shichun  and
      Tong, Jingqi  and
      Jiang, Changhao  and
      Chai, Mingxu  and
      Xi, Zhiheng  and
      Dou, Shihan  and
      Gui, Tao  and
      Zhang, Qi  and
      Huang, Xuanjing",
    editor = "Christodoulopoulos, Christos  and
      Chakraborty, Tanmoy  and
      Rose, Carolyn  and
      Peng, Violet",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2025",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-emnlp.263/",
    doi = "10.18653/v1/2025.findings-emnlp.263",
    pages = "4888--4914",
    ISBN = "979-8-89176-335-7",
    abstract = "Evaluating large language models (LLMs) in medicine is crucial because medical applications require high accuracy with little room for error. Current medical benchmarks have three main types: medical exam-based, comprehensive medical, and specialized assessments. However, these benchmarks have limitations in question design (mostly multiple-choice), data sources (often not derived from real clinical scenarios), and evaluation methods (poor assessment of complex reasoning). To address these issues, we present LLMEval-Medicine, a new benchmark covering five core medical areas, including 2,996 questions created from real-world electronic health records and expert-designed clinical scenarios. We also design an automated evaluation pipeline, incorporating expert-developed checklists into our LLM-as-Judge framework. Furthermore, our methodology validates machine scoring through human-machine agreement analysis, dynamically refining checklists and prompts based on expert feedback to ensure reliability. We evaluate 13 LLMs across three categories (specialized medical models, open-source models, and closed-source models) on LLMEval-Med, providing valuable insights for the safe and effective deployment of LLMs in medical domains."
}
```

## 🔗 Related Projects

| Project | Description | Link |
|---------|-------------|------|
| **LLMEval** (AAAI 2024) | Foundational evaluation methodology paper | [arXiv](https://arxiv.org/abs/2312.07398) |
| **LLMEval-Fair** (ACL 2026) | Robust & fair evaluation, 200K+ questions | [GitHub](https://github.com/llmeval/LLMEval-Fair) |
| **LLMEval-1** | Phase I: General capability evaluation | [GitHub](https://github.com/llmeval/LLMEval-1) |
| **LLMEval-2** | Phase II: Professional domain evaluation | [GitHub](https://github.com/llmeval/LLMEval-2) |
| **Official Website** | All projects & leaderboard | [llmeval.com](http://llmeval.com/) |

---

<p align="center">
  <b>LLMEval</b> | Fudan University NLP Lab
</p>
