from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def simulate_poisson_process(lambda_rate, T, sample_period):
    # Step 1: Simulate the actual event times with a Poisson process
    event_times = []
    time = 0
    while time < T:
        time_to_next_event = np.random.exponential(1/lambda_rate)
        time += time_to_next_event
        if time < T:
            event_times.append(time)
    event_series = pd.Series(event_times, name="Events")

    # Step 2: Take samples at regular intervals, noting the last event time
    sample_times = np.arange(0, T, sample_period)
    last_event_times = []
    current_event = 0
    for sample_time in sample_times:
        # Find the last event time before the sample was taken
        while current_event < len(event_times) - 1 and event_times[current_event + 1] < sample_time:
            current_event += 1
        last_event_times.append(event_times[current_event] if current_event < len(event_times) and event_times[current_event] < sample_time else None)

    # Convert samples to a pandas DataFrame
    samples_df = pd.DataFrame({
        "SAMPLE TIME": sample_times,
        "LAST EVENT TIME": last_event_times
    })

    return event_series, samples_df

# Parameters
expected_interval = 2
lambda_rate = 1/expected_interval # rate of events per unit time
T = expected_interval * 10000    # total time
s = 1          # sample period

# Simulate and get DataFrame
events, samples = simulate_poisson_process(lambda_rate, T, s)
samples["TIME SINCE LAST"] = samples["SAMPLE TIME"] - samples["LAST EVENT TIME"]

def n_trials(n):
    trial_means = []
    total_intervals = []
    for i in range(n):
        T = expected_interval * 1000 * (i+1)
        events, samples = simulate_poisson_process(lambda_rate, T, s)
        samples["TIME SINCE LAST"] = samples["SAMPLE TIME"] - samples["LAST EVENT TIME"]
        trial_means.append(samples["TIME SINCE LAST"].mean())
        total_intervals.append(T)
    # trial_means = pd.Series(trial_means)
    df = pd.DataFrame({
        "MEAN TIME SINCE LAST": trial_means,
        "TOTAL INTERVAL": total_intervals,
    })
    plt.figure(figsize=(8,4))
    plt.plot(df["TOTAL INTERVAL"], df["MEAN TIME SINCE LAST"])
    plt.plot([0,len(df)],[expected_interval, expected_interval],label="True Inter-arrival Mean")
    plt.title("Simulated Estimation of Inter-arrival Time with Deterministic Sampling Rate")
    plt.xlabel("Total Interval")
    plt.ylabel("Estimated Scale Parameter")
    plt.tight_layout()
    plt.savefig("fig/poisson_simulation.pdf")
    return df["MEAN TIME SINCE LAST"]

print("Event Times:", events)
print("Sample DataFrame:")
print(samples)
print(n_trials(100), expected_interval)
