import sys
import os
# add the root directory to the sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime, timedelta
from API.Database.Database import Database


# Fetch analytics data from Firebase
def get_analytics_data() -> dict:
    """
    Retrieves all analytics data from the Firebase Realtime Database.
    """
    db = Database()
    analytics_ref = db.root_ref.child(
        "analytics").get()  # Retrieve all analytics data
    if analytics_ref is None:
        return {}
    return analytics_ref


# Aggregate analytics data to compute metrics
def aggregate_analytics_data(analytics_data: dict) -> dict:
    """
    Aggregates event counts and user engagement from the analytics data.
    :param analytics_data: Raw data fetched from Firebase
    :return: Dictionary containing event count and user engagement
    """
    event_count = defaultdict(int)  # To store counts of each event type
    # User engagement per event type
    user_engagement = defaultdict(lambda: defaultdict(int))

    # Loop through analytics data
    for event_name, users in analytics_data.items():
        for user_id, timestamps in users.items():
            event_count[event_name] += len(timestamps)  # Count total events
            # Count events per user
            user_engagement[user_id][event_name] += len(timestamps)

    return {
        "event_count": dict(event_count),
        "user_engagement": dict(user_engagement),
    }


# Plot the event counts
def plot_events_count(events_count: dict):
    """
    Visualizes the event counts using a bar chart.
    - The x labels are kept straight with smaller fonts.
    - The y-axis maximum is set to 50 (or more if needed).
    - The graph is saved as a file in the 'Analytics' directory.
    - Increases horizontal space between x labels by making the graph wider.
    :param events_count: Dictionary with event names as keys and their respective counts as values
    """
    events = list(events_count.keys())
    counts = list(events_count.values())

    # Increase the figure size to make the graph wider (more space between x labels)
    plt.figure(figsize=(14, 6))  # Adjust the width (14) to spread out the labels

    # Create the bar chart
    plt.bar(events, counts, color='blue')

    # Set labels and title
    plt.xlabel('Event Type', fontsize=12, labelpad=15)  # Adds vertical space between x-label and graph
    plt.ylabel('Count', fontsize=12)
    plt.title('Events Count in Analytics', fontsize=14)

    # Ensure x labels are straight and use smaller font
    plt.xticks(fontsize=10)  # Set font size for x labels

    # Set y-axis limit to 50 or more if needed
    plt.ylim(0, max(50, max(counts) + 5))  # y-axis minimum is 0, max is 50 or slightly more than the highest count

    # Save the plot as a file in the Analytics directory
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events_count.png')
    plt.savefig(output_path)

    print(f"Graph saved at: {output_path}")


# Plot the user event counts
def plot_user_events_count(user_engagement: dict):
    """
    Visualizes the user event counts using a bar chart.
    - The x labels are user IDs.
    - The y-axis shows the number of events each user has.
    - The graph is saved as a file in the 'Analytics' directory.
    :param user_engagement: Dictionary with user IDs as keys and event counts as values
    """
    users = list(user_engagement.keys())
    events_count = [sum(events.values()) for events in user_engagement.values()]

    # Increase the figure size to make the graph wider (more space between x labels)
    plt.figure(figsize=(14, 6))  # Adjust the width to spread out the labels if necessary

    # Create the bar chart
    plt.bar(users, events_count, color='green')

    # Set labels and title
    plt.xlabel('Users', fontsize=12, labelpad=15)  # Adds vertical space between x-label and graph
    plt.ylabel('Count', fontsize=12)
    plt.title('User Events Count in Analytics', fontsize=14)

    # Ensure x labels are straight and use smaller font
    plt.xticks(fontsize=10)  # Set font size for x labels

    # Set y-axis limit to 50 or more if needed
    plt.ylim(0, max(50, max(events_count) + 5))  # y-axis minimum is 0, max is 50 or slightly more than the highest count

    # Save the plot as a file in the Analytics directory
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_events_count.png')
    plt.savefig(output_path)

    print(f"Graph saved at: {output_path}")


# Plot the user growth over time
def plot_user_growth(user_data: dict):
    """
    Plots a line chart showing the number of users created over time.
    :param user_data: Dictionary where keys are user_ids and values are timestamps of user creation
    """
    # Extract the creation timestamps from the 'user_created' event within each user_id
    creation_dates = [datetime.strptime(timestamp, "%Y%m%d%H%M%S") for user_id, timestamps in user_data['user_created'].items() for timestamp in timestamps.keys()]
    creation_dates.sort()  # Sort dates in ascending order
    
    # Initialize user count and cumulative count for plotting
    cumulative_user_count = []
    count = 0

    # Add the starting point (16/10/24, 0)
    start_date_point = datetime(2024, 10, 16)
    cumulative_user_count.append((start_date_point, 0))

    # Append each user creation date and increment count
    for date in creation_dates:
        count += 1  # Increment user count for each creation date
        cumulative_user_count.append((date, count))

    # Separate the dates and user counts for plotting
    dates, user_counts = zip(*cumulative_user_count)
    
    # Create x-axis values with labels every 3 days from 16/10/24 to 17/11/24
    start_date = datetime(2024, 10, 16)
    end_date = datetime(2024, 11, 17)
    date_range = [start_date + timedelta(days=3 * i) for i in range((end_date - start_date).days // 3 + 1)]

    # Plot the line chart
    plt.figure(figsize=(12, 6))
    plt.plot(dates, user_counts, marker='o', color='red', linestyle='-', linewidth=2, markersize=4)  # Reduced marker size
    
    # Set labels and title
    plt.xlabel('Date', fontsize=12, labelpad=15)
    plt.ylabel('User Count', fontsize=12)
    plt.title('Number of Users Over Time', fontsize=14)

    # Format the x-axis to show date every 3 days, with no rotation
    plt.xticks(date_range, [date.strftime('%d/%m/%y') for date in date_range], fontsize=10)

    # Set y-axis limit to 50 or higher based on user count
    plt.ylim(0, max(50, max(user_counts) + 5))

    # Save the plot as a file in the Analytics directory
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_growth.png')
    plt.savefig(output_path)
    
    print(f"Graph saved at: {output_path}")


# Main function to fetch, aggregate, and visualize the analytics data
def main():
    """
    Main function that retrieves the analytics data, aggregates it, and visualizes the results.
    """
    # Step 1: Fetch analytics data
    analytics_data = get_analytics_data()
    if not analytics_data:
        print("No analytics data found.")
        return

    # Step 2: Aggregate the data
    aggregated_data = aggregate_analytics_data(analytics_data)

    # Step 3: Plot event counts
    plot_events_count(aggregated_data["event_count"])

    # Step 4: Plot user events count
    plot_user_events_count(aggregated_data["user_engagement"])

    # Step 5: Plot user growth over time
    plot_user_growth(analytics_data)


if __name__ == "__main__":
    main()