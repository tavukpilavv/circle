# 🎯 Circle Event

🚀 **Live Platform:** https://www.circleevent.app/#/

A production-ready web platform that aggregates university club events into a single ecosystem.
Currently **actively used by 170+ registered users and 10+ student clubs**, enabling students to discover, join, and engage with campus events across universities.

---

## 🌍 Deployment

🔗 **Frontend (Production):** https://www.circleevent.app/#/
🔗 **Backend API:** https://circle-9srg.onrender.com

---

## 🧪 Preview (Staging)

🔗 https://new2-git-project-circles-projects-4e72fdc3.vercel.app

> Used for testing before production releases.

---

## 📊 Project Impact

* 👥 **170+ active users**
* 🏫 **10+ student clubs onboarded**
* 📅 Real event participation system
* 💬 Active feedback & interaction between students
* 🔄 Continuous deployment & iteration

---

## ✨ Features

* 🔐 **Role-Based Access Control (RBAC)**
  Super Admin & Club Admin role separation with strict permission control.

* 📝 **Club Application System**
  Structured onboarding workflow for new student communities.

* 🎯 **Secure Event Management**
  Clubs can only manage their own events (backend enforced isolation).

* 💬 **Event Registration & Feedback**
  Users can join events and share experiences afterward.

* 🌐 **Multi-University Platform**
  Discover events across different campuses in one place.

---

## 🧱 Architecture

```text id="w82md1"
Frontend (Vue.js)
        ↓
REST API (Flask)
        ↓
Database
```

---

## 🛠️ Tech Stack

| Layer      | Technology                 |
| ---------- | -------------------------- |
| Frontend   | Vue.js 3 (Composition API) |
| Backend    | Flask (Python)             |
| Deployment | Vercel & Render            |
| API        | RESTful                    |

---

## 🔐 Security & QA

* ✔️ Role-based authorization (RBAC)
* ✔️ Input validation (client & server)
* ✔️ XSS & Injection protection
* ✔️ Secure authentication & session handling
* ✔️ HTTPS enforced

📊 **Testing:**
15+ functional & security test cases executed

---

## ⚙️ Installation

### Clone repositories

```bash id="4t1z8k"
git clone <frontend-repo-link>
git clone <backend-repo-link>
```

### Frontend

```bash id="a2k91p"
cd frontend
npm install
npm run dev
```

### Backend

```bash id="92lxks"
cd backend
pip install -r requirements.txt
flask run
```

---

## 🔑 Environment Variables

```env id="zz81kd"
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
JWT_SECRET=your_jwt_secret
```

---

## 👥 Team

* **Ezgi İşgüzar** — Full Stack Developer & QA Engineer
* **Hacer Büşra Köse** — Backend Developer
* **Malak Ali Nagi Nosary** — Frontend Developer & Database Engineer

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Note

Circle Event is an actively growing platform, continuously evolving with real user feedback and expanding student communities.

