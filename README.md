# Digital-Twin-Visualization

A **Python digital twin** for a simple manufacturing cell:
- **SimPy**-based discrete-event simulation for a **conveyor + station + QC** cell.
- Live **Streamlit dashboard** with 3D-like plots (Plotly) and state timelines.
- Inject faults, change speeds, and watch KPIs (throughput, WIP, utilization, scrap).

> Designed to showcase systems thinking, data viz, and light simulation skills.

---

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/twin_dashboard.py
```

---

## Layout
```
Digital-Twin-Visualization/
├── app/twin_dashboard.py      # interactive UI
├── sim/model.py               # SimPy cell model
├── utils/kpi.py               # KPI calculators
├── configs/defaults.yaml
├── scripts/run_batch.py       # headless batch runs for experiments
├── tests/test_model.py
├── requirements.txt
└── README.md
```
