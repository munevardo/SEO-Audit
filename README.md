# 🚀 Automated SEO Audit Pipeline (RICOPA)

**Turn raw crawling data into actionable business intelligence.**

This repository contains a Python-based automation tool designed to streamline technical SEO audits.
Instead of spending hours cleaning Excel sheets, this script ingests raw CSV exports (from tools like Screaming Frog), processes them, and generates a prioritized roadmap for developers and content strategists.

## ⚡ Key Capabilities
* **Automated Data ETL:** Ingests multiple CSV reports (4xx errors, Core Web Vitals, H1/Meta issues, etc.) from Google Drive.
* **Workload Estimation:** unique algorithm that calculates the **estimated hours** required to fix specific errors based on volume.
* **Role Assignment:** Automatically categorizes tasks by responsible team member (e.g., `Frontend Dev` vs. `Content Strategist`).
* **RICOPA Methodology:** organizes findings into **R**astreo (Crawl), **I**ndexability, **C**ontent, **O**n-Page, **P**opularity, and **A**uthority.

## 🛠️ Tech Stack
* **Python (Pandas/NumPy):** For data manipulation and cleanup.
* **Google Colab/Drive API:** For cloud-based file handling.
* **Excel Integration:** Exports a multi-sheet, client-ready `.xlsx` master file.
