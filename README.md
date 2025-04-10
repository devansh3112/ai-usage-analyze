# AI-Usage-Analyzer

📊 Visualize and analyze your usage patterns across ChatGPT and Claude AI assistants

![GitHub license](https://img.shields.io/github/license/devansh3112/ai-usage-analyze)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

## Overview

This tool generates beautiful GitHub-style heat maps to visualize when you use ChatGPT and Claude throughout the year. Compare your usage patterns, analyze your AI interaction habits, and discover insights about your productivity rhythms.

**Easily answer questions like:**
- Which AI assistant do I use more frequently?
- What days/times am I most active with each assistant?
- How has my usage pattern changed over time?
- When do I prefer Claude vs ChatGPT?

## Heat Map Visualizations

### Comparison Heat Map
This visualization shows which AI assistant you use more frequently on each day:
- **Orange cells**: Days where Claude usage dominates
- **Green cells**: Days where ChatGPT usage dominates
- **Gray cells**: Days with equal usage of both platforms
- **Darker color intensity**: Higher number of conversations

![Comparison Heat Map](example_images/comparison_heatmap_example.png)

### Individual Assistant Heat Maps

See your usage patterns for each assistant individually:

**Claude Usage Heat Map** (Orange intensity indicates conversation frequency)
![Claude Heat Map](example_images/claude_heatmap_example.png)

**ChatGPT Usage Heat Map** (Green intensity indicates conversation frequency)
![ChatGPT Heat Map](example_images/chatgpt_heatmap_example.png)

## Understanding the Heat Maps

- **Weekly Patterns**: Identify which days of the week you use AI assistants most frequently
- **Monthly Trends**: See how your usage changes throughout the year
- **Assistant Preference**: Discover which assistant you prefer for different time periods
- **Usage Intensity**: Brighter colors indicate more conversations on that day
- **Year-over-Year Analysis**: Generate visualizations for multiple years to track changes

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/devansh3112/ai-usage-analyze.git
   cd ai-usage-analyze
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Export your conversation data:
   - **ChatGPT**: Settings → Data controls → Export
   - **Claude**: Settings → Account → Data → Export data

4. Configure your data paths:
   - Update the `chatgpt_folder` and `claude_folder` paths in `generate_heatmap.py`
   - Set your `local_tz` timezone (default is 'Asia/Kolkata')

5. Generate visualizations:
   ```bash
   python generate_heatmap.py
   ```
   
   Or use the provided batch file:
   ```bash
   generate_visualizations.bat
   ```

For more detailed instructions, see the [detailed documentation](README-detailed.md).

## Features

- **Multiple AI Assistants**: Compare usage between ChatGPT and Claude
- **Year-by-Year Analysis**: Generate separate visualizations for each year
- **Beautiful Heat Maps**: GitHub-style activity visualization 
- **Custom Time Zones**: Adjust for your local time zone
- **Detailed Statistics**: See your most active days and total usage counts

## Documentation

For complete documentation, including setup instructions, usage examples, and customization options, see our [main README](README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
