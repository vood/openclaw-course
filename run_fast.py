"""
Fast hypothesis sweep - 50ep, 2-fold, 2 subjects, 1 session each.
Runs ALL hypotheses in one process for fast results.
"""
import warnings; warnings.filterwarnings('ignore')
import sys, os, json, time
import numpy as np
import torch
from moabb.datasets import BNCI2014_001
from moabb.paradigms import MotorImagery
from braindecode import EEGClassifier
from braindecode.models import EEGNetv4
from skorch.callbacks import LRScheduler
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

SUBJECTS = [1, 3]  # 2 subjects for speed
N_FOLDS = 2
os.makedirs("/home/user/openclaw-course/results", exist_ok=True)

dataset = BNCI2014_001()

def make_configs():
    EP = 50  # Fast iteration
    return {
        "baseline": {
            "desc": "Default EEGNet (50ep, lr=1e-3, drop=0.5, Adam, bs=64, 4-38Hz)",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h01_longer": {
            "desc": "200 epochs instead of 50",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=200, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h02_lr5e4": {
            "desc": "lr=5e-4",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.0005, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h03_adamw": {
            "desc": "AdamW wd=0.01",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.AdamW, optimizer__lr=0.001, optimizer__weight_decay=0.01),
            "module_kwargs": {},
        },
        "h04_cosine": {
            "desc": "Cosine LR",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0,
                        callbacks=[("lr_sched", LRScheduler(policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                                                            T_max=EP, eta_min=1e-6))]),
            "module_kwargs": {},
        },
        "h05_drop25": {
            "desc": "Dropout 0.25",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.25, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h06_bs128": {
            "desc": "Batch size 128",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=128,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h07_bs32": {
            "desc": "Batch size 32",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=32,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h08_F16": {
            "desc": "F1=16 temporal filters",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {"F1": 16, "D": 2},
        },
        "h09_wide": {
            "desc": "1-45 Hz",
            "paradigm": dict(n_classes=4, fmin=1, fmax=45, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h10_mubeta": {
            "desc": "8-30 Hz mu/beta",
            "paradigm": dict(n_classes=4, fmin=8, fmax=30, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {},
        },
        "h11_kern128": {
            "desc": "Kernel length 128",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {"kernel_length": 128},
        },
        "h12_D4": {
            "desc": "Depth D=4",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.5, max_epochs=EP, batch_size=64,
                        optimizer=torch.optim.Adam, optimizer__lr=0.001, optimizer__weight_decay=0),
            "module_kwargs": {"D": 4},
        },
        "h13_combo_train": {
            "desc": "AdamW+cosine+drop25+200ep",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.25, max_epochs=200, batch_size=64,
                        optimizer=torch.optim.AdamW, optimizer__lr=0.001, optimizer__weight_decay=0.01,
                        callbacks=[("lr_sched", LRScheduler(policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                                                            T_max=200, eta_min=1e-6))]),
            "module_kwargs": {},
        },
        "h14_combo_arch": {
            "desc": "F1=16+kern128+AdamW+cosine+drop25+200ep",
            "paradigm": dict(n_classes=4, fmin=4, fmax=38, resample=128),
            "clf": dict(module__drop_prob=0.25, max_epochs=200, batch_size=64,
                        optimizer=torch.optim.AdamW, optimizer__lr=0.0005, optimizer__weight_decay=0.01,
                        callbacks=[("lr_sched", LRScheduler(policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                                                            T_max=200, eta_min=1e-6))]),
            "module_kwargs": {"F1": 16, "D": 2, "kernel_length": 128},
        },
        "h15_kitchen": {
            "desc": "F16+D4+kern128+mubeta+AdamW+cosine+drop25+200ep",
            "paradigm": dict(n_classes=4, fmin=8, fmax=30, resample=128),
            "clf": dict(module__drop_prob=0.25, max_epochs=200, batch_size=64,
                        optimizer=torch.optim.AdamW, optimizer__lr=0.0005, optimizer__weight_decay=0.01,
                        callbacks=[("lr_sched", LRScheduler(policy=torch.optim.lr_scheduler.CosineAnnealingLR,
                                                            T_max=200, eta_min=1e-6))]),
            "module_kwargs": {"F1": 16, "D": 4, "kernel_length": 128},
        },
    }


def eval_hypothesis(name, config):
    paradigm = MotorImagery(**config["paradigm"])
    scores = {}
    t0 = time.time()

    for subj in SUBJECTS:
        X, y, meta = paradigm.get_data(dataset, subjects=[subj])
        le = LabelEncoder()
        y = le.fit_transform(y)
        X = X.astype(np.float32)
        n_ch, n_t, n_cls = X.shape[1], X.shape[2], len(np.unique(y))

        module_kw = {"n_chans": n_ch, "n_outputs": n_cls, "n_times": n_t, "final_conv_length": "auto"}
        module_kw.update(config["module_kwargs"])

        # Only use first session for speed
        sessions = sorted(meta['session'].unique())[:1]
        for sess in sessions:
            mask = meta['session'] == sess
            X_s, y_s = X[mask], y[mask]
            skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=42)
            fold_scores = []
            for tr, te in skf.split(X_s, y_s):
                clf_kw = dict(config["clf"])
                cbs = clf_kw.pop("callbacks", [])
                clf = EEGClassifier(
                    module=EEGNetv4, train_split=None, callbacks=cbs,
                    device='cpu', verbose=0,
                    **{f"module__{k}": v for k, v in module_kw.items()},
                    **clf_kw,
                )
                clf.fit(X_s[tr], y_s[tr])
                fold_scores.append(float(clf.score(X_s[te], y_s[te])))
            mean_s = np.mean(fold_scores)
            scores[f"s{subj}_{sess}"] = {"mean": mean_s, "folds": fold_scores}
            print(f"  {name} | S{subj}/{sess}: {mean_s:.4f} {fold_scores}", flush=True)

    elapsed = time.time() - t0
    mean_acc = np.mean([v["mean"] for v in scores.values()])
    std_acc = np.std([v["mean"] for v in scores.values()])
    return {"hypothesis": name, "description": config["desc"],
            "mean_accuracy": float(mean_acc), "std_accuracy": float(std_acc),
            "per_subject_session": scores, "elapsed_seconds": float(elapsed)}


if __name__ == "__main__":
    configs = make_configs()
    all_results = []

    print(f"Running {len(configs)} hypotheses on {SUBJECTS} subjects, {N_FOLDS}-fold CV", flush=True)
    print("=" * 70, flush=True)

    for name, config in configs.items():
        print(f"\n>>> {name}: {config['desc']}", flush=True)
        t0 = time.time()
        result = eval_hypothesis(name, config)
        all_results.append(result)
        with open(f"/home/user/openclaw-course/results/{name}.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"    RESULT: {result['mean_accuracy']:.4f} +/- {result['std_accuracy']:.4f} ({time.time()-t0:.0f}s)", flush=True)

    # Final summary
    all_results.sort(key=lambda x: x["mean_accuracy"], reverse=True)
    baseline_acc = next(r["mean_accuracy"] for r in all_results if r["hypothesis"] == "baseline")

    print("\n" + "=" * 70, flush=True)
    print(f"{'Rank':<5} {'Hypothesis':<20} {'Accuracy':>10} {'vs Base':>10} {'Time':>8}", flush=True)
    print("-" * 58, flush=True)
    for i, r in enumerate(all_results, 1):
        delta = r["mean_accuracy"] - baseline_acc
        sign = "+" if delta >= 0 else ""
        print(f"{i:<5} {r['hypothesis']:<20} {r['mean_accuracy']:>9.4f} {sign}{delta:>9.4f} {r['elapsed_seconds']:>7.0f}s", flush=True)

    print(f"\nBaseline: {baseline_acc:.4f}", flush=True)
    best = all_results[0]
    print(f"Best: {best['hypothesis']} at {best['mean_accuracy']:.4f} ({best['mean_accuracy']-baseline_acc:+.4f})", flush=True)

    with open("/home/user/openclaw-course/results/summary.json", "w") as f:
        json.dump({"ranked_results": all_results, "baseline_accuracy": baseline_acc}, f, indent=2)
    print("\nAll results saved to results/", flush=True)
