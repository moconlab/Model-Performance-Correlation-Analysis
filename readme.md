# Model properties vs performance — correlation study
## What we are trying to achieve
3D models differ in polygon count, object density, empty space, and other measurable traits. Load time, frame rate, and memory use differ too. This project helps you **see which traits move together with performance** before you invest in deeper profiling or code changes. It can also incidcate how a model might perform in an application.

The main artifact is **`model-properties-performance-correlation.ipynb`**. It:
- Loads a table with **one row per model** (geometry or density scalars plus benchmark outcomes).
- Computes **Spearman rank correlations** between property columns and performance columns — useful when relationships are monotonic but not linear, and when counts are heavy-tailed.
- Surfaces **heatmaps**, **top property–outcome pairs**, and **scatter plots** for the outcome you care about most (for example init time or FPS).
- Can **export** a correlation table as CSV for slides, tickets, or BI tools.
Correlation is **not causation**. The notebook is a prioritization tool: it suggests *which* fields deserve follow-up experiments, not *why* a build is slow.
## Who this helps
| Audience | How it helps |
|----------|----------------|
| **Rendering / loading engineers** | Shortlist geometry or model density metrics that track with regressions so profiling targets the right signals. |
| **Performance QA and release owners** | Compare builds on a fixed device with a consistent table; share ranked associations without a full ML pipeline. |
| **Technical artists and content leads** | Connect authoring choices (complexity, density) to load and runtime outcomes when discussing budgets with engineering. |

You do **not** need a predictive model to get value here. If you later want Ridge regression, random forests, or full EDA, treat this notebook as the **first filter** on which columns matter.
## Repository layout
Paths are relative to the **Model-Performance-Correlation-Analysis** folder (set the notebook working directory to **Science** when you run it).
```
Model-Performance-Correlation-Analysis/
 model-properties-performance-correlation.ipynb
 model_correlation_utils.py
 requirements.txt
 model-correlation-sample-data/
   model_properties.csv    # geometry / density scalars per model
   model_performance.csv   # load and runtime outcomes per model
   models_merged.csv       # inner join on model_name + urn (default input)
```
| File | Role |
|------|------|
| `model_properties.csv` | Property side of the join (e.g. poly count, objects, unit volume, optional ModelStats peaks). |
| `model_performance.csv` | Outcome side (init time, stage duration, FPS, memory, timing milestones). |
| `models_merged.csv` | Pre-merged demo table — default when `DATA_SOURCE = "merged"`. |
## Quick start
```sh
cd Model-Performance-Correlation-Analysis
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Open **`model-properties-performance-correlation.ipynb`**, run all cells. Demo data loads from `model-correlation-sample-data/`.
### Using your own data
1. Build one CSV (or merge property + performance files on **`model_name`** or **`urn`**).
2. In the notebook, set `DATA_SOURCE = "custom"` and point **`CUSTOM_MERGED_CSV`** at your file.
3. Adjust **`PRIMARY_OUTCOME`** and column lists in `model_correlation_utils.py` if your export uses different names.
## Method in one paragraph
We use **Spearman ρ** for each property × outcome pair with enough non-null samples. Results are sorted by **|ρ|** per outcome so the strongest monotonic associations appear first. Optional export writes `correlation_results.csv` next to the input data folder.
## Dependencies
See **`requirements.txt`**: pandas, matplotlib, seaborn, scipy, ipykernel.



