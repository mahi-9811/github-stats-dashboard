# 📊 GitHub Stats Dashboard

A comprehensive Streamlit web application for analyzing GitHub user repositories with advanced analytics, performance scoring, and AI-generated insights.

## 🌟 Features

### 📊 Overview Tab
- **Developer Profile Score** (0-100) - Comprehensive scoring based on:
  - Star Score (popularity of repositories)
  - Activity Score (commit history)
  - Diversity Score (programming languages used)
  - Maturity Score (repository forks)
  - Consistency Score (number of projects)
- **AI-Generated Developer Bio** - Automatically generated professional bio based on GitHub data
- **Key Statistics** - Total repos, stars, forks, and commits at a glance
- **Top 10 Most Starred Repositories** - Bar chart visualization
- **Languages Distribution** - Pie chart showing tech stack

### 📈 Analytics Tab
- **Detailed Statistics** - Average metrics across all repositories
- **Stars Distribution** - Histogram showing star distribution
- **Commits by Project** - Top projects by commit count
- **Project Efficiency** - Stars earned per commit ratio
- **Language Performance** - Average metrics broken down by programming language
- **Advanced Correlations** - Scatter plots analyzing stars vs commits

### 📋 Projects Tab
- **Complete Repository List** - Browse all repositories
- **Search Functionality** - Filter by repository name or language
- **Sorting Options** - Sort by stars, commits, forks, or name
- **Direct GitHub Links** - Click to view repositories on GitHub

### 🔬 Detailed Analysis Tab
- **Efficiency Metrics** - Which projects get the most stars with minimal effort
- **Fork Analysis** - Most forked repositories relative to stars
- **Comprehensive Metrics Table** - All projects with calculated metrics
- **Key Insights** - Highlights of most starred, most forked, and most active projects

### 📥 PDF Report Download
- Download a professional PDF report with:
  - Developer Profile Score breakdown
  - AI-generated bio
  - Key insights and statistics
  - Top 10 repositories table

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Python web framework
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Data manipulation
- **Visualizations**: [Plotly](https://plotly.com/) - Interactive charts
- **Database**: SQLite - Local data storage
- **APIs**: 
  - GitHub API - Repository data
  - OpenAI API - AI-generated bios (optional)
- **Report Generation**: ReportLab - PDF creation

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git (for cloning)

### Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/mahi-9811/github-stats-dashboard.git
cd github-stats-dashboard
```

2. **Create a virtual environment:**
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
```
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_github_username
OPENAI_API_KEY=your_openai_api_key_here (optional)
```

5. **Run the app:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🔑 Getting API Keys

### GitHub Token
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `public_repo` - Read public repositories
   - `repo` - General repository access
4. Copy and save the token

### OpenAI API Key (Optional)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and save it

> Note: The app works without OpenAI API key - it will generate template bios instead

## 🚀 Live Demo

Visit the deployed application:
https://mahi-9811-github-stats-dashboard.streamlit.app/

### Example Users to Try
- `torvalds` - Linux creator
- `guido` - Python creator
- `facebook` - Facebook organization
- `microsoft` - Microsoft organization
- `google` - Google organization
- `netflix` - Netflix organization

## 📊 Scoring Methodology

The Developer Profile Score (0-100) uses logarithmic scaling to fairly evaluate developers of all sizes:

**Star Score (30 points max)** - Based on total stars across repositories using the formula `log₁₀(total_stars + 1) × 5`. This measures the popularity and usefulness of your projects.

**Activity Score (25 points max)** - Based on total commits using `log₁₀(total_commits + 1) × 4`. This reflects how actively you contribute and maintain your work.

**Diversity Score (20 points max)** - Based on the number of different programming languages used, calculated as `(languages / 15) × 20`. This shows your versatility across different tech stacks.

**Maturity Score (15 points max)** - Based on average forks per repository using `log₁₀(avg_forks + 1) × 3`. Forks indicate how useful and reusable your code is to others.

**Consistency Score (10 points max)** - Based on the number of projects you maintain, calculated as `(projects / 50) × 10`. This demonstrates your consistency and productivity.

The logarithmic approach ensures fair scoring for both individual developers and large organizations, preventing massive numbers from creating disproportionately high scores.

## 📁 Project Structure

```
github-stats-dashboard/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database operations
├── github_api.py          # GitHub API integration
├── analytics.py           # Scoring and insights generation
├── ai_helper.py           # OpenAI integration for bio generation
├── pdf_report.py          # PDF report generation
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Usage

1. **Search for a Developer/Organization:**
   - Enter a GitHub username in the sidebar
   - Click "Analyze User"

2. **Explore the Data:**
   - **Overview**: Quick stats and visualizations
   - **Analytics**: Detailed metrics and correlations
   - **Projects**: Browse and search repositories
   - **Detailed Analysis**: Advanced metrics and insights

3. **Download Report:**
   - Click "📥 Download PDF Report" in the sidebar
   - Save the professional report locally

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/mahi-9811/github-stats-dashboard/issues)
2. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)

## 🎯 Roadmap

Planned features:
- [ ] Real-time data updates
- [ ] Developer comparison (side-by-side)
- [ ] Trend analysis over time
- [ ] Custom scoring weights
- [ ] Export to CSV
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] GitHub Actions integration

## 👨‍💻 Author

**Mahip Patel**
- GitHub: [@mahi-9811](https://github.com/mahi-9811)
- Project: [GitHub Stats Dashboard](https://github.com/mahi-9811/github-stats-dashboard)

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Plotly Documentation](https://plotly.com/python/)

---

**Made with ❤️ using Python and Streamlit**
