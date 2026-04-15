<p align="center">
  <img src="llmeval-logo.png" width="200">
</p>

<h2 align="center">LLMEval-Med: 基于真实临床场景、医生验证的医学大模型评测基准</h2>

<p align="center">
  <a href="https://arxiv.org/abs/2506.04078"><img src="https://img.shields.io/badge/论文-Arxiv-blue.svg?style=for-the-badge" alt="论文"></a>
  <a href="https://huggingface.co/datasets/HuayuSha/LLMeval-Med"><img src="https://img.shields.io/badge/数据集-HuggingFace-yellow.svg?style=for-the-badge" alt="数据集"></a>
  <a href="https://github.com/llmeval"><img src="https://img.shields.io/badge/组织-LLMEval-green.svg?style=for-the-badge" alt="LLMEval"></a>
</p>

> **注意：** 英文版 README 请参阅 [README.md](README.md)。

> 🎉 **最新消息：** 我们的论文已被 **EMNLP 2025 Findings** 录用！

## 📚 概述

LLMEval-Med 提供了一个全面的、经医生验证的基准，用于评估大语言模型在真实临床任务上的表现。数据集涵盖多种医学场景，旨在促进对医学大模型的严格、标准化评估。有关基准设计、评测协议和基线结果的详细信息，请参阅我们的[论文](https://arxiv.org/abs/2506.04078)。数据集也可在 [HuggingFace](https://huggingface.co/datasets/HuayuSha/LLMeval-Med) 上获取。

## 🗂️ 项目结构

```
.
├── dataset/
│   └── dataset.json       # 医学领域评测数据集
├── evaluate/
│   ├── Answer.py          # 获取模型回答的脚本
│   └── Evaluate.py        # 评估模型回答的脚本
```

## 💾 数据集结构

`dataset/dataset.json` 包含 **667 道医学题目** 的测试集，按以下类别组织：

- 医学知识（Medical Knowledge）
- 医学语言理解（Medical Language Understanding）
- 医学推理（Medical Reasoning）
- 医学伦理与安全（Medical Ethics and Safety）
- 医学文本生成（Medical Text Generation）

每道题目包含以下字段：

- **category1**: 一级类别
- **category2**: 二级类别
- **scene**: 场景或上下文
- **round**: 轮次（多轮对话场景）
- **problem**: 医学问题
- **groupCode**: 组别标识
- **sanswer**: 标准参考答案
- **difficulty**: 难度等级
- **checklist**: 评测要点清单

## 📊 评测指标

回答按 5 分制评分：

| 等级 | 分数 | 标准 |
|:-----|:-----|:-----|
| 优秀 | 5 分 | 与参考答案完全一致，满足核心和次要要求，无医疗安全风险 |
| 良好 | 4 分 | 核心信息正确，存在少量非关键性错误，无医疗安全风险 |
| 一般 | 3 分 | 部分关键信息偏差，部分满足核心要求，无医疗安全风险 |
| 较差 | 2 分 | 存在重大信息错误，有医疗安全隐患，未满足核心要求 |
| 不可接受 | 1 分 | 重大事实错误，严重医疗安全风险，完全偏离要求 |

## 🛠️ 使用指南

### 1. 获取模型回答

```bash
python evaluate/Answer.py
```

主要配置项：
- 在 `model_name` 中设置模型路径
- 在 `CUDA_VISIBLE_DEVICES` 中配置 GPU
- 在 `inputs_dir` 和 `outputs_dir` 中设置输入输出路径

### 2. 评估模型表现

```bash
python evaluate/Evaluate.py
```

主要配置项：
- 设置 OpenAI API 配置（`base_url` 和 `api_key`）
- 配置输入/输出路径

## 🔗 相关项目

| 项目 | 说明 | 链接 |
|------|------|------|
| **LLMEval**（AAAI 2024） | 评测方法论研究 | [arXiv](https://arxiv.org/abs/2312.07398) |
| **LLMEval-Fair**（ACL 2026） | 鲁棒公平评测，20 万+题 | [GitHub](https://github.com/llmeval/LLMEval-Fair) |
| **LLMEval-1** | 第一期通用能力评测 | [GitHub](https://github.com/llmeval/LLMEval-1) |
| **LLMEval-2** | 第二期专业领域评测 | [GitHub](https://github.com/llmeval/LLMEval-2) |
| **官方网站** | 全部项目与排行榜 | [llmeval.com](http://llmeval.com/) |

## 📝 引用

```bibtex
@inproceedings{zhang-etal-2025-llmeval,
    title     = "{LLME}val-{M}ed: A Real-world Clinical Benchmark for Medical {LLM}s with Physician Validation",
    author    = "Zhang, Ming and Shen, Yujiong and Li, Zelin and Sha, Huayu and Hu, Binze and Wang, Yuhui and Huang, Chenhao and Liu, Shichun and Tong, Jingqi and Jiang, Changhao and Chai, Mingxu and Xi, Zhiheng and Dou, Shihan and Gui, Tao and Zhang, Qi and Huang, Xuanjing",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2025",
    month     = nov,
    year      = "2025",
    address   = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url       = "https://aclanthology.org/2025.findings-emnlp.263/",
    doi       = "10.18653/v1/2025.findings-emnlp.263",
    pages     = "4888--4914",
}
```

## 📞 联系我们

- **邮箱**：mingzhang23@m.fudan.edu.cn / shenyj22@m.fudan.edu.cn
- **网站**：[http://llmeval.com/](http://llmeval.com/)

---

<p align="center">
  <b>LLMEval</b> | 复旦大学 NLP 实验室
</p>
