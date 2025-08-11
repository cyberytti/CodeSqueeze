<div align="center">
  <img src="https://github.com/cyberytti/CodeSqueeze/blob/main/assets/CodeSqueeze_image.png" alt="CodeSqueeze Banner" width="1000" hight="1000/>
</div>

<div align="center">

### Ever tried to upload an entire codebase to a chatbot, and hit the context limit error? 😩

**CodeSqueeze is the answer!** It intelligently scans your project, bundles all your source code into a single, optimized text file, and gets it ready for any AI chatbot. Provide full project context to models like **Qwen**, **Claude**, or **GPT** with zero hassle.
</div>

-----
## How It Works??

Basically this tool combine this tree things in the output txt file.

1. *System prompt*  
2. *Project-tree structure*  
3. *Only the source (code) files*

By stripping away everything else—docs, binaries, configs, tests, etc.—it keeps the prompt within token limits while still giving the chatbot a complete, uncluttered view of the codebase.
-----

## Features

1. **Include Only Source Code Files**  
   If you want to include only the source code files, just provide the project path without any other instructions.  
   **Example:**  
   ```
   python3 CodeSqueeze.py "your project path"
   ```  
   This will give you three things: the list of files included in the output file, the output file size in MB, and the estimated token count for that file.

2. **Add Other File Types**  
   If you want to add other file types like txt, md, or anything else, use the "-e" parameter with the file type (without the dot), such as txt, md, yaml, etc.  
   **Example:**  
   ```
   python3 CodeSqueeze.py "your project path" -e "txt" -e "yaml" ...
   ```  
   This command will include all txt and yaml files in the output file.

3. **Exclude Specific Files from a Type**  
   If you want to include a certain type of file but exclude one or two specific files from that type, use the "-i" parameter.  
   **Example:**  
   ```
   python3 CodeSqueeze.py "your project path" -e "txt" -i "requirements.txt" 
   ```  
   This command will include all txt files except requirements.txt.

4. **Include Specific Files Without Their Type**  
   If you want to include just one or two specific files without adding their entire file type, use the "-f" parameter.  
   **Example:**  
   ```
   python3 CodeSqueeze.py "your project directory" -f "the selected file" -f "another selected file"...
   ```  
   This command will add those specific files to the output file.

5. **Copy Output as a Prompt to Clipboard**  
   This tool usually creates a txt file that you can upload to any chatbot and discuss with it, but if you want to copy the output txt file as a prompt straight to your clipboard, use the "-c" parameter.  
   **Example:**  
   ```
   python3 CodeSqueeze.py "your project path" -c 
   ```  
   This command will create a prompt and copy it to your clipboard automatically.

-----

### 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/cyberytti/CodeSqueeze.git
cd CodeSqueeze

# 2. Install requirements
pip install -r requirements.txt

# 3. Check the help
python3 CodeSqueeze.py --help
```
-----
