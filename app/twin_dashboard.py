import streamlit as st
import yaml, plotly.graph_objects as go
from sim.model import run_once
from utils.kpi import summarize

st.set_page_config(page_title="Digital Twin", layout="wide")
st.title("🧪 Digital Twin — Conveyor + Station + QC")

with open('configs/defaults.yaml','r') as f:
    CFG = yaml.safe_load(f)

arrival = st.sidebar.slider("Arrival rate (items/min)", 0.1, 2.0, float(CFG['sim']['arrival_rate']), 0.1)
ptime   = st.sidebar.slider("Process time mean (min)", 0.2, 2.0, float(CFG['sim']['process_time_mean']), 0.1)
qcfail  = st.sidebar.slider("QC fail prob", 0.0, 0.3, float(CFG['sim']['qc_fail_prob']), 0.01)
mtf     = st.sidebar.slider("Mean time to failure (min)", 10.0, 180.0, float(CFG['sim']['breakdown_mtf']), 5.0)
rt      = st.sidebar.slider("Repair time mean (min)", 1.0, 20.0, float(CFG['sim']['repair_time_mean']), 1.0)
dur     = st.sidebar.slider("Duration (min)", 60, 480, int(CFG['sim']['duration_min']), 30)

if st.button("Run Simulation"):
    cfg = dict(arrival_rate=arrival, process_time_mean=ptime, qc_fail_prob=qcfail, breakdown_mtf=mtf, repair_time_mean=rt, duration_min=dur)
    res = run_once(cfg, seed=7)
    st.metric("Throughput", res['throughput'])
    st.metric("Scrap", res['scrap'])
    k = summarize(res['timeline'])

    # State timeline
    states = {'IDLE':0,'BUSY':1,'DOWN':-1}
    xs = [t for t,_ in res['timeline']]
    ys = [states[s] for _,s in res['timeline']]
    fig = go.Figure(go.Scatter(x=xs, y=ys, mode='lines+markers', name='state'))
    fig.update_layout(yaxis=dict(tickmode='array', tickvals=[-1,0,1], ticktext=['DOWN','IDLE','BUSY']), xaxis_title='time (min)')
    st.plotly_chart(fig, use_container_width=True)

    st.write("Uptime:", round(k['uptime'],1), "min | Downtime:", round(k['downtime'],1), "min | Utilization:", round(100*k['busy']/max(1,k['uptime']),1), "%")
else:
    st.info("Adjust parameters and click **Run Simulation**.")
