# Github CI/CD

GitHub Actions is a **CI/CD (Continuous Integration and Continuous Deployment) and automation platform** built into GitHub.

It allows you to automate workflows directly from your GitHub repository. Essentially, you can make GitHub do tasks automatically whenever certain events happen in your repository, such as code pushes, pull requests, issue creation, or scheduled times.

## Key Features:

1. **Automated Workflows** – Run scripts or commands automatically based on events.
2. **CI/CD Pipelines** – Test, build, and deploy code automatically.
3. **Custom Actions** – Create reusable steps or use prebuilt actions from the GitHub Marketplace.
4. **Matrix Builds** – Test your code across multiple operating systems, versions, or configurations.
5. **Secrets Management** – Store sensitive credentials securely for use in workflows.
6. **Integration with GitHub Ecosystem** – Directly tied to pull requests, issues, and GitHub Packages.

## How it Works:

* A workflow is defined in a **YAML file** in `.github/workflows/` folder.
* Go to your Github repo, there is a tab **Actions** where all workflows are recognized.
* Each workflow has:

  * **Trigger (event)**: e.g., push, pull_request, schedule.
  * **Jobs**: Tasks to run, often on virtual environments (Linux, Windows, macOS).
  * **Steps**: Individual commands or actions within a job.

## Common Use Cases:

1. **Continuous Integration (CI)**

   * Run automated tests whenever code is pushed.
   * Example: Linting, unit tests, code coverage checks.

2. **Continuous Deployment (CD)**

   * Automatically deploy applications to cloud providers, servers, or containers.
   * Example: Deploy a website to AWS S3 or Heroku when code merges to `main`.

3. **Automated Builds**

   * Compile code or build Docker images automatically.

4. **Code Quality and Security Checks**

   * Run linters, static analysis, and vulnerability scanners.

5. **Automation of Routine Tasks**

   * Label issues, merge pull requests, generate release notes, or send notifications.

6. **Scheduled Jobs**

   * Run backups, database migrations, or cleanups on a schedule.

---

💡 **Analogy:** Think of GitHub Actions as a robot assistant for your repository. Every time something happens (code push, PR merge, etc.), you tell the robot what tasks to perform automatically.


## Practical workflow

This workflow forces to apply linting by `ruff` everytime a PR is made to the `main` branch.

```yml
name: Lint

on:
  pull_request:
    branches: [main]
    paths:
      - "**.py"

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - run: pip install ruff
      - run: ruff check .
```

## Detail explanation

### 1. **`on`**

```yaml
on:
  pull_request:
    branches: [main]
    paths:
      - "**.py"
```

* **Purpose:** Defines **when the workflow should run**.
* Can respond to events like `push`, `pull_request`, `schedule`, `workflow_dispatch` (manual trigger), etc.
* In this example:

  * Triggers on a **pull request** targeting the `main` branch.
  * Only triggers if **Python files (`*.py`)** were changed.
* Think of it as the **event listener** for your workflow.

---

### 2. **`jobs` and `runs-on`**

```yaml
jobs:
  ruff:
    runs-on: ubuntu-latest
```

* **`jobs`**: Defines one or more tasks (jobs) that run as part of the workflow.
* Each job runs in a **virtual environment**.
* **`runs-on`**: Specifies the type of machine for the job.

  * Examples: `ubuntu-latest`, `windows-latest`, `macos-latest`.
* Each job runs **independently**, unless you define dependencies (`needs:`).

---

### 3. **`steps`**

* **Steps** are the individual commands executed in a job, in order.
* Each step can either **run a shell command** or **use an action**.

---

a) **`uses`**

```yaml
- uses: actions/checkout@v6
```

* Refers to a **prebuilt GitHub Action** from the Marketplace or GitHub itself.
* Syntax: `owner/repo@version`
* Examples in your workflow:

  1. `actions/checkout@v6` → Checks out your repository so the runner has the code.
  2. `actions/setup-python@v6` → Sets up a specific Python version.

✅ **Tip:** `uses` is like saying “run this prepackaged tool”.

---

b) **`with`**

```yaml
- uses: actions/setup-python@v6
  with:
    python-version: '3.13'
```

* Provides **input parameters to the action used**.
* Example: For `setup-python`, `python-version` tells the action which Python version to install.
* Think of it as **configuring the action**.

---

c) **`run`**

```yaml
- run: pip install ruff
- run: ruff check .
```

* Runs **arbitrary shell commands** directly in the runner.
* Can be used to install packages, run tests, build code, deploy, etc.
* Multiple `run` steps execute **sequentially** in the same job environment.

---

### Quick Analogy:

* **`on`** → “When should I do this?”
* **`jobs` / `runs-on`** → “Where should I do this?”
* **`steps`** → “What exact things should I do?”

  * **`uses`** → “Use this prebuilt tool”
  * **`with`** → “Configure that tool with these options”
  * **`run`** → “Run this custom command myself”

### Workflow diagram

```
[PULL REQUEST to main branch with Python changes]  ←── "on: pull_request"
                     │
                     ▼
          ┌───────────────────────┐
          │ Workflow: Lint        │
          └───────────────────────┘
                     │
                     ▼
          ┌───────────────────────┐
          │ Job: ruff             │
          │ runs-on: ubuntu-latest│
          └───────────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │ Step 1: Checkout Code       │
       │ uses: actions/checkout@v6   │
       └─────────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────────┐
       │ Step 2: Setup Python          │
       │ uses: actions/setup-python@v6 │
       │ with: python-version: 3.13    │
       └───────────────────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │ Step 3: Install Ruff        │
       │ run: pip install ruff       │
       └─────────────────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │ Step 4: Run Linter          │
       │ run: ruff check .           │
       └─────────────────────────────┘
                     │
                     ▼
           ┌────────────────────┐
           │ PASS or FAIL       │
           │ Workflow Status    │
           └────────────────────┘
```