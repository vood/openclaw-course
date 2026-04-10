"""
Round 2: High-impact experiments to substantially improve accuracy.
Focused on the techniques most likely to close the gap with Riemannian methods.

Tests on subjects 1, 3, 7 with 3-fold CV, both sessions (matching baseline).
"""
import warnings; warnings.filterwarnings('ignore')
import os, json, time
import numpy as np
import torch
from moabb.datasets import BNCI2014_001
from moabb.paradigms import MotorImagery
from braindecode import EEGClassifier
from braindecode.models import EEGNetv4, ShallowFBCSPNet
from skorch.callbacks import LRScheduler
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

SUBJECTS = [1, 3, 7]
N_FOLDS = 3
dataset = BNCI2014_001()
os.makedirs("/home/user/openclaw-course/results_r2", exist_ok=True)

EXPERIMENTS = {
    "r2_shallow_200ep": {
        "desc": "ShallowConvNet 200ep (MOABB's best DL model)",
        "model_class": ShallowFBCSPNet,
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(module__drop_prob=0.5, max_epochs=200, batch_size=64,
                    optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
        "module_kwargs": {},
    },
    "r2_shallow_500ep_cosine": {
        "desc": "ShallowConvNet 500ep + cosine LR + AdamW",
        "model_class": ShallowFBCSPNet,
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(module__drop_prob=0.5, max_epochs=500, batch_size=64,
                    optimizer=torch.optim.AdamW, optimizer__lr=0.001, optimizer__weight_decay=0.01,
                    callbacks=[("lr_sched", LRScheduler(
                        policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                        T_max=500, eta_min=1e-6))]),
        "module_kwargs": {},
    },
    "r2_eegnet_500ep_cosine": {
        "desc": "EEGNet 500ep + cosine LR + AdamW + drop=0.25",
        "model_class": EEGNetv4,
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(module__drop_prob=0.25, max_epochs=500, batch_size=64,
                    optimizer=torch.optim.AdamW, optimizer__lr=0.001, optimizer__weight_decay=0.01,
                    callbacks=[("lr_sched", LRScheduler(
                        policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                        T_max=500, eta_min=1e-6))]),
        "module_kwargs": {},
    },
    "r2_eegnet_kern128_500ep": {
        "desc": "EEGNet kern128 + 500ep + cosine + AdamW + drop=0.25",
        "model_class": EEGNetv4,
        "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
        "clf": dict(module__drop_prob=0.25, max_epochs=500, batch_size=64,
                    optimizer=torch.optim.AdamW, optimizer__lr=0.001, optimizer__weight_decay=0.01,
                    callbacks=[("lr_sched", LRScheduler(
                        policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                        T_max=500, eta_min=1e-6))]),
        "module_kwargs": {"kernel_length": 128},
    },
}


def run_experiment(name, config):
    paradigm = MotorImagery(**config["paradigm"])
    model_cls = config["model_class"]
    scores = {}
    t0 = time.time()

    for subj in SUBJECTS:
        X, y, meta = paradigm.get_data(dataset, subjects=[subj])
        le = LabelEncoder()
        y = le.fit_transform(y)
        X = X.astype(np.float32)
        n_ch, n_t, n_cls = X.shape[1], X.shape[2], len(np.unique(y))

        module_kw = {"n_chans": n_ch, "n_outputs": n_cls, "n_times": n_t,
                     "final_conv_length": "auto"}
        module_kw.update(config["module_kwargs"])

        sessions = sorted(meta['session'].unique())
        for sess in sessions:
            mask = meta['session'] == sess
            X_s, y_s = X[mask], y[mask]
            skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=42)
            fold_scores = []
            for tr, te in skf.split(X_s, y_s):
                clf_kw = dict(config["clf"])
                cbs = clf_kw.pop("callbacks", [])
                clf = EEGClassifier(
                    module=model_cls, train_split=None, callbacks=cbs,
                    device='cpu', verbose=0,
                    **{f"module__{k}": v for k, v in module_kw.items()},
                    **clf_kw,
                )
                clf.fit(X_s[tr], y_s[tr])
                fold_scores.append(float(clf.score(X_s[te], y_s[te])))
            mean_s = np.mean(fold_scores)
            key = f"s{subj}_{sess}"
            scores[key] = {"mean": float(mean_s), "folds": fold_scores}
            print(f"  {name} | S{subj}/{sess}: {mean_s:.4f} {fold_scores}", flush=True)

    elapsed = time.time() - t0
    overall_mean = np.mean([v["mean"] for v in scores.values()])
    overall_std = np.std([v["mean"] for v in scores.values()])
    return {"hypothesis": name, "description": config["desc"],
            "mean_accuracy": float(overall_mean), "std_accuracy": float(overall_std),
            "per_subject_session": scores, "elapsed_seconds": float(elapsed),
            "subjects": SUBJECTS}


if __name__ == "__main__":
    print(f"Round 2: {len(EXPERIMENTS)} high-impact experiments", flush=True)
    print(f"Subjects: {SUBJECTS}, {N_FOLDS}-fold CV, all sessions", flush=True)
    print("=" * 70, flush=True)

    # Load baseline for comparison
    baseline_acc = 0.7494  # from results/baseline.json

    all_results = []
    for name, config in EXPERIMENTS.items():
        print(f"\n>>> {name}: {config['desc']}", flush=True)
        result = run_experiment(name, config)
        all_results.append(result)
        with open(f"/home/user/openclaw-course/results_r2/{name}.json", "w") as f:
            json.dump(result, f, indent=2)
        delta = result["mean_accuracy"] - baseline_acc
        s = "+" if delta >= 0 else ""
        print(f"    RESULT: {result['mean_accuracy']:.4f} (vs baseline 0.7494: {s}{delta:.4f}) [{result['elapsed_seconds']:.0f}s]", flush=True)

    # Summary
    all_results.sort(key=lambda x: x["mean_accuracy"], reverse=True)
    print("\n" + "=" * 70, flush=True)
    print("ROUND 2 RESULTS vs BASELINE (0.7494)", flush=True)
    print(f"{'#':<3} {'Experiment':<30} {'Acc':>7} {'vs Base':>10} {'Time':>7}", flush=True)
    print("-" * 62, flush=True)
    for i, r in enumerate(all_results, 1):
        d = r["mean_accuracy"] - baseline_acc
        s = "+" if d >= 0 else ""
        print(f"{i:<3} {r['hypothesis']:<30} {r['mean_accuracy']:>6.4f} {s}{d:>9.4f} {r['elapsed_seconds']:>6.0f}s", flush=True)

    with open("/home/user/openclaw-course/results_r2/summary.json", "w") as f:
        json.dump({"baseline_accuracy": baseline_acc, "ranked_results": all_results}, f, indent=2)
    print("\nResults saved to results_r2/", flush=True)
