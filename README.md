# Python for Linguistic Data Analysis with VS Code and LLMs

A workshop repository for **Python programming**, **data analysis**, and **AI-assisted coding** focused on linguistic research.

This is a companion to the [CRC 1252 Research Data and Methods Workshop Series](https://sfb1252.github.io/talks/) at the University of Cologne.

---

## 🎯 Workshop Overview

This workshop illustrates some modern Python development skills for linguistic researchers, covering:

- **Python fundamentals** (pandas, NumPy, SciPy)
- **Interactive development** with Jupyter notebooks and VS Code
- **Statistical analysis** for linguistic data
- **Large Language Models (LLMs)** for code assistance and documentation
- **Git and GitHub** for version control and collaboration
- **Reproducible workflows** with virtual environments and dependency management

---

## 📋 Contents

### Example Project

**Head Nods Analysis** (`head-nods-example/`)
- Statistical comparison of head nod characteristics across languages
- Sample size assessment and power analysis
- Normality testing and comparative statistics

### Setup & Configuration

- `slides.qmd` - Quarto presentation (Python setup, LLM configuration, async agents)
- `requirements.txt` - Python dependencies
- `.gitignore` - Recommended git ignore rules
- `styles.css` - Presentation styling
- `example-scripts/` - Helper scripts for environment variable loading

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jobschepens/py-rdm.git
cd py-rdm
```

### 2. Set Up Python & Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scipy` - Statistical analysis
- `matplotlib` - Visualization
- `seaborn` - Statistical plotting
- `jupyter` - Interactive notebooks
- `ipython` - Enhanced Python shell

### 4. Set Up LLM Access (Optional)

Copy `example-scripts/load-env.sh` (macOS/Linux) or `load-env.ps1` (Windows) to your project root:

```bash
# macOS/Linux
source ./load-env.sh

# Windows PowerShell
. ./load-env.ps1
```

Create a `.env` file with your API credentials (ignored by git):

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SAIA_API_KEY=...
```

### 5. Start Working

**Run example analyses:**

```bash
# Head nods example
python head-nods-example/job-testanalysis2/code/sample_size_analysis.py
```

**Launch Jupyter:**

```bash
jupyter lab
```

---

## 📊 Folder Structure

```
py-rdm/
├── head-nods-example/
│   ├── data/                    # Input data (CSV)
│   ├── job-testanalysis2/
│   │   ├── code/               # Analysis scripts
│   │   ├── processed_data/     # Intermediate results
│   │   └── results/            # Outputs (plots, CSV, stats)
│   └── README.md
│
├── example-scripts/             # Helper scripts (env loading, etc.)
├── slides.qmd                   # Workshop presentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── LICENSE
```

---

## 💻 Workflow for Participants

### For Individual Analysis

1. **Clone or fork this repo**
2. **Create a folder** with your name/identifier: `analyses/your-name/`
3. **Write analysis scripts** in your folder
4. **Commit and push** to your fork (or to a branch if you have push access)

**Example:**

```bash
mkdir analyses/alice
cd analyses/alice
# Create your Python scripts here
python analyze_data.py
```

### Folder Organization Best Practices

```
analyses-alice/
├── code/
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
├── processed_data/
│   └── cleaned_data.csv
├── results/
│   ├── plots/
│   ├── summary.csv
│   └── report.md
└── README.md  # Document your analysis
```

---

## 📖 Resources

### LLM Integration

- [CoCo AI (GWDG Academic Cloud)](https://docs.hpc.gwdg.de/services/chat-ai/index.html)

### Git & GitHub

- [Git handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow guide](https://guides.github.com/introduction/flow/)
- [Fork and Pull Request workflow](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

---

## 🔧 Tools & Environment

### Recommended Setup

- **Python**: 3.9+ (3.11+ recommended)
- **Editor**: [Visual Studio Code](https://code.visualstudio.com/)
- **Terminal**: PowerShell (Windows) or Bash (macOS/Linux)
- **Version Control**: Git with GitHub

### VS Code Extensions

**Recommended:**
- Python (Microsoft)
- Jupyter (Microsoft)
- Pylance (Microsoft)
- Continue or GitHub Copilot Chat (AI assistance)

### Virtual Environments

Always use a virtual environment to isolate dependencies:

```bash
# Create
python -m venv .venv

# Activate
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate
deactivate
```

---

## 📝 Workflow Tips

### Running Scripts from the Correct Directory

Python scripts in subfolders use relative paths. Always run from the project root:

```bash
# ✅ Correct
python head-nods-example/job-testanalysis2/code/sample_size_analysis.py

# ❌ Wrong (will fail to find data)
cd head-nods-example/job-testanalysis2/code
python sample_size_analysis.py
```

---

## 📧 Contact

**Workshop instructor**: Job Schepens  
**Affiliation**: CRC 1252 "Prominence in Language", University of Cologne  
**Website**: https://sfb1252.uni-koeln.de/

**Community & Support**:
- [Workshop website](https://sfb1252.github.io/talks/)
- [GitHub repository](https://github.com/jobschepens/py-rdm)

---

## 📄 License

[MIT License](LICENSE) - Feel free to use and modify for educational purposes.

---

## 🙋 Get Started Now

```bash
git clone https://github.com/jobschepens/py-rdm.git
cd py-rdm
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
jupyter lab
```

Happy coding! 🐍📊
