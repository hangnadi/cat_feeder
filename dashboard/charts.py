import pandas as pd
import matplotlib.pyplot as plt

def plot_daily_totals(csv_path: str):
    df = pd.read_csv(csv_path)
    if df.empty:
        print("No data to plot.")
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df[df["action"] == "FEED"]
    daily = df.groupby(df["timestamp"].dt.date)["grams"].sum()
    daily.plot(kind="bar")
    plt.title("Daily Dispensed Food (g)")
    plt.xlabel("Date")
    plt.ylabel("Grams")
    plt.tight_layout()
    plt.show()
