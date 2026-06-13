# Voice2Task Post-Training 实验报告

## 项目目标

将中文口语浏览器指令转换为结构化 JSON（BrowserTaskContract），通过 SFT + DPO 微调 Qwen2.5-7B-Instruct 实现。

## 数据

| 阶段 | Seeds | SFT rows | DPO pairs |
|------|-------|----------|-----------|
| 初始 | 4 | 12 | 27 |
| 扩充后 | 240 | 916 | 1,689 |

- 6 种 task_type 全覆盖：search, navigate, form_fill, extract, clarify, blocked
- 数据生成：Claude API (claude-sonnet-4-6) + schema 校验 + 编辑距离去重
- 分层划分：train 628 / dev 128 / test 160

## 模型配置

- Base: Qwen2.5-7B-Instruct
- 方法: LoRA (r=16, alpha=32, target=q/k/v/o_proj)
- SFT: 3 epochs, lr=2e-4, batch=4, grad_accum=2
- DPO: 2 epochs, lr=5e-5, beta=0.1, batch=2, grad_accum=4
- 硬件: 单卡 A100-80G

## 实验结果

### Dev Split 最终指标 (SFT v2, normalized data)

| 指标 | 值 |
|------|-----|
| json_valid_rate | 100% |
| task_type_accuracy | 99.2% |
| route_accuracy | 99.2% |
| safety_precision | 100% |
| safety_recall | 100% |
| confirmation_accuracy | 95.3% |
| slot_f1 (strict) | 33.0% |
| slot_f1_soft (internal diagnostic, char-F1≥0.7) | 70.3% |
| contract_exact_match | 13.3% |

### Test Split 最终指标

| 指标 | 值 |
|------|-----|
| json_valid_rate | 100% |
| task_type_accuracy | 98.1% |
| route_accuracy | 98.1% |
| safety_precision | 95.2% |
| safety_recall | 100% |
| confirmation_accuracy | 98.8% |
| slot_f1 (strict) | 43.0% |
| slot_f1_soft (internal diagnostic) | 66.8% |
| contract_exact_match | 16.9% |

### 消融实验对比

| 配置 | slot_f1_strict | slot_f1_soft (internal diagnostic) | safety_p | safety_r |
|------|---------------|-------------|----------|----------|
| SFT v1 (原始数据) | 28.1% | 71.8% | 92.3% | 100% |
| SFT v1 + DPO | 28.4% | — | 100% | 88.9% |
| **SFT v2 (normalized)** | **33.0%** | **70.3%** | **100%** | **100%** |

## 关键发现

1. **数据量是核心**：4 seeds 时 json_valid=0%，240 seeds 后达到 100%——7B 模型需要 ~200+ 样本学习输出格式

2. **SFT 足以解决结构化问题**：task_type/route/safety 等分类字段在 SFT 后即接近完美（99%+），DPO 对此无额外收益

3. **DPO 对 slot 无效且有害**：DPO 的 reward accuracy 达到 100%（模型已完美区分 hard negatives），但 slot value 生成是文本生成问题而非偏好问题。DPO 反而导致 json_valid 从 100% 退化到 94.5%

4. **Slot_f1 仍是主要瓶颈**：strict slot_f1 仍低；soft char-F1 只是内部诊断视角，用来定位
   表述差异，不能替代 strict slot_f1 或 `contract_exact_match`。

5. **Slot value 的本质困难**：搜索 query 没有唯一正确答案——"帮我搜搜庆余年第二季什么时候出" 的 query 可以是 "庆余年第二季播出时间" 也可以是 "庆余年第二季上映时间"，两者都正确

## 技术实现要点

- Assistant-only label masking：SFTTrainer 只对 assistant 回复部分计算 loss
- Schema retry：prediction 输出如果 JSON 解析失败，尝试修复后重试
- Bad words suppression：禁止生成 markdown code fence（解决了 transformers 5.5.0 的 multi-token bad_words_ids bug）
- Dual-adapter loading：DPO predict 时需先 merge SFT adapter 再加 DPO adapter，全部 merge_and_unload 后上 GPU

## 结论

Qwen2.5-7B + LoRA SFT 在 240 seeds 规模下：
- **结构化输出字段**：在本次 dev/test 实验中较高，但这不是生产可用声明。
- **Slot 抽取能力**：strict 指标仍是瓶颈；soft 指标仅作内部误差分析。
- **推荐后续方向**：
  - 扩大到 500+ seeds 并严格统一 slot value 标注规范
  - 使用 LLM-as-judge 评估 slot 语义等价性（替代字符匹配）
  - 若评估 soft matching 或语义相似度，应作为单独诊断指标，不能替代 strict contract 指标

## 文件结构

```
<repo-root>/                                  # 本地项目根目录
├── src/voice2task/                           # 核心代码
│   ├── training.py                           # SFT/DPO 训练 + prediction
│   ├── evaluation.py                         # 评估指标（含 soft slot_f1）
│   ├── dataset.py                            # 数据集构建 + hard negative 生成
│   └── formatting.py                         # SFT prompt 格式化
├── scripts/
│   ├── generate_seed_traces.py               # 批量生成 seed（Claude API）
│   ├── validate_generated_seeds.py           # 校验 + 去重
│   └── normalize_slot_values.py              # Slot value 规范化
├── data/local-private/
│   ├── seed_traces_full_normalized.jsonl     # 规范化后的 229 seeds
│   └── full-corpus-v2/                       # 最终训练数据
└── configs/                                  # 训练/预测配置

<a100-project-root>/                          # 服务器训练产物
├── outputs/sft-v2-normalized/adapter/        # 最终 SFT adapter（推荐使用）
├── outputs/sft-full-corpus/adapter/          # v1 SFT adapter
└── outputs/dpo-full-corpus/adapter/          # DPO adapter（不推荐使用）
```
