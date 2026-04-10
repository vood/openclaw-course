#!/bin/bash
# Run all hypothesis tests sequentially
cd /home/user/openclaw-course

HYPOTHESES=(
    baseline
    h01_longer_training
    h02_lower_lr
    h03_adamw_wd
    h04_cosine_lr
    h05_lower_dropout
    h06_larger_batch
    h07_smaller_batch
    h08_F1_16
    h09_wider_band
    h10_mu_beta
    h11_kernel_128
    h12_D4
    h13_combined_training
    h14_combined_arch
    h15_kitchen_sink
)

echo "Starting ${#HYPOTHESES[@]} hypothesis tests at $(date)"
echo "================================================"

for h in "${HYPOTHESES[@]}"; do
    echo ""
    echo ">>> Starting $h at $(date)"
    python run_hypothesis.py "$h" 2>&1
    echo ">>> Finished $h at $(date)"
    echo "---"
done

echo ""
echo "================================================"
echo "ALL TESTS COMPLETE at $(date)"
echo "================================================"

# Summarize results
echo ""
echo "SUMMARY:"
python3 -c "
import json, glob, os
results = []
for f in sorted(glob.glob('results/*.json')):
    with open(f) as fh:
        r = json.load(fh)
        results.append(r)

results.sort(key=lambda x: x['mean_accuracy'], reverse=True)

print(f\"{'Rank':<5} {'Hypothesis':<25} {'Accuracy':>10} {'Std':>8} {'Time':>8}\")
print('-' * 60)
for i, r in enumerate(results, 1):
    print(f\"{i:<5} {r['hypothesis']:<25} {r['mean_accuracy']:>9.4f} {r['std_accuracy']:>7.4f} {r['elapsed_seconds']:>7.0f}s\")

baseline_acc = next(r['mean_accuracy'] for r in results if r['hypothesis'] == 'baseline')
print(f\"\nBaseline accuracy: {baseline_acc:.4f}\")
print('Improvements over baseline:')
for r in results:
    if r['hypothesis'] != 'baseline':
        delta = r['mean_accuracy'] - baseline_acc
        sign = '+' if delta >= 0 else ''
        print(f\"  {r['hypothesis']:<25} {sign}{delta:.4f} ({sign}{delta/baseline_acc*100:.1f}%)\")
"
