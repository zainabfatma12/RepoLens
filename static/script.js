async function analyzeRepo() {

    const input =
        document.getElementById("repoUrl");

    const button =
        document.getElementById("analyzeButton");

    const url =
        input.value.trim();


    if (!url) {

        alert(
            "Please enter a public GitHub repository URL."
        );

        return;
    }


    if (!url.includes("github.com/")) {

        alert(
            "Please enter a valid GitHub repository URL."
        );

        return;
    }


    button.disabled = true;

    button.innerHTML =
        "Analyzing <span>◌</span>";


    try {

        const response =
            await fetch("/analyze", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    url: url
                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to analyze repository."
            );

        }


        sessionStorage.setItem(
            "repoLensData",
            JSON.stringify(data)
        );


        window.location.href =
            "/dashboard.html";


    } catch (error) {

        alert(error.message);

        button.disabled = false;

        button.innerHTML =
            "Analyze <span>→</span>";

    }

}


function loadDashboard() {

    const stored =
        sessionStorage.getItem(
            "repoLensData"
        );


    if (!stored) {

        window.location.href = "/";

        return;
    }


    const data =
        JSON.parse(stored);


    const repo =
        data.repo;

    const analysis =
        data.analysis;


    /* REPOSITORY */

    document.getElementById(
        "repoName"
    ).textContent =
        repo.full_name;


    document.getElementById(
        "repoDescription"
    ).textContent =
        repo.description ||
        "No repository description provided.";


    document.getElementById(
        "githubLink"
    ).href =
        repo.url;


    document.getElementById(
        "repoLanguage"
    ).textContent =
        repo.language ||
        "Multiple technologies";


    /* SCORE */

    document.getElementById(
        "score"
    ).textContent =
        analysis.score;


    document.getElementById(
        "level"
    ).textContent =
        analysis.level;


    setTimeout(() => {

        document.getElementById(
            "scoreFill"
        ).style.width =
            analysis.score + "%";

    }, 150);


    /* STATS */

    document.getElementById(
        "stars"
    ).textContent =
        repo.stars;


    document.getElementById(
        "forks"
    ).textContent =
        repo.forks;


    document.getElementById(
        "issues"
    ).textContent =
        repo.issues;


    document.getElementById(
        "commits"
    ).textContent =
        analysis.commit_count;


    document.getElementById(
        "snapshotStars"
    ).textContent =
        repo.stars;


    document.getElementById(
        "snapshotForks"
    ).textContent =
        repo.forks;


    document.getElementById(
        "snapshotCommits"
    ).textContent =
        analysis.commit_count;


    /* FINDINGS */

    const findings =
        document.getElementById(
            "findings"
        );


    findings.innerHTML = "";


    if (
        analysis.findings.length === 0
    ) {

        findings.innerHTML = `
            <div class="signal-item">

                <div class="signal-icon good">
                    ✓
                </div>

                No positive signals detected yet.

            </div>
        `;

    } else {

        analysis.findings.forEach(
            item => {

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "signal-item";


                div.innerHTML = `

                    <div class="signal-icon good">
                        ✓
                    </div>

                    <div>
                        ${escapeHtml(item)}
                    </div>

                `;


                findings.appendChild(div);

            }
        );

    }


    /* WARNINGS */

    const warnings =
        document.getElementById(
            "warnings"
        );


    warnings.innerHTML = "";


    if (
        analysis.warnings.length === 0
    ) {

        warnings.innerHTML = `

            <div class="signal-item">

                <div class="signal-icon good">
                    ✓
                </div>

                No major improvement
                opportunities detected.

            </div>

        `;

    } else {

        analysis.warnings.forEach(
            item => {

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "signal-item";


                div.innerHTML = `

                    <div class="signal-icon warning">
                        !
                    </div>

                    <div>
                        ${escapeHtml(item)}
                    </div>

                `;


                warnings.appendChild(div);

            }
        );

    }


    /* README */

    document.getElementById(
        "readme"
    ).textContent =
        data.readme;

}


function copyReadme() {

    const readme =
        document.getElementById(
            "readme"
        ).textContent;


    navigator.clipboard.writeText(
        readme
    );


    const button =
        document.querySelector(
            ".copy-button"
        );


    button.textContent =
        "Copied ✓";


    setTimeout(() => {

        button.textContent =
            "Copy README";

    }, 1800);

}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;

}


if (
    window.location.pathname.includes(
        "dashboard.html"
    )
) {

    loadDashboard();

}