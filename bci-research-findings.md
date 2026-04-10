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

### 3. Braindecode (1,194 stars - strong alternative top pick)
**Repository:** [braindecode/braindecode](https://github.com/braindecode/braindecode)
**Stars:** 1,194 | **Open Issues:** 95 | **Language:** Python/PyTorch

Braindecode is the main deep learning toolbox for EEG decoding. It has several high-impact bugs that directly affect classification accuracy:

**Critical accuracy-affecting bugs:**
- **Bug #816:** Official BCI Competition IV-2a tutorial returns **25% accuracy (chance level)** for 4-class motor imagery. The model fails to learn due to insufficient training duration and misconfigured pipeline. Fixing this = immediate, dramatic accuracy improvement in the project's flagship example.
- **Bug #984:** SyncNet has **swapped parameter initialization** - `phi_ini` (phase shift) pulls from `beta_init_values` and vice versa, causing incorrect model behavior.
- **Bug #873:** MultiHeadAttention scaling factor is `emb_size ** (1/2)` when it should be `(emb_size // num_heads) ** (1/2)`, deviating from the standard transformer formulation.
- **Bug #889:** SqueezeAndExcitation module has dimension mismatch in fc2 layer.

**Pipeline/infrastructure bugs:**
- **Bug #885:** 19 standalone MNE preprocessor classes pass string names instead of callables, breaking the preprocessing pipeline.
- **Bug #892:** Pydantic v2 serialization failure in model configs (EEGNetConfig, EEGConformerConfig).
- **Performance #947:** `push_to_hub` bottleneck with hardcoded chunk size.

**Enhancement opportunities:**
- **Issue #913:** TODO list for adding new model architectures
- **Issue #828:** Port winning models from EPFL epilepsy competitions

Best for: demonstrating Claude Code fixing real bugs in production ML code with immediate, measurable accuracy impact.

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
**Stars:** 558 | **Open Issues:** 31 | **Language:** Python/PyTorch

Comprehensive EEG toolkit with benchmark implementations. Notable bugs:
- **Bug #114:** EEGNet padding bug - even-sized convolution kernels cause the time dimension to increase by 1 (TensorFlow `padding='SAME'` vs PyTorch mismatch)
- **Issue #156:** Uses NumPy-based `pywt` instead of PyTorch-native `ptwt` for CWT, missing GPU acceleration
- Motor imagery classification and imbalanced learning improvements

### 6. pyRiemann
**Repository:** [pyRiemann/pyRiemann](https://github.com/pyRiemann/pyRiemann)
**Stars:** 748 | **Open Issues:** 8 | **Language:** Python

The leading Riemannian geometry library for BCI (backbone of the best-performing MOABB pipelines):
- **PR #433:** Add Python Array API support for NumPy/PyTorch backend transparency (enables GPU acceleration)
- **Issue #338** (`help wanted`): Generalize `make_classification_transfer` beyond 2 classes/2 domains
- **Issue #396:** Generalize `geodesic` to accept ndarray of alpha values
- **Issue #429:** Unify convergence criteria across iterative mean computations

### 7. MOABB Performance Issues
- **Issue #394** (`help wanted`): Add parallel processing for `CrossSubjectEvaluation` - parallelization exists for WithinSession and CrossSession but not CrossSubject, which is the most computationally expensive
- **15+ open dataset requests** (Issues #892-#916, #943-#944) - each a formulaic Python class following existing patterns

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

**For maximum drama:** Fix braindecode's official BCI IV-2a tutorial (#816) from 25% (chance) to 80%+ accuracy. This is the project's flagship example broken at chance level - fixing it is both a bug fix AND a dramatic accuracy demonstration.

**For quickest wins:** Fix braindecode bugs (#816, #984, #873, #889, #885) - these are real bugs affecting real users with clear, scoped fixes.

**For practical contribution:** Add MOABB CrossSubjectEvaluation parallelization (#394, `help wanted`) or implement dataset loaders for the 15+ requested datasets.

---

## Prioritized Action Tiers

### Tier 1 - Quick wins with measurable impact (hours)
1. **Fix braindecode #816** - Official tutorial at chance level (25% → 80%+). Most dramatic single fix.
2. **Fix braindecode #984** - SyncNet swapped parameter initialization
3. **Fix braindecode #873** - MultiHeadAttention wrong scaling factor
4. **Fix braindecode #889** - SqueezeAndExcitation dimension mismatch
5. **Fix braindecode #885** - 19 broken MNE preprocessor classes
6. **Fix TorchEEG #114** - EEGNet padding bug

### Tier 2 - Medium effort, high value (days)
7. **MOABB #394** - Add parallelization to CrossSubjectEvaluation (`help wanted`)
8. **Add DL pipelines for P300/SSVEP in MOABB** - currently zero DL coverage
9. **Implement EEG data augmentation** in braindecode (time-warping, noise injection, channel dropout)
10. **pyRiemann #433** - Array API / GPU support
11. **MOABB dataset loaders** - 15+ templated dataset classes needed

### Tier 3 - Larger projects with research impact (weeks)
12. Integrate EEG foundation models (CodeBrain, NeuroLM) into braindecode + MOABB benchmarking
13. Implement domain adaptation for cross-subject transfer learning
14. Build automated hyperparameter optimization into MOABB DL pipelines

---

## Key Insight: Why Deep Learning Underperforms in BCI

SpeechBrain-MOABB proved the gap is **not fundamental** - they achieved **14.9% improvement over MOABB's DL results** simply through:
1. Proper hyperparameter search (MOABB used defaults)
2. Multi-seed evaluation (MOABB used single seeds)
3. Better training recipes (learning rate scheduling, early stopping)

This means Claude Code doesn't need to invent new architectures - just properly configure and train existing ones.

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
- [SpeechBrain Benchmarks GitHub](https://github.com/speechbrain/benchmarks)
- [BCI Competition IV](https://www.bbci.de/competition/iv/)
- [BNCI Horizon 2020 Datasets](https://bnci-horizon-2020.eu/database/data-sets)
- [PhysioNet EEG MI Dataset](https://www.physionet.org/content/eegmmidb/1.0.0/)
