# 🚀 How to Host Your Streamlit App for Free — Step by Step

> **You will be done in about 20–30 minutes. No experience needed. Just follow each step one by one.**

---

## 🧭 What We Are Going to Do (Big Picture)

Think of it like this:

1. **GitHub** = A free online "locker" where you store your code files
2. **Streamlit Cloud** = A free service that reads your code from that locker and runs it as a live website
3. **You** = Just need to put your files in the locker and press "Deploy"!

---

## ✅ PHASE 1 — Create a GitHub Account (Skip if you already have one)

### Step 1 — Go to GitHub

- Open your browser (Chrome, Edge, etc.)
- Go to: **https://github.com**
- Click the green **"Sign up"** button

### Step 2 — Fill in your details

- Enter your **email address**
- Create a **password** (write it down somewhere safe!)
- Choose a **username** (example: `pavan-machine-demo` — no spaces allowed)
- Click **"Continue"** and verify your email

### Step 3 — Confirm your email

- Go to your email inbox
- You will see an email from GitHub
- Click the confirmation link inside it
- You are now logged in to GitHub ✅

---

## ✅ PHASE 2 — Install Git on Your Computer

Git is a small program that helps upload files to GitHub. You only install it once.

### Step 4 — Download Git

- Go to: **https://git-scm.com/download/win**
- The download will start automatically
- It will download a file like `Git-2.xx.x-64-bit.exe`

### Step 5 — Install Git

- Double-click the downloaded file
- Keep clicking **"Next"** on every screen (default settings are fine)
- At the end, click **"Finish"**

### Step 6 — Check Git is installed

- Press the **Windows key** on your keyboard
- Type **"cmd"** and press **Enter** (this opens the Command Prompt — a black window)
- In the black window, type exactly this and press Enter:
  ```
  git --version
  ```
- You should see something like: `git version 2.45.0`
- If you see that, Git is installed ✅

---

## ✅ PHASE 3 — Tell Git Who You Are (One-time setup)

### Step 7 — Set your name and email in Git

In the same black Command Prompt window, type these two commands **one by one**, pressing Enter after each:

```
git config --global user.name "Your Name"
```
*(Replace `Your Name` with your actual name, keep the quotes)*

```
git config --global user.email "your@email.com"
```
*(Replace with the email you used for GitHub, keep the quotes)*

---

## ✅ PHASE 4 — Create a GitHub Repository (Your Online Locker)

### Step 8 — Create a new repository on GitHub

- Go to **https://github.com** and log in
- Click the **"+"** button at the top-right corner
- Click **"New repository"**

### Step 9 — Fill in the repository details

- **Repository name:** Type `welch-plug-demo` (no spaces — use hyphens)
- **Description:** Type `Welch Plug Pressing Machine Datalogging Demo`
- Select **"Public"** (so anyone with the link can view your demo)
- **Do NOT** check "Add a README file" (leave it unchecked)
- Click the green **"Create repository"** button

### Step 10 — Copy the repository link

- After creating, you will see a page with some commands
- Look for a link that looks like:
  `https://github.com/YourUsername/welch-plug-demo.git`
- **Copy this link** (you'll need it in the next phase)

---

## ✅ PHASE 5 — Upload Your Project Files to GitHub

### Step 11 — Open Command Prompt IN your project folder

- Open **File Explorer** on your computer
- Go to this folder: `C:\Users\DELL\Desktop\Projs\UI_to_Sql_Project`
- In the address bar at the top of File Explorer, **click on it** (the path will become highlighted)
- Type `cmd` and press **Enter**
- A black Command Prompt window will open, **already inside your project folder** ✅

### Step 12 — Initialize Git in your project folder

Type this command and press Enter:
```
git init
```
You should see: `Initialized empty Git repository in ...`

### Step 13 — Connect your folder to GitHub

Type this command (replace `YourUsername` with your actual GitHub username):
```
git remote add origin https://github.com/YourUsername/welch-plug-demo.git
```

### Step 14 — Add all your project files

Type this command and press Enter:
```
git add .
```
*(The dot means "add everything". There is a space between `add` and `.`)*

### Step 15 — Save a snapshot (called a "commit")

Type this command and press Enter:
```
git commit -m "Initial upload of Welch Plug demo"
```
You will see a list of files being saved.

### Step 16 — Upload (push) to GitHub

Type this command and press Enter:
```
git push -u origin main
```

> ⚠️ **It may ask you to log in:**
> - A browser window will pop up asking you to sign in to GitHub
> - Sign in with your GitHub username and password
> - Come back to the command prompt — it will continue automatically

You should see something like:
```
Branch 'main' set up to track remote branch 'main' from 'origin'.
```
This means your files are now on GitHub ✅

### Step 17 — Verify your files are on GitHub

- Go to `https://github.com/YourUsername/welch-plug-demo`
- You should see all your files listed there:
  - `streamlit_app.py`
  - `machine_data.db`
  - `requirements.txt`
  - `setup_db.py`
  - etc.

---

## ✅ PHASE 6 — Deploy on Streamlit Cloud (The Final Step!)

### Step 18 — Go to Streamlit Cloud

- Open browser and go to: **https://share.streamlit.io**
- Click **"Sign in"**
- Click **"Continue with GitHub"**
- It will ask you to authorize Streamlit — click **"Authorize streamlit"**
- You are now inside Streamlit Cloud ✅

### Step 19 — Create a new app

- Click the **"Create app"** button (blue button)
- Select **"I have an existing app"** / **"Deploy a public app from GitHub"**

### Step 20 — Fill in the deployment details

You will see a form. Fill it in like this:

| Field | What to enter |
|-------|--------------|
| **Repository** | `YourUsername/welch-plug-demo` |
| **Branch** | `main` |
| **Main file path** | `streamlit_app.py` |
| **App URL** | Choose a name like `welch-plug-demo` |

### Step 21 — Click Deploy!

- Click the **"Deploy!"** button
- You will see a log screen with messages scrolling — this is normal!
- Wait about **2–3 minutes**
- When it's done, you'll see your app running live! 🎉

### Step 22 — Get your shareable link

- Your app will be available at a URL like:
  `https://welch-plug-demo.streamlit.app`
- **Copy this link** and share it with anyone!
- They can open it on their phone, laptop, or any device — no installation needed!

---

## 🔄 How to Update the App Later (if you make changes)

If you change something in `streamlit_app.py` later, just open Command Prompt in your project folder and run these 3 commands:

```
git add .
git commit -m "Updated the app"
git push
```

Streamlit Cloud will **automatically update** within a minute! ✅

---

## ❓ Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| `git push` asks for username/password every time | Use GitHub's browser login popup that appears — it only asks once |
| App shows an error on Streamlit Cloud | Check that `machine_data.db` file was uploaded to GitHub |
| "Repository not found" error | Make sure you copied the exact repository link in Step 13 |
| App stuck on "Your app is in the oven" | Wait 3–5 minutes, sometimes it's slow the first time |

---

## 📋 Quick Summary Checklist

- [ ] Created GitHub account
- [ ] Installed Git
- [ ] Configured Git with name and email
- [ ] Created GitHub repository called `welch-plug-demo`
- [ ] Opened cmd in project folder
- [ ] Ran `git init`
- [ ] Ran `git remote add origin ...`
- [ ] Ran `git add .`
- [ ] Ran `git commit -m "..."`
- [ ] Ran `git push -u origin main`
- [ ] Verified files on GitHub website
- [ ] Signed in to share.streamlit.io with GitHub
- [ ] Deployed the app
- [ ] Got the live link 🎉

