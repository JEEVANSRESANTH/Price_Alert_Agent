AI Price Tracker
Cloud-Based Autonomous Price Monitoring System using Docker & Microservices
📌 Overview

The AI Price Tracker is a cloud-deployed full-stack application that automatically monitors product prices from e-commerce platforms. It uses an autonomous worker agent to continuously scrape prices, stores historical data, and provides real-time insights through an interactive dashboard.

The system is built using a microservices architecture, where the API, worker, and UI run independently using Docker and are deployed on Azure Container Apps.

URL link: https://price-tracker-ui.greenplant-9b018a93.southeastasia.azurecontainerapps.io/
✨ Features
📦 Track multiple products using URLs
🔄 Automated price scraping using worker agent
📊 Price history visualization (Chart.js)
🚨 Price drop detection
☁️ Cloud deployment on Azure
🐳 Docker-based microservices architecture
🏗️ Architecture
Frontend (Dashboard UI)
        │
        ▼
FastAPI Backend (REST APIs)
        │
        ▼
Azure CosmosDB (Database)
        ▲
        │
Worker Agent (Scraper + Automation)
⚙️ Tech Stack

Frontend

HTML, CSS, JavaScript
Chart.js

Backend

FastAPI (Python)

Database

Azure CosmosDB

Cloud & DevOps

Azure Container Apps
Azure Container Registry (ACR)
Docker
🔁 Workflow
User adds a product via dashboard
Backend stores product details
Worker agent periodically scrapes price
Data stored in CosmosDB
Dashboard displays latest price + history
🐳 Docker Setup (Local)
# Build API
docker build -f Dockerfile -t price-tracker-api .

# Build Worker
docker build -f Dockerfile.worker -t price-tracker-worker .

# Build UI
docker build -f Dockerfile.ui -t price-tracker-ui .
☁️ Azure Deployment
Deployed using Azure Container Apps
Images stored in Azure Container Registry
Services:
price-tracker-api
price-tracker-worker
price-tracker-ui
🚧 Challenges Faced
Handling dynamic web scraping
Debugging Azure container deployment
Managing environment variables
API integration with frontend
🔮 Future Improvements
AI-based price prediction
Multi-platform tracking (Amazon, Flipkart, etc.)
Smart alerts & recommendations
Enhanced UI (React dashboard)
🧠 What I Learned
Building scalable backend systems with FastAPI
Designing microservices architecture
Docker containerization & cloud deployment
Working with Azure services (CosmosDB, Container Apps)
🙌 Author

Jeevan Sresanth S
🚧 Challenges Faced
Handling dynamic web scraping
Debugging Azure container deployment
Managing environment variables
API integration with frontend
🔮 Future Improvements
AI-based price prediction
Multi-platform tracking (Amazon, Flipkart, etc.)
Smart alerts & recommendations
Enhanced UI (React dashboard)
🧠 What I Learned
Building scalable backend systems with FastAPI
Designing microservices architecture
Docker containerization & cloud deployment
Working with Azure services (CosmosDB, Container Apps)
🙌 Author

Jeevan Sresanth S
⭐ If you like this project

Give it a star ⭐ and feel free to fork!
