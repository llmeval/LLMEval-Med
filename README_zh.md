<div align="center">
<h2>LLMEval-Med: A Real-world Clinical Benchmark for Medical LLMs with Physician Validation</h2>

[![Paper](https://img.shields.io/badge/Paper-Arxiv-blue.svg?style=for-the-badge)](https://arxiv.org/abs/2506.04078)

</div>

> **注意：** 英文版 README 请参阅 [README.md](README.md)。

## 📚 概述

LLMEval-Med 提供了一个真实临床场景下、经过临床医生验证的大型语言模型评估基准。该数据集涵盖多种医疗任务，旨在帮助研究者对医疗领域的 LLM 进行严格、标准化的评估。更多基准设计、评估协议和基线结果，请参阅我们的 [论文](https://arxiv.org/abs/2506.04078)。

## 🗂️ 项目结构

```
.
├── dataset/
│   └── dataset.json       # 医疗领域评估数据集
├── evaluate/
│   ├── Answer.py          # 生成模型回答的脚本
│   └── Evaluate.py        # 对模型回答进行评估的脚本
```

## 💾 数据集结构

`dataset/dataset.json` 包含 **667 道** 医学测试题，按以下五大类组织：

* 医学知识（Medical Knowledge）
* 医学语言理解（Medical Language Understanding）
* 医学推理（Medical Reasoning）
* 医学伦理与安全（Medical Ethics and Safety）
* 医学文本生成（Medical Text Generation）

每道题是一个 JSON 对象，字段说明如下：

* **category1**：题目一级类别（如 “Medical Knowledge”）
* **category2**：题目二级类别（更细的分组）
* **scene**：题目场景或背景
* **round**：轮次编号（单轮对话为 1）
* **problem**：模型需回答的医学问题或提示
* **groupCode**：分组标识
* **sanswer**：专家提供的标准参考答案
* **difficulty**：难度等级
* **checklist**：评估要点，确保答案覆盖核心内容

示例：

```json
{
    "category1": "医疗知识",
    "category2": "医学基础知识/医学考试",
    "scene": "医学基础知识/医学考试_中医知识",
    "round": 1,
    "problem": "为什么β-OH蒽醌比α-OH蒽醌的酸性大？",
    "groupCode": 5,
    "sanswer": "β-OH蒽醌比α-OH蒽醌酸性更强的原因主要与分子结构中的共振效应、氢键作用和空间位阻有关：...",
    "difficulty": "中",
    "checklist": "核心需求：..."
}
```

> **注意：**
> 各类别的评分提示（如“医学知识”、“医学语言理解”等）均在 `evaluate/Evaluate.py` 中定义，用于引导评估并保证不同题型的一致性。

## 🛠️ 使用指南

### 1. 获取模型回答

运行：

```bash
python evaluate/Answer.py
```

* 在 `Answer.py` 中设置：

  * `model_name`：模型路径或名称
  * `CUDA_VISIBLE_DEVICES`：GPU 配置
  * `inputs_dir`、`outputs_dir`：输入输出路径

脚本流程：

1. 读取 `dataset/dataset.json`
2. 调用指定 LLM 生成回答
3. 将结果保存为 JSON
4. 支持多轮对话的上下文管理
5. 自动选择可用 GPU 并优化显存使用

### 2. 评估模型性能

运行：

```bash
python evaluate/Evaluate.py
```

* 在 `Evaluate.py` 中设置：

  ```python
  client = OpenAI(
      base_url='<Your API URL>',
      api_key='<Your API Key>'
  )
  ```
* 配置 `inputs_dir`、`outputs_dir`

评估流程：

1. 加载模型回答
2. 使用 GPT-4 对每条回答打分
3. 按 1–5 分制输出分数和详细反馈

## 📊 评价指标

* **5 分（准确）**
  与参考答案完全一致，满足核心与次要要求，无安全风险

* **4 分（良好）**
  核心信息正确，只有轻微非关键错误，无安全风险

* **3 分（一般）**
  部分核心信息有偏差，次要要求部分未满足，无安全风险

* **2 分（差）**
  重要信息错误或遗漏，存在医学安全隐患

* **1 分（不可接受）**
  严重事实错误，安全风险高，完全不符合要求

## 🔑 重要事项

1. **GPU 要求**

   * 支持多 GPU
   * 自动选择剩余显存最多的 GPU
   * 内存管理机制保证稳定运行

2. **API Key**

   * 评估需调用 OpenAI API
   * 在 `Evaluate.py` 中配置 API 地址和密钥

3. **数据处理**

   * 支持批量处理
   * 自动维护多轮对话历史
   * 完善的错误处理机制

## 👥 贡献

欢迎提交 Issue 和 Pull Request，一起完善基准。

## 📮 联系方式

如有问题或建议，请：

* 在 GitHub 上提 Issue

* 联系项目负责人：
  Ming Zhang: mingzhang23@m.fudan.edu.cn

  Yujiong Shen: shenyj22@m.fudan.edu.cn
