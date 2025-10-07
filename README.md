# 🔐 DevSecOps Flask Project – Insecure App

This intentionally vulnerable **Flask application** is created for **educational purposes** in DevSecOps training.  
It contains multiple security flaws in both the application code and the Dockerfile.  

⚠️ **Disclaimer:** Do **not** deploy this app in production. It is meant only for learning and practicing security scanning.

---

## 🚀 Quick Deployment

### Automated Deployment
```bash
git clone https://github.com/talhazafarjutt/devsecops-flask-project.git
cd devsecops-flask-project
chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh
```

### Access URLs
- **🔒 Flask App**: https://dev.devsecopsassignment.work.gd
- **📊 Grafana**: https://dev.devsecopsassignment.work.gd/grafana/
- **📈 Prometheus**: https://dev.devsecopsassignment.work.gd/prometheus/

---

## 🎯 Learning Goals

- Identify and fix **common security flaws** in application code and Docker images  
- Practice **SAST** (Static Application Security Testing) using SonarQube  
- Run **container security scans** with Trivy  
- Learn **secrets scanning** with Gitleaks  
- Build and run a **CI/CD pipeline with GitHub Actions**  
- Deploy the Flask app through CI/CD pipeline  
- Set up **application monitoring** with Prometheus & Grafana  
- Understand **secure coding & containerization best practices**

---

## 🚩 What's Wrong (On Purpose)

- Hardcoded credentials in the Flask app  
- No input validation  
- Debug route that exposes system commands  
- Weak session key  
- Dockerfile uses **unpinned base image**  
- Container runs as **root user**  
- Missing healthcheck and cleanup steps  

---

## 🧪 Tools You'll Use

- **SonarQube** – Static code analysis (SAST)  
- **Trivy** – Docker image scanning  
- **Gitleaks** – Secret detection  
- **Docker** – Build and run the app  
- **Git & GitHub** – Version control  
- **GitHub Actions** – CI/CD automation  
- **Prometheus & Grafana** – Monitoring and visualization  

---

## 📝 Student Tasks – What You Need to Do

Follow these steps to complete the project.  
(Remember: this app is intentionally insecure, your job is to improve and secure it.)

---

### 1. Repository Setup
- Fork this repository into your own GitHub account  
- Clone your fork locally  
- Explore the project files (Flask app + Dockerfile)  

```bash
# Step 1: Fork this Repo
# (click 'Fork' on GitHub and create your own copy)

# Step 2: Clone Your Fork
git clone https://github.com/<your-username>/devsecops-flask-project.git
cd devsecops-flask-project

```

---

### 2. Run Locally
- Build the Docker image of the app  
- Run the container and verify it works on [http://localhost:5000](http://localhost:5000)  
```bash
# Step 1: Build the Docker Image
docker build -t devsecops-flask-project .

# Step 2: Run the App
docker run -p 5000:5000 devsecops-flask-project
```
---

### 3. Analyze Security Issues
- Identify insecure practices in the Flask app  
- Identify insecure practices in the Dockerfile  
- Write down your observations before fixing  

---

### 4. Setup CI/CD with GitHub Actions
- Create a GitHub Actions workflow (`.github/workflows/ci-cd.yml`)  
- Add the following stages in the pipeline:
  - **Checkout**: Pull code from your repo  
  - **Static Code Scan**: Run SonarQube  
  - **Secrets Scan**: Run Gitleaks  
  - **Build**: Build Docker image  
  - **Image Scan**: Run Trivy on the image  
  - **Push**: Push Docker image to a registry (GitHub Container Registry or DockerHub) (Optional)
  - **Deploy**: Run the container in your target environment  

---

### 5. Fix Security Issues (Optional)
- Apply fixes to Flask code (credentials, validation, debug routes, session key, etc.)  
- Apply fixes to Dockerfile (pin image version, non-root user, healthcheck, cleanup)  
- Commit and push changes  
- Re-run pipeline and verify scans show improvements  

---

### 6. Monitoring Setup
- Deploy **Prometheus** in a container  
- Deploy **Grafana** in a container  
- Connect Prometheus as a data source in Grafana  
- Create two dashboards: one generic monitoring dashboard for system metrics and one Docker monitoring dashboard for container metrics on the server where the application is deployed

---

### 7. Final Deliverables
- Share the repository URL of a working Flask app deployed via CI/CD  
- Passing scans in CI/CD (SonarQube, Trivy, Gitleaks)  
- Running Prometheus + Grafana monitoring stack  
- Documentation (google doc) of:
  - Insecure issues found  
  - Fixes applied  
  - Screenshots of scans & dashboards  

---

## 🔧 Development

### Local Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### CI/CD Pipeline
The project includes a comprehensive CI/CD pipeline with:
- Code quality analysis (SonarQube)
- Security scanning (Bandit, Safety, Trivy)
- Container security scanning
- Automated testing

---

## 📊 Monitoring

The project includes a complete monitoring stack:
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Node Exporter**: System metrics
- **Cadvisor**: Container metrics

---

## 🔒 Security

This project demonstrates:
- Common security vulnerabilities
- Security scanning tools
- Secure coding practices
- Container security
- HTTPS/SSL configuration

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.