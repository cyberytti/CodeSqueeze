<div align="center">
  <img src="https://github.com/cyberytti/CodeSqueeze/blob/main/assets/CodeSqueeze_image.png" alt="CodeSqueeze Banner" width="1000" hight="1000/>
</div>

<div align="center">

### Ever tried to upload an entire codebase to a chatbot, and hit the context limit error? 😩

**CodeSqueeze is the answer!** It intelligently scans your project, bundles all your source code into a single, optimized text file, and gets it ready for any AI chatbot. Provide full project context to models like **Qwen**, **Claude**, or **GPT** with zero hassle.
</div>

-----

### ✨ Features

- **📦 All-in-One File**: Compresses your entire project into a single `.txt` file.
- **🧠 AI-Optimized**: Includes a directory tree and smart headers to give the AI maximum context.
- **📋 Auto-Clipboard**: Automatically copies the entire output to your clipboard with a single command (`-c`).
- **🔧 Fully Customizable**: Easily add extra file types (`-e`), ignore files/folders (`-i`), or add specific files (`-f`).
- **📊 Quick Stats**: Tells you the final file size and estimated token count.

-----

### 🚀 Getting Started

1. **Clone the repository** (or just save the `CodeSqueeze.py` file).
2. **Install dependencies**:
   ```bash
   pip install click pyfiglet pyperclip
   ```
3. **Run it!**

-----

### 💻 Usage

Point the script at your project directory. It's that simple.

#### **Basic Example**

This command will process `my-cool-app` and create `my-cool-app_codebase.txt`.

```bash
python CodeSqueeze.py ./my-cool-app
```

#### **Advanced Example**

This command will:

- Process the `my-cool-app` directory.
- Include `.md` and `.toml` files.
- Ignore the `dist` folder and `config.json`.
- Create a custom output file named `final_context.txt`.
- Copy the result directly to your clipboard! 📋

```bash
python CodeSqueeze.py ./my-cool-app -e md -e toml -i dist -i config.json -o final_context.txt -c
```
