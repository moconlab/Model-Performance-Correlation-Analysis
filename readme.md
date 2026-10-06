# Model correlation demo data
Synthetic datasets for **`model-properties-performance-correlation.ipynb`**.
| File | Description |
|------|-------------|
| `model_properties.csv` | Geometry / density scalars (as from `DensityStats.json` + optional `ModelStats.csv` peaks) |
| `model_performance.csv` | Load and runtime outcomes (benchmark export) |
| `models_merged.csv` | Inner join on `model_name` and `urn` — default input for the notebook |


```
Model-Performance-Correlation/
  model-correlation-sample-data/
    model_properties.csv
    model_performance.csv
    models_merged.csv
  model-properties-performance-correlation.ipynb
```

Run the notebook with working directory set to `Model-Performance-Correlation` (default when opened from this folder).