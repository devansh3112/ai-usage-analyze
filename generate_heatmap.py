import json
import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pytz
import os
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta

# Configuration
# You should update these paths to your own data export locations
chatgpt_folder = os.getenv("CHATGPT_FOLDER")
claude_folder = os.getenv("CLAUDE_FOLDER")
local_tz = 'Asia/Kolkata'  # Set to your local timezone

# Get year from command line argument if provided, otherwise process all years
if len(sys.argv) > 1:
    try:
        year_to_visualize = int(sys.argv[1])
        process_all_years = False
    except ValueError:
        print(
            f"Invalid year format: {sys.argv[1]}, processing all available years instead")
        process_all_years = True
else:
    process_all_years = True
    print("No year specified, processing all available years")

# Create output directory if it doesn't exist
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

# Load ChatGPT data
try:
    with open(f'{chatgpt_folder}/conversations.json', 'r') as f:
        oai_convs = json.load(f)
    print(f"Loaded {len(oai_convs)} ChatGPT conversations")
except Exception as e:
    print(f"Error loading ChatGPT data: {e}")
    print("Make sure you've updated the 'chatgpt_folder' variable with your data export path")
    oai_convs = []

# Load Claude data
try:
    with open(f'{claude_folder}/conversations.json', 'r') as f:
        claude_convs = json.load(f)
    print(f"Loaded {len(claude_convs)} Claude conversations")
except Exception as e:
    print(f"Error loading Claude data: {e}")
    print("Make sure you've updated the 'claude_folder' variable with your data export path")
    claude_convs = []

# Process ChatGPT timestamps
oai_convo_times = []
for conv in oai_convs:
    # Given Unix timestamp
    unix_timestamp = conv['create_time']

    # Convert to UTC datetime
    utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

    # Convert UTC datetime to local timezone
    local_datetime = utc_datetime.astimezone(pytz.timezone(local_tz))
    oai_convo_times.append(local_datetime)

# Process Claude timestamps


def convert_claude_timestamps(convs, local_tz):
    convo_times = []
    for conv in convs:
        # Parse ISO format string to datetime
        utc_datetime = datetime.strptime(
            conv['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

        # Add UTC timezone info
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)

        # Convert UTC to local timezone
        local_datetime = utc_datetime.astimezone(pytz.timezone(local_tz))
        convo_times.append(local_datetime)

    return convo_times


claude_convo_times = convert_claude_timestamps(claude_convs, local_tz)

# Get all available years from the data
all_years = set()
for dt in oai_convo_times:
    all_years.add(dt.year)
for dt in claude_convo_times:
    all_years.add(dt.year)

all_years = sorted(list(all_years))
print(f"Found conversations from these years: {all_years}")

# Define a function to create a heatmap for a single assistant


def create_single_heatmap(convo_times, year, name, color_map, output_file=None):
    # Convert convo_times to dates and filter for the given year
    just_dates = [convo.date() for convo in convo_times if convo.year == year]

    date_counts = Counter(just_dates)
    total_convos = sum(date_counts.values())

    if total_convos == 0:
        print(
            f"No {name} conversations found for year {year}, skipping visualization")
        return False

    # Create a full year date range for the calendar
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()

    total_days = (end_date - start_date).days + 1
    date_range = [start_date + timedelta(days=i) for i in range(total_days)]

    # Prepare data for plotting
    data = []
    for date in date_range:
        week = ((date - start_date).days + start_date.weekday()) // 7
        day_of_week = date.weekday()
        count = date_counts.get(date, 0)
        data.append((week, day_of_week, count))

    weeks_in_year = (end_date - start_date).days // 7 + 1

    # Find the most active day
    max_count_date = max(date_counts.items(),
                         key=lambda x: x[1]) if date_counts else (None, 0)
    max_count = max_count_date[1] if max_count_date[0] is not None else 0

    # Calculate p90 for color scaling
    p90_count = np.percentile(
        list(date_counts.values()), 90) if date_counts else 1

    # Plot the heatmap
    plt.figure(figsize=(15, 8))
    ax = plt.gca()
    ax.set_aspect('equal')

    for week, day_of_week, count in data:
        color = color_map(
            (count + 1) / p90_count) if count > 0 else 'lightgray'
        rect = patches.Rectangle(
            (week, day_of_week), 1, 1, linewidth=0.5, edgecolor='black', facecolor=color)
        ax.add_patch(rect)

    # Replace week numbers with month names below the heatmap
    month_starts = [start_date + timedelta(days=i) for i in range(total_days)
                    if (start_date + timedelta(days=i)).day == 1]
    for month_start in month_starts:
        week = (month_start - start_date).days // 7
        plt.text(week + 0.5, 7.75, month_start.strftime('%b'),
                 ha='center', va='center', fontsize=10, rotation=0)

    # Adjustments for readability
    ax.set_xlim(-0.5, weeks_in_year + 0.5)
    ax.set_ylim(-0.5, 8.5)
    plt.title(
        f'{year} {name} Conversation Heatmap (total={total_convos})\n'
        f'Most active day: {max_count_date[0]} with {max_count} convos.',
        fontsize=16
    )
    plt.xticks([])
    plt.yticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.gca().invert_yaxis()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to {output_file}")
    else:
        plt.show()

    plt.close()
    return True

# Define the comparison heatmap function


def create_comparison_heatmap(claude_times, openai_times, year, output_file=None):
    # Convert times to dates and filter for the given year
    claude_dates = [convo.date()
                    for convo in claude_times if convo.year == year]
    openai_dates = [convo.date()
                    for convo in openai_times if convo.year == year]

    claude_counts = Counter(claude_dates)
    openai_counts = Counter(openai_dates)

    # Calculate totals
    claude_total = sum(claude_counts.values())
    openai_total = sum(openai_counts.values())
    combined_total = claude_total + openai_total

    if combined_total == 0:
        print(
            f"No conversations found for year {year}, skipping comparison visualization")
        return False

    # Create a full year date range
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()
    total_days = (end_date - start_date).days + 1
    date_range = [start_date + timedelta(days=i) for i in range(total_days)]

    # Prepare data for plotting - Reverse the day_of_week calculation
    data = []
    for date in date_range:
        week = ((date - start_date).days + start_date.weekday()) // 7
        # Reverse the order: 0 (Mon) -> 6, 1 (Tue) -> 5, etc.
        day_of_week = 6 - date.weekday()  # This reverses the order
        claude_count = claude_counts.get(date, 0)
        openai_count = openai_counts.get(date, 0)
        dominant_llm = 'claude' if claude_count > openai_count else 'openai' if openai_count > claude_count else 'tie'
        count = max(claude_count, openai_count)
        data.append((week, day_of_week, count, dominant_llm))

    weeks_in_year = (end_date - start_date).days // 7 + 2

    # Calculate overall p90 for color scaling
    all_counts = list(claude_counts.values()) + list(openai_counts.values())
    p90_count = np.percentile(all_counts, 90) if all_counts else 1

    # Plot setup
    plt.figure(figsize=(20, 8))
    ax = plt.gca()
    ax.set_aspect('equal')

    # Plot rectangles
    for week, day_of_week, count, dominant_llm in data:
        if count > 0:
            # Start at 0.1 (10%) intensity and scale up to 1
            intensity = min(0.1 + (count / p90_count * 0.9), 1)
            color = plt.cm.Oranges(intensity) if dominant_llm == 'claude' else \
                plt.cm.Greens(intensity) if dominant_llm == 'openai' else \
                'lightgray'
        else:
            color = '#F5F5F5'  # Light gray for empty cells

        rect = patches.Rectangle(
            (week, day_of_week), 1, 1,
            linewidth=1,
            edgecolor='black',
            facecolor=color
        )
        ax.add_patch(rect)

    # Add month labels
    month_starts = [start_date + timedelta(days=i) for i in range(total_days)
                    if (start_date + timedelta(days=i)).day == 1]
    for month_start in month_starts:
        week = (month_start - start_date).days // 7
        plt.text(week + 0.5, -0.5, month_start.strftime('%b'),
                 ha='center', va='top', fontsize=10)

    # Find most active days
    claude_max_date = max(claude_counts.items(),
                          key=lambda x: x[1]) if claude_counts else (None, 0)
    openai_max_date = max(openai_counts.items(),
                          key=lambda x: x[1]) if openai_counts else (None, 0)

    # Title and formatting
    plt.title(
        f'{year} AI Conversation Comparison (Total: {combined_total:,} conversations)\n'
        f'Claude total: {claude_total:,}, max: {claude_max_date[1]} on {claude_max_date[0]}\n'
        f'OpenAI total: {openai_total:,}, max: {openai_max_date[1]} on {openai_max_date[0]}',
        fontsize=12, pad=15
    )

    # Adjust axis limits and labels
    plt.xlim(-0.5, weeks_in_year + 0.5)
    plt.ylim(-1, 7)
    plt.xticks([])

    # Set y-ticks at the center of each box (offset by 0.5)
    plt.yticks([i + 0.5 for i in range(7)],
               ['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon'])

    # Adjust y-axis label positioning
    ax.yaxis.set_tick_params(pad=10)

    # Add legend
    legend_elements = [
        patches.Patch(facecolor=plt.cm.Oranges(0.7), label='Claude Dominant'),
        patches.Patch(facecolor=plt.cm.Greens(0.7), label='OpenAI Dominant'),
        patches.Patch(facecolor='lightgray', label='Tie')
    ]
    plt.legend(handles=legend_elements, loc='center left',
               bbox_to_anchor=(1.02, 0.5))

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to {output_file}")
    else:
        plt.show()

    plt.close()
    return True


# Generate visualizations
years_to_process = all_years if process_all_years else [year_to_visualize]

print(f"Generating visualizations for years: {years_to_process}")

for year in years_to_process:
    print(f"\nProcessing year {year}...")
    claude_success = create_single_heatmap(claude_convo_times, year, "Claude", plt.cm.Oranges,
                                           output_file=f"{output_dir}/claude_heatmap_{year}.png")

    chatgpt_success = create_single_heatmap(oai_convo_times, year, "ChatGPT", plt.cm.Greens,
                                            output_file=f"{output_dir}/chatgpt_heatmap_{year}.png")

    if claude_success or chatgpt_success:
        create_comparison_heatmap(claude_convo_times, oai_convo_times, year,
                                  output_file=f"{output_dir}/comparison_heatmap_{year}.png")

print("\nVisualization process complete!")
