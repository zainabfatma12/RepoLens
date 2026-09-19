from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "RepoLens-HackDevengers"
}


def parse_repo_url(repo_url):
    """Extract owner and repository name from GitHub URL."""

    if not repo_url:
        raise ValueError("Please enter a GitHub repository URL.")

    repo_url = repo_url.strip().rstrip("/")

    if "github.com/" not in repo_url:
        raise ValueError("Please enter a valid GitHub repository URL.")

    path = repo_url.split("github.com/", 1)[1]

    parts = path.split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1].replace(".git", "")

    if not owner or not repo:
        raise ValueError("Invalid GitHub repository URL.")

    return owner, repo


def github_get(endpoint):
    """Safe GitHub API request."""

    response = requests.get(
        f"{GITHUB_API}{endpoint}",
        headers=HEADERS,
        timeout=10
    )

    return response


def get_repository(owner, repo):
    response = github_get(f"/repos/{owner}/{repo}")

    if response.status_code == 404:
        raise ValueError(
            "Repository not found. Make sure it is public and the URL is correct."
        )

    if response.status_code != 200:
        raise ValueError("GitHub API request failed.")

    return response.json()


def get_contents(owner, repo):
    response = github_get(f"/repos/{owner}/{repo}/contents")

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            return data

    return []


def get_readme(owner, repo):
    response = github_get(f"/repos/{owner}/{repo}/readme")

    if response.status_code == 200:
        return response.json()

    return None


def get_commits(owner, repo):
    response = github_get(
        f"/repos/{owner}/{repo}/commits?per_page=10"
    )

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            return data

    return []


def has_license(owner, repo):
    response = github_get(f"/repos/{owner}/{repo}/license")

    return response.status_code == 200


def analyze_repository(repo, contents, readme, commits, license_exists):

    score = 0
    findings = []
    warnings = []

    filenames = [
        item.get("name", "").lower()
        for item in contents
    ]

    # ==========================================
    # DOCUMENTATION — 30
    # ==========================================

    if readme:

        score += 10
        findings.append("README file exists.")

        try:
            readme_response = requests.get(
                readme.get("download_url"),
                timeout=10
            )

            readme_text = readme_response.text.lower()

            if len(readme_text) > 300:
                score += 5
                findings.append(
                    "README contains substantial documentation."
                )

            if "install" in readme_text or "setup" in readme_text:
                score += 5
                findings.append(
                    "Installation or setup instructions detected."
                )
            else:
                warnings.append(
                    "Add clear installation instructions to your README."
                )

            if "feature" in readme_text:
                score += 5
                findings.append(
                    "Features section detected."
                )
            else:
                warnings.append(
                    "Add a clear Features section."
                )

            if "usage" in readme_text or "how to use" in readme_text:
                score += 5
                findings.append(
                    "Usage instructions detected."
                )
            else:
                warnings.append(
                    "Add a Usage section."
                )

        except Exception:
            pass

    else:
        warnings.append(
            "README file is missing."
        )

    # ==========================================
    # PROJECT STRUCTURE — 25
    # ==========================================

    source_extensions = [
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".html",
        ".css",
        ".go",
        ".rs"
    ]

    has_source = any(
        any(filename.endswith(ext) for ext in source_extensions)
        for filename in filenames
    )

    if has_source:
        score += 10
        findings.append(
            "Source code files detected."
        )
    else:
        warnings.append(
            "No recognizable source files detected."
        )

    package_files = [
        "requirements.txt",
        "package.json",
        "pom.xml",
        "cargo.toml",
        "go.mod"
    ]

    if any(
        file in filenames
        for file in package_files
    ):
        score += 5
        findings.append(
            "Dependency or configuration file detected."
        )
    else:
        warnings.append(
            "Consider adding a dependency/configuration file."
        )

    if ".gitignore" in filenames:
        score += 5
        findings.append(
            ".gitignore file detected."
        )
    else:
        warnings.append(
            "Add a .gitignore file."
        )

    if len(contents) >= 3:
        score += 5
        findings.append(
            "Repository has a structured file layout."
        )

    # ==========================================
    # OPEN SOURCE — 20
    # ==========================================

    if license_exists:
        score += 10
        findings.append(
            "Open-source license detected."
        )
    else:
        warnings.append(
            "Consider adding an open-source license."
        )

    if "contributing.md" in filenames:
        score += 5
        findings.append(
            "Contribution guidelines detected."
        )
    else:
        warnings.append(
            "Consider adding CONTRIBUTING.md."
        )

    if "code_of_conduct.md" in filenames:
        score += 5
        findings.append(
            "Code of Conduct detected."
        )
    else:
        warnings.append(
            "Consider adding a Code of Conduct."
        )

    # ==========================================
    # ACTIVITY — 25
    # ==========================================

    commit_count = len(commits)

    if commit_count >= 5:
        score += 10
        findings.append(
            "Recent commit activity detected."
        )

    elif commit_count >= 1:
        score += 5
        findings.append(
            "Repository has commit activity."
        )

    else:
        warnings.append(
            "No recent commits detected."
        )

    if repo.get("forks_count", 0) > 0:
        score += 5
        findings.append(
            "Repository has forks."
        )
    else:
        warnings.append(
            "No forks yet."
        )

    if repo.get("stargazers_count", 0) > 0:
        score += 5
        findings.append(
            "Repository has GitHub stars."
        )
    else:
        warnings.append(
            "No GitHub stars yet."
        )

    if repo.get("open_issues_count", 0) > 0:
        score += 5
        findings.append(
            "GitHub issue activity detected."
        )
    else:
        warnings.append(
            "Consider using GitHub Issues for project tracking."
        )

    score = min(score, 100)

    if score >= 80:
        level = "Excellent"

    elif score >= 65:
        level = "Portfolio Ready"

    elif score >= 45:
        level = "Needs Improvement"

    else:
        level = "Early Stage"

    return {
        "score": score,
        "level": level,
        "findings": findings,
        "warnings": warnings,
        "commit_count": commit_count
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received."
            }), 400

        repo_url = data.get("repo_url", "").strip()

        owner, repo_name = parse_repo_url(repo_url)

        repo = get_repository(owner, repo_name)

        contents = get_contents(owner, repo_name)

        readme = get_readme(owner, repo_name)

        commits = get_commits(owner, repo_name)

        license_exists = has_license(owner, repo_name)

        analysis = analyze_repository(
            repo,
            contents,
            readme,
            commits,
            license_exists
        )

        result = {
            "success": True,

            "repository": {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "html_url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "issues": repo.get("open_issues_count", 0),
                "watchers": repo.get("watchers_count", 0),
                "updated_at": repo.get("updated_at")
            },

            "analysis": analysis
        }

        return jsonify(result)

    except ValueError as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except requests.exceptions.Timeout:

        return jsonify({
            "success": False,
            "error": "GitHub request timed out. Please try again."
        }), 504

    except requests.exceptions.RequestException:

        return jsonify({
            "success": False,
            "error": "Could not connect to GitHub."
        }), 502

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error": "Something went wrong while analyzing the repository."
        }), 500


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )