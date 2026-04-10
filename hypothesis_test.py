"""
Hypothesis testing framework for improving EEGNet on BNCI2014_001 (BCI IV-2a).

Usage: python hypothesis_test.py --hypothesis <name> --output <file>

Each hypothesis modifies the EEGNet training pipeline and measures accuracy
against the MOABB within-session evaluation on all 9 subjects.
"""
import warnings
warnings.filterwarnings('ignore')

import argparse
import numpy as np
import json
import time
import torch
from torch import nn
from moabb.datasets import BNCI2014_001
from moabb.paradigms import MotorImagery
from moabb.evaluations import WithinSessionEvaluation
from braindecode import EEGClassifier
from braindecode.models import EEGNetv4
from skorch.callbacks import EarlyStopping, LRScheduler
from sklearn.pipeline import Pipeline


def get_data_info():
    """Get dataset dimensions."""
    dataset = BNCI2014_001()
    paradigm = MotorImagery(n_classes=4, fmin=4, fmax=38, resample=128)
    X, y, _ = paradigm.get_data(dataset, subjects=[1])
    return X.shape[1], X.shape[2], len(np.unique(y))


# ============================================================
# HYPOTHESIS DEFINITIONS
# ============================================================

def baseline(n_channels, n_times, n_classes):
    """Default EEGNet - same as MOABB paper."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=200,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h01_longer_training(n_channels, n_times, n_classes):
    """H1: Train for 500 epochs instead of 200."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=500,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h02_lower_lr(n_channels, n_times, n_classes):
    """H2: Lower learning rate (0.0005 instead of 0.001)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.0005,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h03_adamw_weight_decay(n_channels, n_times, n_classes):
    """H3: AdamW optimizer with weight decay (regularization)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.001,
            optimizer__weight_decay=0.01,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h04_cosine_lr_schedule(n_channels, n_times, n_classes):
    """H4: Cosine annealing LR schedule."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[
                ("lr_scheduler", LRScheduler(
                    policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                    T_max=300,
                    eta_min=1e-6,
                )),
            ],
            device='cpu',
            verbose=0,
        ),
    }


def h05_lower_dropout(n_channels, n_times, n_classes):
    """H5: Lower dropout (0.25 instead of 0.5) - less regularization."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.25,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h06_larger_batch(n_channels, n_times, n_classes):
    """H6: Larger batch size (128 instead of 64)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=128,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h07_smaller_batch(n_channels, n_times, n_classes):
    """H7: Smaller batch size (32 instead of 64) for better generalization."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=32,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h08_more_temporal_filters(n_channels, n_times, n_classes):
    """H8: More temporal filters F1=16 (instead of 8) and D=2."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__F1=16,
            module__D=2,
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h09_wider_freq_band(n_channels, n_times, n_classes):
    """H9: Wider frequency band (1-45 Hz instead of 4-38 Hz)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=1, fmax=45, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h10_narrow_mu_beta(n_channels, n_times, n_classes):
    """H10: Focus on mu/beta motor imagery bands (8-30 Hz)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=8, fmax=30, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h11_longer_kernel(n_channels, n_times, n_classes):
    """H11: Longer temporal kernel (128 instead of 64) for better freq resolution."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__kernel_length=128,
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h12_higher_resample(n_channels, n_times, n_classes):
    """H12: Higher resampling rate (250Hz instead of 128Hz) to preserve high-freq info."""
    paradigm = MotorImagery(n_classes=4, fmin=4, fmax=38, resample=250)
    dataset = BNCI2014_001()
    X, y, _ = paradigm.get_data(dataset, subjects=[1])
    n_t = X.shape[2]
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=250),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_t,
            module__final_conv_length='auto',
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h13_depth_multiplier_4(n_channels, n_times, n_classes):
    """H13: Deeper spatial filters D=4 (instead of D=2)."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__F1=8,
            module__D=4,
            module__drop_prob=0.5,
            max_epochs=300,
            batch_size=64,
            optimizer=torch.optim.Adam,
            optimizer__lr=0.001,
            optimizer__weight_decay=0,
            train_split=None,
            callbacks=[],
            device='cpu',
            verbose=0,
        ),
    }


def h14_combined_best_training(n_channels, n_times, n_classes):
    """H14: Combined improvements - AdamW + cosine LR + lower dropout + 500 epochs."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__drop_prob=0.25,
            max_epochs=500,
            batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.001,
            optimizer__weight_decay=0.01,
            train_split=None,
            callbacks=[
                ("lr_scheduler", LRScheduler(
                    policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                    T_max=500,
                    eta_min=1e-6,
                )),
            ],
            device='cpu',
            verbose=0,
        ),
    }


def h15_combined_architecture(n_channels, n_times, n_classes):
    """H15: Combined arch improvements - F1=16, D=2, longer kernel + better training."""
    return {
        "paradigm_kwargs": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "pipeline": EEGClassifier(
            module=EEGNetv4,
            module__n_chans=n_channels,
            module__n_outputs=n_classes,
            module__n_times=n_times,
            module__final_conv_length='auto',
            module__F1=16,
            module__D=2,
            module__kernel_length=128,
            module__drop_prob=0.25,
            max_epochs=500,
            batch_size=64,
            optimizer=torch.optim.AdamW,
            optimizer__lr=0.0005,
            optimizer__weight_decay=0.01,
            train_split=None,
            callbacks=[
                ("lr_scheduler", LRScheduler(
                    policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                    T_max=500,
                    eta_min=1e-6,
                )),
            ],
            device='cpu',
            verbose=0,
        ),
    }


# Register all hypotheses
HYPOTHESES = {
    "baseline": baseline,
    "h01_longer_training": h01_longer_training,
    "h02_lower_lr": h02_lower_lr,
    "h03_adamw_weight_decay": h03_adamw_weight_decay,
    "h04_cosine_lr_schedule": h04_cosine_lr_schedule,
    "h05_lower_dropout": h05_lower_dropout,
    "h06_larger_batch": h06_larger_batch,
    "h07_smaller_batch": h07_smaller_batch,
    "h08_more_temporal_filters": h08_more_temporal_filters,
    "h09_wider_freq_band": h09_wider_freq_band,
    "h10_narrow_mu_beta": h10_narrow_mu_beta,
    "h11_longer_kernel": h11_longer_kernel,
    "h12_higher_resample": h12_higher_resample,
    "h13_depth_multiplier_4": h13_depth_multiplier_4,
    "h14_combined_best_training": h14_combined_best_training,
    "h15_combined_architecture": h15_combined_architecture,
}


def run_hypothesis(name):
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS: {name}")
    print(f"{'='*60}")

    n_channels, n_times, n_classes = 22, 513, 4  # Known from dataset

    config = HYPOTHESES[name](n_channels, n_times, n_classes)
    paradigm_kwargs = config["paradigm_kwargs"]
    pipeline = config["pipeline"]

    paradigm = MotorImagery(**paradigm_kwargs)
    dataset = BNCI2014_001()

    evaluation = WithinSessionEvaluation(
        paradigm=paradigm,
        datasets=[dataset],
        overwrite=True,
        hdf5_path=None,
        n_jobs=1,
    )

    pipelines = {name: pipeline}
    start_time = time.time()
    results = evaluation.process(pipelines)
    elapsed = time.time() - start_time

    print(f"\n{'Subject':<10} {'Accuracy':<12} {'Session'}")
    print("-" * 40)
    for _, row in results.iterrows():
        print(f"{row['subject']:<10} {row['score']:.4f}       {row['session']}")

    mean_acc = results['score'].mean()
    std_acc = results['score'].std()
    print(f"\n{'MEAN':<10} {mean_acc:.4f} +/- {std_acc:.4f}")
    print(f"Elapsed: {elapsed:.0f}s")

    result = {
        "hypothesis": name,
        "description": HYPOTHESES[name].__doc__.strip(),
        "dataset": "BNCI2014_001",
        "mean_accuracy": float(mean_acc),
        "std_accuracy": float(std_acc),
        "per_subject": {},
        "elapsed_seconds": elapsed,
    }
    for _, row in results.iterrows():
        subj = str(row['subject'])
        sess = str(row['session'])
        key = f"s{subj}_{sess}"
        result["per_subject"][key] = float(row['score'])

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hypothesis", required=True, choices=list(HYPOTHESES.keys()))
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    result = run_hypothesis(args.hypothesis)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResults saved to {args.output}")
