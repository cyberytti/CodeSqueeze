# 🤖 CodeSqueeze

> **Upload your entire codebase to ChatGPT, Claude, or any AI - without hitting token limits!**

![CodeSqueeze Banner](https://github.com/cyberytti/CodeSqueeze/blob/main/assets/CodeSqueeze_image.png)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![UV](https://img.shields.io/badge/UV-Ready-green.svg)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Finally! Share your entire project with AI assistants in one click** 🚀

</div>

---

## 😤 **Tired of This?**

❌ **"Your message is too long"**  
❌ **Copying files one by one to ChatGPT**  
❌ **AI missing context because you can't share the full codebase**  
❌ **Explaining your project structure over and over**  
❌ **Token limit errors killing your productivity**  

## ✅ **CodeSqueeze Fixes It All!**

✨ **One command** → **Entire codebase ready for any AI**  
📋 **Auto-copies to clipboard** → **Paste directly into ChatGPT/Claude**  
🎯 **Perfect context every time** → **Better AI responses**  

---

## 🎯 **Perfect For When You Want To:**

| **🔥 Use Case** | **Why You Need CodeSqueeze** |
|-----------------|-------------------------------|
| **🐛 Debug Complex Issues** | Give AI your full codebase context for accurate solutions |
| **📚 Code Reviews** | Share entire project with teammates or AI for comprehensive feedback |
| **🚀 Refactoring Help** | Let AI see all interconnected files to suggest better architecture |
| **📖 Documentation** | AI can write better docs when it sees your complete project |
| **🎓 Learning & Teaching** | Share codebases with mentors, students, or AI tutors |
| **🔄 Migration Projects** | Get help converting entire codebases to new frameworks/languages |
| **⚡ Quick Onboarding** | New team members understand your project structure instantly |

---

## 🚀 **Get Started in 30 Seconds**

### **Install on macOS and Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/cyberytti/CodeSqueeze/main/install.sh | sudo bash
```

### **Check help**
```bash
CodeSqueeze --help
```

**That's it!** 🎉 **Now you are ready to squeeze your code bases**

---

## 💡 **Real-World Examples**

### **🐛 "My React app has a weird bug"**
```bash
CodeSqueeze my-react-app --copy
```
→ Paste in ChatGPT: *"Here's my full React app. There's a weird rendering bug on the dashboard page. Can you help me find what's causing it?"*

### **📚 "Please review my Python project"**
```bash
CodeSqueeze my-python-project --ignore tests --copy
```
→ Paste in Claude: *"Can you review this codebase and suggest improvements for performance and code quality?"*

### **🎓 "Explain this codebase to me"**
```bash
CodeSqueeze legacy-project --copy
```
→ Paste in AI: *"I inherited this codebase. Can you explain how it works and create documentation for the main components?"*

### **🔄 "Help me migrate to Next.js"**
```bash
CodeSqueeze old-react-app -e json -e md --copy
```
→ Paste in AI: *"Can you help me migrate this React app to Next.js 14? What's the best approach?"*

---

## 🎮 **Common Commands You'll Love**

```bash
# 📋 Most used: Copy entire project to clipboard
CodeSqueeze my-project --copy

# 📝 Include config files and documentation  
CodeSqueeze my-project -e json -e yaml -e md --copy

# 🚫 Skip test files and build folders
CodeSqueeze my-project --ignore tests --ignore build --copy

# 🎯 Include only specific important files
CodeSqueeze my-project -f README.md -f package.json --copy

# 💾 Save to file instead of clipboard
CodeSqueeze my-project -o my-project-for-ai.txt
```

---

## 🌟 **Works With All Your Favorite AI Tools**

<div align="center">

| **🤖 AI Assistant** | **✅ Status** | **💡 Best For** |
|-------------------|--------------|-----------------|
| **ChatGPT** | Perfect | Code reviews, debugging, refactoring |
| **Claude** | Perfect | Complex analysis, documentation |
| **Qwen** | Perfect | Open-source AI development |
| **Any AI** | Works! | Whatever you're using |

</div>

---

## 🎯 **What Languages Work?**

**All of them!** 🌍 Python, JavaScript, Java, C++, Rust, Go, TypeScript, PHP, Ruby, Swift, Kotlin... **If you code in it, CodeSqueeze handles it.**

---

## ❓ **FAQ**

### **"Will this work with my huge codebase?"**
Yes! CodeSqueeze is smart about what to include. It skips build files, dependencies, and other clutter - keeping only what AI needs to help you.

### **"What if I hit token limits anyway?"**
CodeSqueeze shows you the estimated token count. You can exclude folders (`--ignore node_modules`) or file types to fit any limit.

### **"Can I use this for proprietary code?"**
Absolutely! Everything stays on your machine. You control what gets shared and with whom.

### **"Do I need to install Python dependencies?"**
Nope! UV handles everything automatically. Just run the command.

---


<div align="center">

## ⭐ **Love CodeSqueeze?**

**Star this repo** if it made your life easier!

**Share it** with fellow developers who are tired of token limits!

---

*Built by developers who were frustrated with copying code files one by one* 😅

**Stop fighting token limits. Start building better software with AI.** 🚀

</div>
