



# 🚀 Blue/Green Deployment Project (Stage 3)

This project demonstrates a **Blue/Green deployment strategy** using **Docker**, **Docker Compose**, and **Nginx** as a reverse proxy for zero-downtime deployments.

---

## 🧩 Project Overview

In this setup:
- **Two app environments** (`Blue` and `Green`) run simultaneously.
- **Nginx** dynamically routes traffic to the active version based on the `.env` variable `ACTIVE_POOL`.
- **Blue** and **Green** apps are identified by their Docker images and release IDs.
- You can easily switch between app versions by changing one line in your `.env` file.

---

## 📁 Repository Structure

bluegreen-deploy/ ├─ docker-compose.yml ├─ .env ├─ nginx.conf.template ├─ README.md └─ (optional) DECISION.md

---

## ⚙️ Requirements

Before you begin, ensure you have:
- **Docker** installed  
- **Docker Compose** installed

---

## 🧰 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd bluegreen-deploy

2️⃣ Create and configure your environment file

Copy the example file and update the variables as needed:

cp .env.example .env

Sample .env:

BLUE_IMAGE=yimikaade/wonderful:devops-stage-two
GREEN_IMAGE=yimikaade/wonderful:devops-stage-two
RELEASE_ID_BLUE=v1.0.0
RELEASE_ID_GREEN=v2.0.0
ACTIVE_POOL=green

> 🔹 To switch versions, simply change ACTIVE_POOL to blue or green, then run:

docker compose up -d




---

🧱 Start the Services

Run the following command to start all containers:

docker compose up -d


---

🧪 Test the Deployment

Check Nginx (main proxy)

curl -I localhost:8080

Check Blue App

curl -I localhost:8081/version

Check Green App

curl -I localhost:8082/version


---

🔁 Switch Between Blue and Green

To change which app receives traffic:

1. Open your .env file.


2. Change the line:

ACTIVE_POOL=green

to

ACTIVE_POOL=blue


3. Rebuild Nginx with the new environment:

docker compose up -d



> ✅ Nginx will now direct requests to the newly activated version without downtime.




---

💥 Optional: Chaos Testing

You can simulate app errors to test resilience:

curl -X POST http://localhost:8081/chaos/start?mode=error
curl -X POST http://localhost:8082/chaos/stop


---

🧾 Notes

envsubst is used to inject .env variables into nginx.conf.template.

/version shows each app’s release ID and pool name.

This setup ensures zero-downtime deployment when switching environments.



---

🧠 Author

Gloria [Your Last Name]
HNG Devops Intern 13– Stage 3 Project
“Building with confidence and excellence.”



