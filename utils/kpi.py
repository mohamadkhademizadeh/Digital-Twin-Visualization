import pandas as pd

def summarize(timeline):
    # timeline: [(t, state)]
    df = pd.DataFrame(timeline, columns=['t','state'])
    df = df.sort_values('t').reset_index(drop=True)
    if df.empty:
        return dict(uptime=0, downtime=0, busy=0, idle=0)
    df['dt'] = df['t'].shift(-1) - df['t']
    df['dt'] = df['dt'].fillna(0)
    summ = df.groupby('state')['dt'].sum().to_dict()
    return dict(
        uptime = summ.get('BUSY',0)+summ.get('IDLE',0),
        downtime = summ.get('DOWN',0),
        busy = summ.get('BUSY',0),
        idle = summ.get('IDLE',0),
    )
