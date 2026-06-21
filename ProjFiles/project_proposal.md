# Project Proposal: Report Screen Integration

This document outlines the requirements, estimates, and questions needed to integrate the new "Report Screen" into the client's existing software application.

## 1. Questions for the Client

Before beginning the actual integration, you need clear technical answers from the client to avoid roadblocks. Ask them the following:

### A. Existing Software Architecture
*   **What programming language and UI framework is the current application built in?** (e.g., Python/PyQt, C#/WPF, VB.NET, LabVIEW). *If it's not Python, we need to know if the Report Screen should be a separate standalone .exe that their app opens, or natively integrated into their existing source code.*
*   **Do we have access to the existing source code?** If so, what version control system is used (Git, SVN)?

### B. Database Connection
*   **What type of database is running in production?** (Microsoft SQL Server, MySQL, SQLite, Oracle?)
*   **Where is the database located?** (Is it on the local machine terminal, or a central factory server?)
*   **Can we get Read-Only credentials (username/password/IP) to the production or staging database?**

### C. Deployment & Environment
*   **What Operating System covers the factory floor PCs?** (Windows 10, Windows 7, Linux?)
*   **Is there internet access on these machines for installing packages, or do we need to provide a fully bundled offline executable?**

---

## 2. Time Estimates (Working 3 Hours / Day)

Integrating a new screen into an *existing* application takes longer than building a demo from scratch because you have to read their code, match their styling programmatically, and handle live production data safely.

| Scenario | Total Hours | Days (at 3 hrs/day) | Weeks |
| :--- | :--- | :--- | :--- |
| **Minimum Time (Best Case)**<br>*(The app is Python, DB is simple SQLite, code is clean)* | 15 Hours | 5 Days | 1 Week |
| **Average Time (Expected)**<br>*(The app is standard C#/Python, DB is SQL Server, requires network setup)* | 30 Hours | 10 Days | 2 Weeks |
| **Above Average Time (Complex)**<br>*(Legacy codebase, complex SQL joins required, custom PDF exports needed)* | 45 Hours | 15 Days | 3 Weeks |
| **Maximum Time (Worst Case)**<br>*(Different programming language required, strict factory IT firewalls, no documentation)*| 60+ Hours | 20+ Days | 4+ Weeks |

---

## 3. Financial Quotes (Freelance / Contract Rates)

Pricing depends heavily on the complexity of their existing system. Below is a realistic breakdown tailored for the Chennai / Indian domestic market for freelance software integration. These rates are competitive and designed to be fair without causing "sticker shock" to local manufacturing or tech clients.

| Quote Tier | Estimated Amount (INR) | What this signifies to the client |
| :--- | :--- | :--- |
| **Minimum Quote** | ₹12,000 - ₹15,000 | "I will integrate it quickly, assuming everything is perfectly documented and already in Python/C#." |
| **Average Quote** | ₹25,000 - ₹35,000 | "Standard integration rate. This includes time for testing with your live database and minor UI revisions." |
| **Above Average Quote** | ₹45,000 - ₹60,000 | "Includes adapting the code to your native language (if not Python), handling basic network setup, and factory-floor testing." |
| **Maximum Quote** | ₹75,000+ | "Turnkey enterprise solution. I will learn your legacy system, write the database wrappers from scratch, and provide a short period of post-launch support." |

---

## 4. Tips for the Demo Presentation in the Local Market

*   **Be clear this is a mockup:** Remind the client this demo runs on a *local offline file*. Real integration will require connecting to their live SQL server.
*   **Focus on the Value:** Emphasize how much time this automated reporting screen will save their factory operators compared to manual checks.
*   **Ask for the tech stack gracefully:** Instead of demanding info, say, *"To give you a precise timeline and fixed-cost quote, arrange a brief 10-minute call with your IT/Dev team to confirm your database version and frontend framework. This helps me give you the best possible price."*
