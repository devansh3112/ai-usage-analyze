# AI-Usage-Analyzer

📊 Visualize and analyze your usage patterns across ChatGPT and Claude AI assistants

![GitHub license](https://img.shields.io/github/license/yourusername/ai-usage-analyzer)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

## Overview

This tool generates beautiful GitHub-style heat maps to visualize when you use ChatGPT and Claude throughout the year. Compare your usage patterns, analyze your AI interaction habits, and discover insights about your productivity rhythms.

**Easily answer questions like:**
- Which AI assistant do I use more frequently?
- What days/times am I most active with each assistant?
- How has my usage pattern changed over time?
- When do I prefer Claude vs ChatGPT?

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-usage-analyzer.git
   cd ai-usage-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Export your conversation data:
   - **ChatGPT**: Settings → Data controls → Export
   - **Claude**: Settings → Account → Data → Export data

4. Configure your data paths:
   - Update the paths in `generate_heatmap.py`

5. Generate visualizations:
   ```bash
   python generate_heatmap.py
   ```

For more detailed instructions, see the [full documentation](README.md).

## Documentation

For complete documentation, including setup instructions, usage examples, and customization options, see our [main README](README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
