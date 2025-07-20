# WEB SCRAPPING 
**Empowering Data-Driven Decisions with Seamless Web Insights**

## 🌐 Overview
This project is a lightweight Python web application built with Flask, designed to extract and serve structured insights from web sources. Featuring a modular setup and deployment-ready configurations for AWS Elastic Beanstalk, it's ideal for rapid development and deployment of web scraping or data extraction tools.

---

## 📚 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

---

## ✨ Features
- 🔥 Flask-based web interface for processing and displaying results
- 📄 HTML scraping using BeautifulSoup
- 🌐 Cross-Origin Resource Sharing (CORS) support
- 🚀 Production-ready with Gunicorn and Elastic Beanstalk support
- 📁 Templated frontend using Jinja2 and custom CSS

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AryanGupta5084/Python.git
   cd Python
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the application locally:

```bash
python application.py
```

By default, the app runs on `http://localhost:5000`. You can access the homepage and begin interacting with the web interface.

---

## ⚙️ Configuration

- **Elastic Beanstalk**: Configured via `.elasticbeanstalk/config.yml` and `.ebextensions/python.config` for deployment.
- **CORS**: Enabled via `Flask-Cors`.
- **Gunicorn**: Used for production WSGI server.

---

## 📦 Dependencies

From `requirements.txt`:
```
Flask==1.1.2
Flask-Cors==3.0.9
gunicorn==20.0.4
requests==2.24.0
beautifulsoup4==4.9.1
bs4==0.0.1
pymongo
Jinja2, click, certifi, idna, urllib3, six, chardet, MarkupSafe, itsdangerous, Werkzeug
```

## 🛠 Troubleshooting

- Ensure all dependencies are installed correctly.
- When deploying on Elastic Beanstalk, double-check `.ebextensions` and Python version compatibility.
- For CORS issues, review `Flask-Cors` middleware configuration in `application.py`.

---

## 👥 Contributors

- **Aryan Gupta** – Author & Maintainer

---
