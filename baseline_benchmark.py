"""
Baseline benchmark: EEGNet on BNCI2014_001 (BCI Competition IV-2a) via MOABB.

This establishes the baseline accuracy that we'll try to improve.
Dataset: 9 subjects, 4-class motor imagery (left hand, right hand, feet, tongue), 22 EEG channels.
"""
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import json
import time
from moabb.datasets import BNCI2014_001
from moabb.paradigms import MotorImagery
from moabb.evaluations import WithinSessionEvaluation
from sklearn.pipeline import Pipeline
from braindecode.models import EEGNetv4
from skorch.callbacks import EarlyStopping, LRScheduler
from skorch import NeuralNetClassifier
from braindecode import EEGClassifier
import torch

print("=" * 60)
print("BASELINE: EEGNet on BNCI2014_001 (BCI IV-2a)")
print("=" * 60)

# Load dataset - use first 2 subjects for faster iteration
dataset = BNCI2014_001()

# Define paradigm
paradigm = MotorImagery(
    n_classes=4,
    fmin=4,
    fmax=38,
    resample=128,
)

# Get data info
X, y, metadata = paradigm.get_data(dataset, subjects=[1])
n_channels = X.shape[1]
n_times = X.shape[2]
n_classes = len(np.unique(y))

print(f"Data shape: {X.shape}")
print(f"Channels: {n_channels}, Timepoints: {n_times}, Classes: {n_classes}")
print(f"Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

# Define EEGNet with MOABB's default settings (as used in the benchmark paper)
def make_eegnet_pipeline():
    model = EEGClassifier(
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
    )
    return model

# Run within-session evaluation on subjects 1-9
pipelines = {"EEGNet_baseline": make_eegnet_pipeline()}

evaluation = WithinSessionEvaluation(
    paradigm=paradigm,
    datasets=[dataset],
    overwrite=True,
    hdf5_path=None,
    n_jobs=1,
)

print("\nRunning evaluation on all 9 subjects...")
print("This may take a while...\n")

start_time = time.time()
results = evaluation.process(pipelines)
elapsed = time.time() - start_time

print(f"\nCompleted in {elapsed:.0f}s")
print("\n" + "=" * 60)
print("BASELINE RESULTS")
print("=" * 60)

# Print per-subject results
print(f"\n{'Subject':<10} {'Accuracy':<12} {'Session'}")
print("-" * 40)
for _, row in results.iterrows():
    print(f"{row['subject']:<10} {row['score']:.4f}       {row['session']}")

mean_acc = results['score'].mean()
std_acc = results['score'].std()
print(f"\n{'MEAN':<10} {mean_acc:.4f} +/- {std_acc:.4f}")

# Save results
baseline_results = {
    "model": "EEGNet_baseline",
    "dataset": "BNCI2014_001",
    "paradigm": "MotorImagery_4class",
    "mean_accuracy": float(mean_acc),
    "std_accuracy": float(std_acc),
    "per_subject": {str(row['subject']): float(row['score']) for _, row in results.iterrows()},
    "elapsed_seconds": elapsed,
    "config": {
        "epochs": 200,
        "batch_size": 64,
        "lr": 0.001,
        "drop_prob": 0.5,
        "optimizer": "Adam",
        "weight_decay": 0,
        "fmin": 4,
        "fmax": 38,
        "resample": 128,
    }
}

with open("baseline_results.json", "w") as f:
    json.dump(baseline_results, f, indent=2)

print(f"\nResults saved to baseline_results.json")
