"""
Fast hypothesis test runner - evaluates a single hypothesis on 3 subjects.
Usage: python run_hypothesis.py <hypothesis_name>
"""
import warnings
warnings.filterwarnings('ignore')

import sys
import numpy as np
import json
import time
import torch
from torch import nn
from moabb.datasets import BNCI2014_001
from moabb.paradigms import MotorImagery
from braindecode import EEGClassifier
from braindecode.models import EEGNetv4
from skorch.callbacks import LRScheduler
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

hypothesis_name = sys.argv[1]
output_file = f"/home/user/openclaw-course/results/{hypothesis_name}.json"

# Fixed params
SUBJECTS = [1, 3, 7]  # Fast iteration on 3 diverse subjects
N_FOLDS = 3  # 3-fold for speed (still statistically meaningful)

print(f"Testing: {hypothesis_name}", flush=True)
print(f"Subjects: {SUBJECTS}", flush=True)

dataset = BNCI2014_001()

# ============================================================
# HYPOTHESIS CONFIGS
# Each returns: (paradigm_kwargs, classifier_kwargs, description)
# ============================================================

EP = 200  # Standard epoch count for fair comparison

CONFIGS = {
    "baseline": {
        "desc": "Default EEGNet (200ep, lr=1e-3, drop=0.5, Adam, bs=64, 4-38Hz)",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h01_longer_training": {
        "desc": "400 epochs instead of 200",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=400, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h02_lower_lr": {
        "desc": "Learning rate 0.0005 instead of 0.001",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.0005, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h03_adamw_wd": {
        "desc": "AdamW with weight_decay=0.01",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.001, optimizer__weight_decay=0.01,
        ),
        "module_kwargs": {},
    },
    "h04_cosine_lr": {
        "desc": "Cosine annealing LR from 1e-3 to 1e-6",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
            callbacks=[("lr_sched", LRScheduler(
                policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                T_max=EP, eta_min=1e-6))],
        ),
        "module_kwargs": {},
    },
    "h05_lower_dropout": {
        "desc": "Dropout 0.25 instead of 0.5",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.25,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h06_larger_batch": {
        "desc": "Batch size 128 instead of 64",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=128,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h07_smaller_batch": {
        "desc": "Batch size 32 instead of 64",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=32,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h08_F1_16": {
        "desc": "F1=16 temporal filters instead of 8",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {"F1": 16, "D": 2},
    },
    "h09_wider_band": {
        "desc": "Frequency band 1-45 Hz instead of 4-38 Hz",
        "paradigm": dict(n_classes=4, fmin=1, fmax=45, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h10_mu_beta": {
        "desc": "Focus on mu/beta bands: 8-30 Hz",
        "paradigm": dict(n_classes=4, fmin=8, fmax=30, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {},
    },
    "h11_kernel_128": {
        "desc": "Temporal kernel length 128 instead of 64",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {"kernel_length": 128},
    },
    "h12_D4": {
        "desc": "Depth multiplier D=4 instead of D=2",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.5,
            max_epochs=EP, batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001, optimizer__weight_decay=0,
        ),
        "module_kwargs": {"D": 4},
    },
    "h13_combined_training": {
        "desc": "AdamW + cosine LR + dropout=0.25 + 400ep",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.25,
            max_epochs=400, batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.001, optimizer__weight_decay=0.01,
            callbacks=[("lr_sched", LRScheduler(
                policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                T_max=400, eta_min=1e-6))],
        ),
        "module_kwargs": {},
    },
    "h14_combined_arch": {
        "desc": "F1=16 + kernel=128 + AdamW + cosine LR + drop=0.25 + lr=5e-4",
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(
            module__drop_prob=0.25,
            max_epochs=400, batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.0005, optimizer__weight_decay=0.01,
            callbacks=[("lr_sched", LRScheduler(
                policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                T_max=400, eta_min=1e-6))],
        ),
        "module_kwargs": {"F1": 16, "D": 2, "kernel_length": 128},
    },
    "h15_kitchen_sink": {
        "desc": "F1=16 + D=4 + kernel=128 + mu/beta + AdamW + cosine + drop=0.25",
        "paradigm": dict(n_classes=4, fmin=8, fmax=30, resample=128),
        "clf": dict(
            module__drop_prob=0.25,
            max_epochs=400, batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.0005, optimizer__weight_decay=0.01,
            callbacks=[("lr_sched", LRScheduler(
                policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                T_max=400, eta_min=1e-6))],
        ),
        "module_kwargs": {"F1": 16, "D": 4, "kernel_length": 128},
    },
}

config = CONFIGS[hypothesis_name]
paradigm = MotorImagery(**config["paradigm"])

all_scores = {}
start_time = time.time()

for subj in SUBJECTS:
    X, y, meta = paradigm.get_data(dataset, subjects=[subj])
    le = LabelEncoder()
    y = le.fit_transform(y)
    X = X.astype(np.float32)
    n_ch, n_t = X.shape[1], X.shape[2]
    n_cls = len(np.unique(y))

    # Build classifier for this subject
    module_kw = {
        "n_chans": n_ch,
        "n_outputs": n_cls,
        "n_times": n_t,
        "final_conv_length": "auto",
    }
    module_kw.update(config["module_kwargs"])

    clf_kwargs = dict(config["clf"])
    callbacks = clf_kwargs.pop("callbacks", [])

    clf = EEGClassifier(
        module=EEGNetv4,
        train_split=None,
        callbacks=callbacks,
        device='cpu',
        verbose=0,
        **{f"module__{k}": v for k, v in module_kw.items()},
        **clf_kwargs,
    )

    # Manual 5-fold CV per session
    sessions = meta['session'].unique()
    for sess in sessions:
        sess_mask = meta['session'] == sess
        X_sess = X[sess_mask]
        y_sess = y[sess_mask]

        skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=42)
        fold_scores = []
        for train_idx, test_idx in skf.split(X_sess, y_sess):
            X_tr, X_te = X_sess[train_idx], X_sess[test_idx]
            y_tr, y_te = y_sess[train_idx], y_sess[test_idx]

            # Re-initialize for each fold
            clf_fold = EEGClassifier(
                module=EEGNetv4,
                train_split=None,
                callbacks=callbacks,
                device='cpu',
                verbose=0,
                **{f"module__{k}": v for k, v in module_kw.items()},
                **clf_kwargs,
            )
            clf_fold.fit(X_tr, y_tr)
            score = clf_fold.score(X_te, y_te)
            fold_scores.append(score)

        mean_score = np.mean(fold_scores)
        key = f"s{subj}_{sess}"
        all_scores[key] = {
            "mean": float(mean_score),
            "folds": [float(s) for s in fold_scores],
        }
        print(f"  Subject {subj}, Session {sess}: {mean_score:.4f} ({fold_scores})", flush=True)

elapsed = time.time() - start_time
overall_mean = np.mean([v["mean"] for v in all_scores.values()])
overall_std = np.std([v["mean"] for v in all_scores.values()])

print(f"\n{'='*50}")
print(f"RESULT: {hypothesis_name}")
print(f"  Description: {config['desc']}")
print(f"  Mean accuracy: {overall_mean:.4f} +/- {overall_std:.4f}")
print(f"  Time: {elapsed:.0f}s")
print(f"{'='*50}")

result = {
    "hypothesis": hypothesis_name,
    "description": config["desc"],
    "mean_accuracy": float(overall_mean),
    "std_accuracy": float(overall_std),
    "per_subject_session": all_scores,
    "elapsed_seconds": float(elapsed),
    "subjects": SUBJECTS,
}

import os
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"Saved to {output_file}")
