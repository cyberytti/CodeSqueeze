# 🚀 CodeSqueeze - A CLI tool to seamlessly upload any codebase to your preferred chatbot.

![CodeSqueeze Banner](https://github.com/cyberytti/CodeSqueeze/blob/main/assets/CodeSqueeze_image.png)

## 🤔 Have you ever tried to upload an entire codebase to a chatbot, and hit the context limit error? 😩
**CodeSqueeze is the answer!** It intelligently scans your project, bundles all your source code into a single, optimized text file, and gets it ready for any AI chatbot. 🌟 Provide full project context to models like Qwen, Claude, or GPT with zero hassle. ✨

---

## 🌐 How It Works?

CodeSqueeze combines these three essential elements in the output text file:

✅ **System prompt**  
📁 **Project tree structure**  
💻 **Only the source (code) files**

By stripping away everything else—docs, binaries, configs, tests, etc.—it keeps the prompt within token limits while still giving the chatbot a complete, uncluttered view of the codebase. 🧹

---

## 💎 Features

1. ### 📁 Include Only Source Code Files
If you want to include only the source code files, just provide the project path without any other instructions.

```bash
python3 CodeSqueeze.py "your project path"
```

This will give you three things:  
📊 the list of files included in the output file  
📏 the output file size in MB  
🔢 and the estimated token count for that file.

---

2. ### 📄 Add Other File Types
If you want to add other file types like txt, md, or anything else, use the `-e` parameter with the file type (without the dot), such as txt, md, yaml, etc.

```bash
python3 CodeSqueeze.py "your project path" -e "txt" -e "yaml" ...
```

This command will include all txt and yaml files in the output file. 📂

---

3. ### 🚫 Exclude Specific Files from a Type
If you want to include a certain type of file but exclude one or two specific files from that type, use the `-i` parameter.

```bash
python3 CodeSqueeze.py "your project path" -e "txt" -i "requirements.txt"
```

This command will include all txt files except requirements.txt. 🙅‍♂️

---

4. ### 🎯 Include Specific Files Without Their Type
If you want to include just one or two specific files without adding their entire file type, use the `-f` parameter.

```bash
python3 CodeSqueeze.py "your project directory" -f "the selected file" -f "another selected file"...
```

This command will add those specific files to the output file. 🎯

---

5. ### 📋 Copy Output as a Prompt to Clipboard
This tool usually creates a txt file that you can upload to any chatbot and discuss with it, but if you want to copy the output txt file as a prompt straight to your clipboard, use the `-c` parameter.

```bash
python3 CodeSqueeze.py "your project path" -c
```

This command will create a prompt and copy it to your clipboard automatically. 🖱️➡️📋

---

## 🎥 Demo

[![CodeSqueeze Demo](https://img.youtube.com/vi/placeholder/0.jpg)](https://www.youtube.com/watch?v=placeholder)

*Click the image above to watch a quick 2-minute demo of CodeSqueeze in action!*

**What you'll see in the demo:**
- 🖥️ Setting up CodeSqueeze for the first time
- 🧩 Processing a real-world codebase
- 📊 Token count optimization in action
- 🤖 Using the output with popular AI chatbots
- ⚡ Time-saving benefits for developers

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/cyberytti/CodeSqueeze.git
cd CodeSqueeze
```

### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 3️⃣ Check the Help
```bash
python3 CodeSqueeze.py --help
```

---

## 🌈 Why Developers Love CodeSqueeze

- **Efficiency** ⏱️ - No more manual code selection
- **Precision** 🎯 - Only relevant files included
- **Compatibility** 🔌 - Works with all major AI models
- **Simplicity** ✨ - One command does it all
- **Flexibility** 🧭 - Customize exactly what gets included

---

> 💡 **Pro Tip**: Combine multiple flags for ultimate control!  
> `python3 CodeSqueeze.py "project" -e "md" -i "README.md" -f "special_config.json" -c`

---

⭐ **Star us on GitHub if CodeSqueeze helps you work smarter with AI!** ⭐
