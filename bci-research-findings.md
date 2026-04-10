# BCI Open Source Software: Improvement Opportunities for Claude Code

## Executive Summary

After surveying the BCI open-source landscape, **the top recommendation is to work with MOABB (Mother of All BCI Benchmarks) + implement an improved deep learning pipeline** that can be benchmarked against 30 existing pipelines across 36 datasets. The secondary recommendation is **FBCSP on BCI Competition IV-2a**, where the accuracy gap between naive implementations (~58%) and state-of-the-art (~85%) makes for a dramatic before/after demonstration.

---

## Top Recommendation: MOABB + New Pipeline

**Repository:** [NeuroTechX/moabb](https://github.com/NeuroTechX/moabb)
**Stars:** 966 | **Open Issues:** 111 | **Language:** Python | **License:** BSD-3

### Why MOABB

MOABB is the standard benchmarking framework for BCI algorithms. It provides:
- **36 publicly available datasets** (14 motor imagery, 15 P300, 7 SSVEP)
- **30 existing pipelines** (11 raw signal, 13 Riemannian, 6 deep learning)
- **Standardized within-session evaluation** with reproducible metrics
- Any improvement is immediately measurable and comparable

### The Opportunity: Deep Learning Underperforms Riemannian Methods

The [2024 MOABB benchmark paper](https://arxiv.org/abs/2404.15319) revealed a critical finding:

> Riemannian distance-based classification consistently outperforms deep learning pipelines across all paradigms.

| Paradigm | Best Riemannian | Best Deep Learning | Gap |
|---|---|---|---|
| MI (L vs R hand) | TS+SVM: 93.37% | ShallowConvNet: 95.65% | DL wins on some datasets |
| MI (R hand vs feet) | FgMDM: 98.48% | ShallowConvNet: 98.06% | Riemannian +0.4% |
| P300 | XDAWNCov+TS+SVM: 98.69% | *No DL pipelines tested* | DL absent |
| SSVEP | SSVEP_TS+LR: 89.44% | *No DL pipelines tested* | DL absent |

**Key gaps Claude Code can address:**
1. **No deep learning pipelines exist for P300 or SSVEP in MOABB** - implementing EEG-conformer or EEGNet for these paradigms would fill a major void
2. **DL pipelines are inconsistent** - EEGNeX scores 49% on Shin2017A but 80%+ on others; improving robustness across datasets is valuable
3. **Only 6 DL pipelines vs 13 Riemannian** - adding modern architectures (EEG-Deformer, ATCNet, EEG-Conformer) would expand coverage
4. **108 open issues** including dataset additions, metadata validation, and pipeline customization

### Concrete Action Plan

```python
# Example: Add EEG-Conformer pipeline to MOABB for Motor Imagery
from moabb.pipelines import create_pipeline_from_braindecode
from braindecode.models import EEGConformer

# Define pipeline, evaluate across all MI datasets
pipeline = create_pipeline_from_braindecode(EEGConformer)
# Run MOABB benchmark -> instant comparison against 30 pipelines
```

### What Success Looks Like
- Beat existing DL pipelines on 3+ motor imagery datasets
- Provide the first DL pipeline for P300 in MOABB
- Reduce variance across subjects (more robust generalization)

---

## Runner-Up: FBCSP on BCI Competition IV-2a

**Repository:** [orvindemsy/BCICIV2a-FBCSP](https://github.com/orvindemsy/BCICIV2a-FBCSP)
**Stars:** 47 | **Open Issues:** 5 | **Language:** Python/Jupyter

### Why This Project

This is a textbook implementation of Filter Bank Common Spatial Pattern (FBCSP) for 4-class motor imagery classification. The accuracy gap is enormous:

| Method | Accuracy (4-class) | Source |
|---|---|---|
| Current FBCSP+SVM | ~58% | This repo |
| EEGNet | ~75% | Literature |
| ATCNet | ~83% | Literature |
| CIACNet (SOTA) | ~85% | Literature, 2025 |

**Claude Code could improve accuracy by 15-25+ percentage points** by:
1. Replacing SVM with a modern classifier (LightGBM, neural net)
2. Adding data augmentation (time shifting, noise injection, mixup)
3. Implementing subject-adaptive transfer learning
4. Adding proper cross-validation and hyperparameter tuning
5. Upgrading to EEGNet or ATCNet architecture

### Advantages
- Small, manageable codebase (~500 lines)
- Standard dataset (BCI Competition IV-2a: 9 subjects, 4 classes, 22 channels)
- Dramatic before/after comparison
- Well-understood problem with known baselines

---

## Other Strong Candidates

### 3. Braindecode
**Repository:** [braindecode/braindecode](https://github.com/braindecode/braindecode)
**Stars:** 800+ | **Language:** Python/PyTorch

**Improvement opportunities:**
- **Bug #889:** SqueezeAndExcitation module has dimension mismatch in fc2 layer
- **Bug #885:** Standalone MNE preprocessor classes break 19 public preprocessors
- **Bug #892:** Pydantic v2 serialization failure in model configs
- **Issue #913:** TODO list for adding new model architectures
- **Performance #947:** `push_to_hub` bottleneck

Best for: demonstrating Claude Code fixing real bugs in production ML code.

### 4. MIN2Net
**Repository:** [IoBT-VISTEC/MIN2Net](https://github.com/IoBT-VISTEC/MIN2Net)
**Stars:** 103 | **Open Issues:** 10 | **Language:** Python/TensorFlow

**The problem:** Subject-independent motor imagery classification. MIN2Net achieves only 49% F1-score on BCI Competition IV-2a in subject-independent mode.

**Improvement opportunities:**
- Optimize autoencoder architecture
- Add modern data augmentation (CutMix for EEG, frequency-domain augmentation)
- Implement better domain adaptation for cross-subject transfer
- Replace TripletLoss with more recent contrastive learning (SimCLR, BYOL-style)

### 5. TorchEEG
**Repository:** [torcheeg/torcheeg](https://github.com/torcheeg/torcheeg)
**Stars:** 300+ | **Language:** Python/PyTorch

Comprehensive EEG toolkit with benchmark implementations. Opportunities in:
- Improving data augmentation pipeline
- Motor imagery classification modules
- Imbalanced learning support

### 6. pyRiemann
**Repository:** [pyRiemann/pyRiemann](https://github.com/pyRiemann/pyRiemann)
**Stars:** 748 | **Language:** Python

The leading Riemannian geometry library for BCI. Fewer obvious improvement opportunities since it already outperforms most methods, but potential in:
- GPU acceleration of covariance matrix operations
- New Riemannian deep learning hybrid methods

---

## Relevant Datasets

| Dataset | Paradigm | Subjects | Classes | Channels | Access |
|---|---|---|---|---|---|
| BCI Competition IV-2a | Motor Imagery | 9 | 4 | 22 | Free (BNCI) |
| BCI Competition IV-2b | Motor Imagery | 9 | 2 | 3 | Free (BNCI) |
| PhysioNet MI | Motor Imagery | 109 | 4 | 64 | Free (PhysioNet) |
| OpenBMI | Motor Imagery | 54 | 2 | 62 | Free |
| BNCI2014-001 | Motor Imagery | 9 | 4 | 22 | Free (MOABB) |
| Lee2019 | MI + SSVEP | 54 | 2 | 62 | Free (MOABB) |

---

## Recommendation Summary

| Criterion | MOABB + Pipeline | FBCSP Improvement | Braindecode Bugs |
|---|---|---|---|
| Measurable impact | High (standardized benchmark) | High (clear accuracy gain) | Medium (bug fixes) |
| Difficulty | Medium | Low-Medium | Medium |
| Community value | Very High | Medium | High |
| Demonstrability | Excellent | Excellent | Good |
| Codebase size | Large (use as framework) | Small (~500 lines) | Large |
| Time to results | Hours | Hours | Hours |

**For maximum impact:** Use MOABB as the evaluation framework, implement a modern DL pipeline (EEG-Conformer or ATCNet), and benchmark it against all existing pipelines. This produces a scientifically rigorous, immediately publishable result.

**For maximum drama:** Take the FBCSP repo and improve accuracy from 58% to 80%+ using modern techniques. This produces the most visually impressive before/after comparison.

**For practical contribution:** Fix braindecode bugs (#889, #885, #892) - these are real issues affecting real users.

---

## Sources

- [MOABB GitHub](https://github.com/NeuroTechX/moabb)
- [MOABB Benchmark Paper (2024)](https://arxiv.org/abs/2404.15319)
- [MOABB Benchmark Results](https://moabb.neurotechx.com/docs/paper_results.html)
- [Braindecode GitHub](https://github.com/braindecode/braindecode)
- [Braindecode Issues](https://github.com/braindecode/braindecode/issues)
- [FBCSP Implementation](https://github.com/orvindemsy/BCICIV2a-FBCSP)
- [MIN2Net GitHub](https://github.com/IoBT-VISTEC/MIN2Net)
- [MIN2Net Paper](https://arxiv.org/abs/2102.03814)
- [TorchEEG GitHub](https://github.com/torcheeg/torcheeg)
- [pyRiemann GitHub](https://github.com/pyRiemann/pyRiemann)
- [SpeechBrain-MOABB (14.9% improvement over MOABB)](https://www.sciencedirect.com/science/article/pii/S001048252401182X)
- [EEG-Deformer](https://github.com/yi-ding-cs/EEG-Deformer)
- [CIACNet - 85.15% on BCI IV-2a](https://pmc.ncbi.nlm.nih.gov/articles/PMC11841462/)
