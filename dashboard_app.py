import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Energy Monitoring Dashboard", layout="wide")

# --- Load Data ---
def load_data():
    try:
        df = pd.read_csv("data/energy_data.csv")  # adjust path if needed
    except FileNotFoundError:
        st.error("⚠️ energy_data.csv not found in the 'data' folder.")
        st.stop()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # If 'energy_usage' is missing, compute it (assuming power * duration exists)
    if "energy_usage" not in df.columns:
        if "power" in df.columns and "duration" in df.columns:
            df["energy_usage"] = df["power"] * df["duration"]
        else:
            st.error("Missing 'energy_usage' or 'power' and 'duration' columns.")
            st.stop()

    return df


# --- Main Dashboard ---
def main():
    st.title("🔌 Office Energy Monitoring Dashboard")
    df = load_data()

    latest = df.iloc[-1]

    # Metrics Section
    st.markdown("### 📊 Current Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🔋 Current Usage (kWh)", f"{latest['energy_usage']:.2f}")
    col2.metric("📅 Last Updated", latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S'))
    col3.metric("💡 Active Device", latest['device'])

    st.markdown("---")

    # Time Filter
    st.markdown("### ⏱️ Filter Data by Time Range")
    hours = st.slider("Select number of past hours to analyze", min_value=1, max_value=48, value=6)
    time_threshold = pd.Timestamp.now() - pd.Timedelta(hours=hours)
    filtered_df = df[df["timestamp"] >= time_threshold]

    if filtered_df.empty:
        st.warning("No data available for the selected time range.")
        return

    # --- Bar Plot of Energy Usage per Device ---
    st.markdown("### 📶 Energy Usage by Device")
    device_usage = filtered_df.groupby("device")["energy_usage"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 3))  # Smaller size
    device_usage.plot(kind="bar", color="#5c9eff", ax=ax)
    ax.set_ylabel("Energy Usage (kWh)", fontsize= 6)
    ax.set_xlabel("Device", fontsize= 6)
    ax.set_title(f"Energy Consumption by Device (Last {hours} hrs)", fontsize = 6)
    ax.tick_params(axis='x', labelsize=4)  
    ax.tick_params(axis='y', labelsize=4)
    st.pyplot(fig)

    # --- Raw Data Option ---
    with st.expander("📄 Show Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
