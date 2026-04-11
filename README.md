# HLX Delta

Deterministic change-tracking system for structured data with exact reconstruction.

Designed for telemetry, streaming systems, and distributed synchronization where minimizing data transfer and compute overhead is critical.

Part of Evo Engineering LLC  
https://www.evo.engineering/

---

## ⚡ Core Result

- Exact reconstruction (SHA256 verified)
- Significant data reduction depending on change patterns
- Deterministic and reproducible behavior
- Consistent performance across structured datasets

In systems where most data remains stable between updates, HLX Delta reduces data transfer while preserving exact system state.

---

## 🚀 Performance Characteristics

HLX Delta operates on change (Δ) rather than full state, enabling significant efficiency gains in systems where data stability is high.

### Observed Behavior (Benchmark Summary)

Across multiple real-world structured datasets:

- ~90–99% reduction in compute (validated via benchmark harness)
- ~97–99.9% reduction in data transfer
- Linear scaling with change frequency

### Key Insight

Compute cost scales with **change rate (Δ)** rather than total dataset size (N):

- Low change → near-zero recomputation  
- Moderate change → proportional compute  
- High change → approaches baseline  

Unlike traditional systems (e.g., Parquet, Delta Lake) that optimize storage, HLX Delta enables execution models that operate on changed data only.

---

## 🔥 Example Output (Real Dataset)

```

HLX DELTA ENGINE — DEMO

Dataset: AEP_hourly.json
Records: 121273

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Original Size:     7.31 MB
Delta Size:        551.27 KB
Reduction:         92.64%

Encode Time:       0.0509 sec
Decode Time:       0.2813 sec

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reconstruction:    PASS
SHA256 Match:      VERIFIED

Observed Efficiency:
Change Rate:       5.00%
Reduction:         92.64%

Compute Comparison (Simulated Workload):
Full Scan Time:    0.084379 sec
Delta Scan Time:   0.011000 sec

````

Tested on real-world energy datasets and structured event streams.

---

## 📊 Behavior

Efficiency depends on:

- stability of the underlying data  
- frequency of change between states  

HLX Delta is most effective when the majority of data remains unchanged between updates.

---

## 🧪 Use Cases

- Telemetry systems  
- Distributed synchronization  
- Event streaming pipelines  
- IoT data transmission  
- Structured data evolution  

---

## ▶️ Run Demo

```bash
python hlx_delta_demo.py sample_data_json/AEP_hourly.json
````

---

## ⚠️ Notes

* This repository provides a demonstration layer
* Compute comparison in the demo uses simulated workloads for illustration
* Full execution optimization and internal architecture are not included
* Performance varies depending on data characteristics

---

## 🏢 By

Evo Engineering LLC

```
