# 🔎 RepoLens

### GitHub Repository Intelligence & Portfolio Readiness Analyzer

RepoLens is a lightweight developer tool that analyzes a public GitHub repository and generates a **Repository Readiness Score** based on documentation, project structure, open-source practices, and repository activity.

Instead of manually reviewing a repository, developers can paste a GitHub URL and instantly receive actionable recommendations.

---

## ✨ Features

- 🔍 Public GitHub repository analysis
- 📊 Repository Readiness Score out of 100
- 📚 README/documentation analysis
- 🗂️ Project structure analysis
- 📦 Dependency/configuration detection
- 🔓 Open-source readiness checks
- 📈 Repository activity analysis
- ⭐ GitHub stars and forks
- ⚠️ Actionable improvement recommendations
- 💻 Clean responsive dashboard
- 🚀 No GitHub login required

---

## 💡 Problem

Developers often spend significant time preparing GitHub repositories for:

- internships
- placements
- portfolios
- open-source contributions
- hackathons
- job applications

However, there is no simple way to quickly understand whether a repository is well documented, structured and ready to showcase.

---

## 💡 Solution

RepoLens turns repository metadata into an easy-to-understand health report.

### Input

A public GitHub repository URL.

### Processing

RepoLens analyzes:

1. Documentation
2. Project structure
3. Open-source readiness
4. Repository activity

### Output

The user receives:

- overall score
- repository statistics
- strengths
- improvement recommendations

---

## 🧠 Scoring Model

| Category | Weight |
|---|---:|
| Documentation | 30 |
| Project Structure | 25 |
| Open Source | 20 |
| Activity | 25 |
| **Total** | **100** |

The score is converted into a simple readiness level:

- **80–100:** Excellent
- **65–79:** Portfolio Ready
- **45–64:** Needs Improvement
- **0–44:** Early Stage

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask

### API

- GitHub REST API

### Deployment

- Gunicorn compatible

---

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │      User           │
                │ GitHub Repository   │
                │       URL           │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      RepoLens       │
                │      Frontend       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     Flask API       │
                │     /analyze        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    GitHub REST API  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Repository Analysis │
                │ Documentation       │
                │ Structure           │
                │ Open Source         │
                │ Activity            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Readiness Report   │
                │ Score + Findings    │
                │ Recommendations     │
                └─────────────────────┘