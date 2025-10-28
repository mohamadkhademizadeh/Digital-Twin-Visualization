import yaml, json
from sim.model import run_once

if __name__ == "__main__":
    cfg = yaml.safe_load(open('configs/defaults.yaml','r'))['sim']
    res = run_once(cfg, seed=42)
    print(json.dumps(res)[:200], "...")
