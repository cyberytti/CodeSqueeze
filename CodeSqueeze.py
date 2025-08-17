# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "pyfiglet",
#     "pyperclip",
# ]
# ///


try:
    import os
    import re
    import sys
    from pathlib import Path
    from typing import Union, Optional
    import click
    import shutil
    import pyfiglet
    import pyperclip


    def print_banner():
        """Enhanced banner with modern aesthetics and better visual appeal"""
        try:
            
            # Generate ASCII art with a more stylish font
            ascii_art = pyfiglet.figlet_format("CodeSqueeze", font="slant")
            subtitle = pyfiglet.figlet_format(".py", font="digital")
            
            # Get terminal dimensions
            term_width = shutil.get_terminal_size((80, 24)).columns
            
            # Enhanced color palette - gradient-like effect
            GRADIENT_COLORS = [
                "\033[1;38;5;81m",   # Bright cyan
                "\033[1;38;5;75m",   # Light blue  
                "\033[1;38;5;69m",   # Blue
                "\033[1;38;5;63m",   # Purple-blue
            ]
            
            ACCENT_COLOR = "\033[1;38;5;226m"    # Bright yellow
            SUBTITLE_COLOR = "\033[1;38;5;208m"  # Orange
            FOOTER_COLOR = "\033[1;38;5;244m"    # Gray
            BORDER_COLOR = "\033[1;38;5;39m"     # Bright blue
            RESET = "\033[0m"
            
            # Unicode box drawing characters for better borders
            TOP_BORDER = "╔" + "═" * (term_width - 2) + "╗"
            BOTTOM_BORDER = "╚" + "═" * (term_width - 2) + "╝"
            SIDE_BORDER = "║"
            
            # Print top border
            print(f"\n{BORDER_COLOR}{TOP_BORDER}{RESET}")
            
            # Add some spacing
            print(f"{BORDER_COLOR}{SIDE_BORDER}{' ' * (term_width - 2)}{SIDE_BORDER}{RESET}")
            
            # Process main ASCII art with gradient effect
            main_lines = ascii_art.splitlines()
            visible_main = [line for line in main_lines if line.strip()]
            
            for i, line in enumerate(visible_main):
                # Apply gradient colors
                color = GRADIENT_COLORS[i % len(GRADIENT_COLORS)]
                
                # Center the line and add borders
                if len(line) > term_width - 4:
                    line = line[:term_width - 4]
                
                centered_line = line.center(term_width - 4)
                print(f"{BORDER_COLOR}{SIDE_BORDER}{color}{centered_line}{RESET}{BORDER_COLOR}{SIDE_BORDER}{RESET}")
            
            # Process subtitle (.py)
            subtitle_lines = subtitle.splitlines()
            visible_subtitle = [line for line in subtitle_lines if line.strip()]
            
            for line in visible_subtitle:
                if len(line) > term_width - 4:
                    line = line[:term_width - 4]
                
                centered_line = line.center(term_width - 4)
                print(f"{BORDER_COLOR}{SIDE_BORDER}{SUBTITLE_COLOR}{centered_line}{RESET}{BORDER_COLOR}{SIDE_BORDER}{RESET}")
            
            # Add decorative separator
            separator = "◆" * min(40, term_width - 10)
            separator_centered = separator.center(term_width - 4)
            print(f"{BORDER_COLOR}{SIDE_BORDER}{ACCENT_COLOR}{separator_centered}{RESET}{BORDER_COLOR}{SIDE_BORDER}{RESET}")
            
            # Add tagline
            taglines = [
                "🚀 Transform Your Codebase into AI-Ready Format 🚀",
                "💡 Perfect for Qwen, Claude or any other chatbot 💡"
            ]
            
            for tagline in taglines:
                if len(tagline) > term_width - 4:
                    tagline = tagline[:term_width - 4]
                
                centered_tagline = tagline.center(term_width - 4)
                print(f"{BORDER_COLOR}{SIDE_BORDER}{ACCENT_COLOR}{centered_tagline}{RESET}{BORDER_COLOR}{SIDE_BORDER}{RESET}")
            
            # Add some spacing before footer
            print(f"{BORDER_COLOR}{SIDE_BORDER}{' ' * (term_width - 2)}{SIDE_BORDER}{RESET}")
            
            # Enhanced footer with better styling
            footer_info = [
                ("👨‍💻", "Created by: cyberytti"),
                ("🔗", "GitHub: github.com/cyberytti"),
                ("📸", "Instagram: @trueliving"),
                ("⭐", "Star this project if you find it useful!")
            ]
            
            for icon, text in footer_info:
                full_text = f"{icon} {text}"
                if len(full_text) > term_width - 6:
                    full_text = full_text[:term_width - 6] + "..."
                
                # Right align footer items
                padding = (term_width - 4) - len(full_text)
                if padding > 0:
                    formatted_line = " " * padding + full_text
                else:
                    formatted_line = full_text
                    
                print(f"{BORDER_COLOR}{SIDE_BORDER}{FOOTER_COLOR}{formatted_line}{RESET}{BORDER_COLOR}{SIDE_BORDER}{RESET}")
            
            # Final spacing and bottom border
            print(f"{BORDER_COLOR}{SIDE_BORDER}{' ' * (term_width - 2)}{SIDE_BORDER}{RESET}")
            print(f"{BORDER_COLOR}{BOTTOM_BORDER}{RESET}")
            
            # Add a final accent line
            accent_line = "═" * term_width
            print(f"{ACCENT_COLOR}{accent_line}{RESET}\n")
            
        except Exception as error:
            # Fallback to simple banner if anything goes wrong
            print("╔" + "═" * 50 + "╗")
            print("║" + " " * 15 + "CodeSqueeze.py" + " " * 15 + "║")
            print("║" + " " * 10 + "Codebase → AI Format" + " " * 10 + "║")
            print("╚" + "═" * 50 + "╝")
            print(f"Error in banner: {error}\n")
    print_banner()
except Exception as error:
    print(error)

class Get_file_paths:
    def __init__(self, given_dir, extra_extensions=None, ignored_files=None, ignored_directories=None, add_files=None, output_file=None):
        self.base_dir = os.path.abspath(given_dir)
        self.prompt = f"""You are an expert coding agent with context-aware understanding of software projects. While you're designed to analyze entire codebases, *only a subset of files and the project structure* has been provided due to context window constraints.  

*Your responsibilities:*  
1. *Accurately execute tasks* (e.g., debugging, documentation, feature implementation) *using ONLY the files currently in context*.  
2. *Explicitly request missing files* when needed:  
   - State exactly which file(s) you require (using full paths from the provided project structure)  
   - Justify why the file is essential for the task  
   - Never assume file existence beyond the provided context  
3. *Prioritize solutions within scope*: If a task can be completed with available files, do so without requesting additions.  

*Critical rules:*  
- ❌ *NEVER* invent code from unprovided files  
- ❌ *NEVER* guess file contents/structure  
- ✅ *ALWAYS* reference the project structure when requesting files  
- ✅ *ALWAYS* clarify ambiguities before proceeding

provided project : {self.base_dir}"""
        

        if output_file:
            self.final_file_path = os.path.abspath(output_file)
        else:
            self.final_file_path = f"{self.base_dir}_codebase.txt"
        self.ignored_files = ignored_files or []
        self.add_files = add_files or []
        self.ignored_directories = ignored_directories or []
        
        # Default list of supported file extensions
        self.extensions_list = [
            "py",
            "cpp",
            "java",
            "js",
            "ts",
            "c",
            "h",
            "cs",
            "go",
            "rs",
            "rb",
            "php",
            "swift",
            "kt",
            "scala",
            "pl",
            "lua",
            "r",
            "dart",
            "html",
            "htm",
            "css",
            "jsx",
            "scss",
            "tsx",
            "vue",
            "svelte",
            "sh",
            "bash",
            "ps1",
            "bat",
            "cmd",
             "hs",    
            "jl",   
            "sql",   
            "m",    
            "ex",   
            "exs",   
            "vb",    
            "fs",   
            "groovy",
            "erl",  
        ]
        
        if extra_extensions:
            self.extensions_list.extend(ext.lstrip(".").lower() for ext in extra_extensions)

    def _tree(
            self,
            root: Union[str, "os.PathLike[str]"],
            *,
            max_depth: Optional[int] = None,
            show_hidden: bool = False,
            _prefix: str = "",
            _depth: int = 0
    ) -> str:
        """Return an ASCII tree of the directory rooted at *root*."""
        root = Path(root)
        if not root.is_dir():
            return f"{root} is not a directory\n"
        if max_depth is not None and _depth > max_depth:
            return ""
        entries = sorted(
            (p for p in root.iterdir() if show_hidden or not p.name.startswith(".")),
            key=lambda p: (p.is_file(), p.name.lower())
        )
        lines: list[str] = []
        for idx, path in enumerate(entries):
            connector = "└── " if idx == len(entries) - 1 else "├── "
            lines.append(f"{_prefix}{connector}{path.name}")
            if path.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                subtree = self._tree(
                    path,
                    max_depth=max_depth,
                    show_hidden=show_hidden,
                    _prefix=_prefix + extension,
                    _depth=_depth + 1,
                )
                lines.append(subtree.rstrip())
        return "\n".join(lines) + ("\n" if lines else "")

    def get_all_file_paths(self):
        file_paths = []
        for root, directories, files in os.walk(self.base_dir):
            # Skip ignored directories
            if self.ignored_directories:
                directories[:] = [d for d in directories if not any(ignored_dir in os.path.join(root, d) for ignored_dir in self.ignored_directories)]
            
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths

    def _remove_newlines(self,file_path: str) -> str:
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")

        try:
            # Read the entire file
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Remove newline characters
            cleaned_text = text.replace("\n", "")

            # Write the cleaned content back to the same file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_text)

            return file_path

        except FileNotFoundError as exc:
            print(f"Error: '{file_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        except PermissionError as exc:
            print(f"Error: Permission denied accessing '{file_path}'.", file=sys.stderr)
            sys.exit(1)
        except OSError as exc:
            print(f"OS error while processing '{file_path}': {exc}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Unexpected error: {exc}", file=sys.stderr)
            sys.exit(1)

    def _replace_multiple_tabs(self,file_path: str) -> str:
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            cleaned_content = re.sub(r"\t{2,}", "\t", content)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_content)

            return file_path

        except FileNotFoundError as exc:
            print(f"Error: '{file_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        except PermissionError as exc:
            print(f"Error: Permission denied accessing '{file_path}'.", file=sys.stderr)
            sys.exit(1)
        except OSError as exc:
            print(f"OS error while processing '{file_path}': {exc}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Unexpected error: {exc}", file=sys.stderr)
            sys.exit(1)

    def purify_files(self, file_paths):
        final_purified_file_paths = []
        for path in file_paths:
            if '.' in path and path.split('.')[-1].lower() in self.extensions_list:
                final_purified_file_paths.append(path)
        return final_purified_file_paths
    
    def _remove_folders(self, file_paths, directories_to_remove):
        """Remove files that are in specified directories"""
        if not directories_to_remove:
            return file_paths
        
        return [
            path for path in file_paths
            if not any(os.path.normpath(dir_to_remove) in os.path.normpath(path) for dir_to_remove in directories_to_remove)
        ]

    def _get_file_size_kb(self, file_path):
        """Get file size in KB using os.stat()"""
        try:
            stat_info = os.stat(file_path)
            size_bytes = stat_info.st_size
            size_kb = size_bytes / 1024
            return size_kb
        except FileNotFoundError:
            return 0
    
    def _create_final_file(self):
        all_files = self.get_all_file_paths()
        source_files = self.purify_files(all_files)
        
        # Add extra files if specified
        if self.add_files:
            for r in self.add_files:
                abs_path = os.path.abspath(r)
                if abs_path not in source_files:
                    source_files.append(abs_path)
      
        # Process ignored files
        if self.ignored_files:
            # Convert to absolute paths for reliable comparison
            ignored_abs = [os.path.abspath(f) for f in self.ignored_files]
            source_files = [f for f in source_files if os.path.abspath(f) not in ignored_abs]
        
        # Remove files from ignored directories (additional safety check)
        if self.ignored_directories:
            source_files = self._remove_folders(source_files, self.ignored_directories)
        
        # Create header with styling
        header = f"""{self.prompt}
PROJECT STRUCTURE:
{'-'*40}
{self._tree(self.base_dir)}
{'='*80}
FILE CONTENTS:
{'='*80}
"""
        with open(self.final_file_path, "w", encoding="utf-8") as outfile:
            outfile.write(header)
        
        processed_count = 0
        for file_path in source_files:
            relative_path = os.path.relpath(file_path, self.base_dir)
            size = self._get_file_size_kb(file_path)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                    file_content = infile.read()
            except Exception as e:
                click.echo(click.style(f"⚠️  Could not read {relative_path}: {e}", fg='yellow'))
                continue
            
            # Append file content with separator
            separator = f"\n{'-'*60}\n"
            with open(self.final_file_path, "a", encoding="utf-8") as outfile:
                outfile.write(
                    f"{separator}"
                    f"📁 File: {relative_path}\n"
                    f"{'-'*60}\n"
                    f"## File content: \n{file_content}\n"
                )
            
            processed_count += 1
            # Progress indicator
            if processed_count % 10 == 0:
                click.echo(f"📦 Processed {processed_count}/{len(source_files)} files...")
        
        return (
            self._replace_multiple_tabs(self._remove_newlines(self.final_file_path)), 
            source_files, 
            self._get_file_size_kb(self.final_file_path)
        )
    
    def main(self):
        return self._create_final_file()

@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    epilog="""
Examples:
  # Basic usage (creates myproject_codebase.txt)
  $ CodeSqueeze.py myproject
  # Include Markdown files and ignore tests directory
  $ CodeSqueeze.py myproject -e md -e yaml --ignore_directory tests
  # Ignore specific files and directories
  $ CodeSqueeze.py myproject -i config.py --ignore_directory __pycache__ --ignore_directory .git
  # Add custom file and specify output
  $ CodeSqueeze.py myproject -f docs/notes.md -o all_code.txt
""",
)
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    metavar="PROJECT_DIR",
)
@click.option(
    "-e",
    "--extra-extensions",
    multiple=True,
    metavar="EXT",
    help="Add file extensions to include (without dot). "
         "Example: -e md -e yaml",
)
@click.option(
    "-i",
    "--ignore",
    multiple=True,
    metavar="PATH",
    help="Exclude files (relative to PROJECT_DIR). "
         "Example: --ignore tests.txt --ignore docs/notes.md",
)
@click.option(
    "-id",
    "--ignore_directory",
    multiple=True,
    metavar="PATH",
    help="Exclude directories (relative to PROJECT_DIR). "
         "Example: --ignore_directory tests --ignore_directory __pycache__",
)
@click.option(
    "-f",
    "--add-files",
    multiple=True,
    metavar="PATH",
    help="Include additional files (bypassing extension filters). "
         "Example: -f notes.txt -f design/README.md",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    metavar="FILE",
    help="Output filename (default: PROJECT_DIR_codebase.txt)",
)
@click.option(
    '-c',
    '--copy',
    is_flag=True,
    help='Copy the generated codebase file to your clipboard as a prompt.'
)
def cli(directory, extra_extensions, ignore, ignore_directory, add_files, output, copy):
    """
    Creates a single text file containing your entire codebase.
    
    PROJECT_DIR: Project directory to process
    
    Perfect for sharing with AI assistants (ChatGPT, Claude, etc.) or 
    teammates - includes all source files in a clean, organized format.
    By default includes common programming files (Python, JS, Java, etc.).
    Use options to customize what gets included.
    """
    
    # Convert directory to absolute path
    base_dir = os.path.abspath(directory)
    
    # Process ignored files (convert to absolute paths relative to base_dir)
    processed_ignored = []
    for f in ignore:
        # If absolute path, use as-is, otherwise make relative to base_dir
        if os.path.isabs(f):
            processed_ignored.append(f)
        else:
            processed_ignored.append(os.path.abspath(os.path.join(base_dir, f)))
    
    # Process add_files
    processed_add_files = []
    for f in add_files:
        # If absolute path, use as-is, otherwise make relative to base_dir
        if os.path.isabs(f):
            processed_add_files.append(f)
        else:
            processed_add_files.append(os.path.abspath(os.path.join(base_dir, f)))
    
    # Process ignored directories
    processed_ignored_dirs = []
    for d in ignore_directory:
        if os.path.isabs(d):
            processed_ignored_dirs.append(d)
        else:
            processed_ignored_dirs.append(os.path.join(base_dir, d))
    
    # Create the file collector
    collector = Get_file_paths(
        given_dir=directory,
        extra_extensions=extra_extensions,
        ignored_files=processed_ignored,
        ignored_directories=processed_ignored_dirs,
        add_files=processed_add_files,
        output_file=output
    )
    
    # Generate the codebase file
    final_file, processed_files, total_size_kb = collector.main()
    
    # Print results
    click.echo("\n" + click.style("✓ Successfully processed files:", fg='green', bold=True))
    for f in processed_files:
        rel_path = os.path.relpath(f, base_dir)
        click.echo(f"  • {rel_path}")
    
    click.echo("\n" + click.style("📄 Output file:", fg='cyan', bold=True))
    click.echo(f"  {final_file}")
    
    total_size_mb = total_size_kb / 1024
    click.echo(click.style(f"  Size: {total_size_mb:.2f} MB", fg='blue'))
    
    # Estimate tokens (simplified: 4 chars ≈ 1 token)
    try:
        with open(final_file, 'r', encoding='utf-8') as f:
            content = f.read()
        token_estimate = len(content) // 4
        click.echo(click.style(f"  Estimated tokens: {token_estimate:,}", fg='magenta'))
    except Exception as e:
        click.echo(click.style(f"  Token estimation failed: {e}", fg='yellow'))
    
    if copy:
        with open(final_file, "r") as file:
            text = file.read()
        text = text + "\n\nQuery: [provide your query]"
        pyperclip.copy(text)
        click.echo(click.style(f"\n✓ Successfully Copied as prompt!\n", fg='cyan'))

if __name__ == '__main__':
    cli()