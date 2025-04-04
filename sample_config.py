# Sample Configuration File
# Copy this file to config.py and update with your own settings

# Paths to your exported data folders
# Replace these with the actual paths to your data exports
CHATGPT_FOLDER = 'your_chatgpt_export_folder'  # Example: 'chatgpt_data_export'
CLAUDE_FOLDER = 'your_claude_export_folder'    # Example: 'claude_data_export'

# Your local timezone
# Common options: 'US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Kolkata', 'Asia/Tokyo'
LOCAL_TIMEZONE = 'Asia/Kolkata'

# Output settings
OUTPUT_DIRECTORY = 'visualizations'
SAVE_IMAGES = True
IMAGE_DPI = 300

# Visualization settings
COLOR_SCHEME_CHATGPT = 'Greens'  # Options: 'Greens', 'Blues', 'YlGn', etc.
COLOR_SCHEME_CLAUDE = 'Oranges'  # Options: 'Oranges', 'Reds', 'YlOrBr', etc.
FIGURE_WIDTH = 15
FIGURE_HEIGHT = 8 