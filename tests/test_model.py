from sim.model import run_once

def test_run():
    cfg = dict(arrival_rate=0.8, process_time_mean=0.9, qc_fail_prob=0.05, breakdown_mtf=60, repair_time_mean=5, duration_min=30)
    res = run_once(cfg, seed=1)
    assert 'throughput' in res and 'timeline' in res
