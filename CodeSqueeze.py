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
    from typing import Union, Optional ,List , Tuple
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


    class CodebaseProcessor:
        """
        A comprehensive tool for processing and analyzing codebases.
        
        This class scans a directory structure, filters files based on extensions and ignore patterns,
        and creates a consolidated text file containing the project structure and file contents.
        The output is formatted for use with AI coding agents.
        """
        
        # Default directories to ignore during processing
        DEFAULT_IGNORED_DIRECTORIES = [
            "node_modules",      # Node.js dependencies - contains source files
            "vendor",            # Go/PHP dependencies - contains source files  
            "packages",          # Some package managers - contains source files
            "deps",              # Elixir/Erlang dependencies - contains source files
            "lib",               # Ruby gems/dependencies - contains source files
            "gems",              # Ruby gems - contains source files
            "bundle",            # Bundler gems - contains source files
            "Pods",              # iOS CocoaPods - contains source files
            "Carthage",          # iOS Carthage - contains source files
            "gradle",            # Gradle wrapper - contains source files
            "mvnw",              # Maven wrapper - contains source files
            ".gradle",           # Gradle cache - contains source files
            ".m2",               # Maven local repository - contains source files
            "target/dependency", # Maven dependencies - contains source files
        ]
        
        # Default supported file extensions for code files
        DEFAULT_SUPPORTED_EXTENSIONS = [
            "py", "cpp", "java", "js", "ts", "c", "h", "cs", "go", "rs", "rb", "php",
            "swift", "kt", "scala", "pl", "lua", "r", "dart", "html", "htm", "css",
            "jsx", "scss", "tsx", "vue", "svelte", "sh", "bash", "ps1", "bat", "cmd",
            "hs", "jl", "sql", "m", "ex", "exs", "vb", "fs", "groovy", "erl",
        ]
        
        def __init__(self, 
                    source_directory: str,
                    additional_extensions: Optional[List[str]] = None,
                    ignored_files: Optional[List[str]] = None,
                    ignored_directories: Optional[List[str]] = None,
                    additional_files: Optional[List[str]] = None,
                    output_file: Optional[str] = None):
            """
            Initialize the CodebaseProcessor.
            
            Args:
                source_directory: Path to the directory to process
                additional_extensions: Extra file extensions to include (without dots)
                ignored_files: Specific files to exclude from processing
                ignored_directories: Additional directories to ignore
                additional_files: Specific files to include regardless of extension
                output_file: Path for the output file (defaults to {source_directory}_codebase.txt)
            """
            self.source_directory = os.path.abspath(source_directory)
            self.output_file_path = self._determine_output_path(output_file)
            
            # Initialize file and directory filters
            self.ignored_files = ignored_files or []
            self.additional_files = additional_files or []
            self.ignored_directories = self._setup_ignored_directories(ignored_directories)
            self.supported_extensions = self._setup_supported_extensions(additional_extensions)
            
            # Generate the AI agent prompt
            self.ai_agent_prompt = self._generate_ai_agent_prompt()
        
        def _determine_output_path(self, output_file: Optional[str]) -> str:
            """Determine the output file path."""
            if output_file:
                return os.path.abspath(output_file)
            return f"{self.source_directory}_codebase.txt"
        
        def _setup_ignored_directories(self, additional_ignored: Optional[List[str]]) -> List[str]:
            """Setup the list of directories to ignore."""
            ignored_dirs = self.DEFAULT_IGNORED_DIRECTORIES.copy()
            if additional_ignored:
                ignored_dirs.extend(additional_ignored)
            return ignored_dirs
        
        def _setup_supported_extensions(self, additional_extensions: Optional[List[str]]) -> List[str]:
            """Setup the list of supported file extensions."""
            extensions = self.DEFAULT_SUPPORTED_EXTENSIONS.copy()
            if additional_extensions:
                # Clean and add additional extensions
                clean_extensions = [ext.lstrip(".").lower() for ext in additional_extensions]
                extensions.extend(clean_extensions)
            return extensions
        
        def _generate_ai_agent_prompt(self) -> str:
            """Generate the prompt text for AI agents."""
            return f"""You are an expert coding agent with context-aware understanding of software projects. While you're designed to analyze entire codebases, *only a subset of files and the project structure* has been provided due to context window constraints.  

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

    Due to context limits, the code is compressed by removing newlines and tabs when sent. However, when responding, debugging, or providing code, always use normal, readable formatting that can be copied and pasted directly.

    provided project : {self.source_directory}"""

        def generate_directory_tree(self,
                                root: Union[str, "os.PathLike[str]"],
                                max_depth: Optional[int] = None,
                                show_hidden: bool = False,
                                ignored_dirs: Optional[List[str]] = None,
                                _prefix: str = "",
                                _depth: int = 0) -> str:
            """
            Generate an ASCII tree representation of the directory structure.
            
            Args:
                root: Root directory to start from
                max_depth: Maximum depth to traverse
                show_hidden: Whether to show hidden files/directories
                ignored_dirs: List of directories to ignore
                _prefix: Internal parameter for recursion
                _depth: Internal parameter for recursion
                
            Returns:
                ASCII tree representation as a string
            """
            root = Path(root)
            if not root.is_dir():
                return f"{root} is not a directory\n"
            
            if max_depth is not None and _depth > max_depth:
                return ""
            
            # Use class ignored directories if none provided
            if ignored_dirs is None:
                ignored_dirs = self.ignored_directories
            
            # Convert ignored directories to absolute paths for comparison
            ignored_paths = set()
            if ignored_dirs:
                for ignored_dir in ignored_dirs:
                    ignored_path = Path(ignored_dir)
                    if not ignored_path.is_absolute():
                        ignored_path = root / ignored_path
                    ignored_paths.add(ignored_path.resolve())
            
            # Get sorted entries, excluding ignored directories
            entries = sorted(
                (p for p in root.iterdir() 
                if (show_hidden or not p.name.startswith(".")) 
                and p.resolve() not in ignored_paths),
                key=lambda p: (p.is_file(), p.name.lower())
            )
            
            lines: List[str] = []
            for idx, path in enumerate(entries):
                connector = "└── " if idx == len(entries) - 1 else "├── "
                lines.append(f"{_prefix}{connector}{path.name}")
                
                if path.is_dir():
                    extension = "    " if idx == len(entries) - 1 else "│   "
                    subtree = self.generate_directory_tree(
                        path,
                        max_depth=max_depth,
                        show_hidden=show_hidden,
                        ignored_dirs=ignored_dirs,
                        _prefix=_prefix + extension,
                        _depth=_depth + 1,
                    )
                    lines.append(subtree.rstrip())
            
            return "\n".join(lines) + ("\n" if lines else "")

        def discover_all_files(self) -> List[str]:
            """
            Recursively collect every file under `source_directory`
            while skipping any directory whose *name* matches an entry
            in `ignored_directories` (either default or user-supplied).
            """
            file_paths = []

            # Build a *flat* set of directory basenames to ignore
            ignored_basenames = {Path(d).name for d in self.ignored_directories}

            for root, dirs, files in os.walk(self.source_directory, topdown=True):
                # Filter the *in-place* list of dirs so os.walk never descends into them
                dirs[:] = [
                    d for d in dirs
                    if d not in ignored_basenames
                ]

                # Collect every file left
                for filename in files:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

            return file_paths

        def filter_files_by_extension(self, file_paths: List[str]) -> List[str]:
            """
            Filter files to include only those with supported extensions.
            
            Args:
                file_paths: List of file paths to filter
                
            Returns:
                List of filtered file paths
            """
            filtered_files = []
            for path in file_paths:
                if '.' in path:
                    extension = path.split('.')[-1].lower()
                    if extension in self.supported_extensions:
                        filtered_files.append(path)
            return filtered_files
        
        def remove_files_from_ignored_directories(self, 
                                                file_paths: List[str], 
                                                directories_to_remove: List[str]) -> List[str]:
            """
            Remove files that are located in specified directories.
            
            Args:
                file_paths: List of file paths
                directories_to_remove: List of directory paths to exclude
                
            Returns:
                Filtered list of file paths
            """
            if not directories_to_remove:
                return file_paths
            
            return [
                path for path in file_paths
                if not any(os.path.normpath(dir_to_remove) in os.path.normpath(path) 
                        for dir_to_remove in directories_to_remove)
            ]

        def get_file_size_kb(self, file_path: str) -> float:
            """
            Get file size in kilobytes.
            
            Args:
                file_path: Path to the file
                
            Returns:
                File size in KB, or 0 if file not found
            """
            try:
                stat_info = os.stat(file_path)
                size_bytes = stat_info.st_size
                return size_bytes / 1024
            except FileNotFoundError:
                return 0.0

        def compress_file_content(self, file_path: str) -> str:
            """
            Remove newlines and compress multiple tabs in a file.
            
            Args:
                file_path: Path to the file to compress
                
            Returns:
                Path to the processed file
                
            Raises:
                SystemExit: If file operations fail
            """
            if not isinstance(file_path, str):
                raise TypeError("file_path must be a string")

            try:
                # Read the file content
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Remove newlines and compress multiple tabs
                content = content.replace("\n", "")
                content = re.sub(r"\t{2,}", "\t", content)

                # Write the compressed content back
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)

                return file_path

            except FileNotFoundError:
                print(f"Error: '{file_path}' does not exist.", file=sys.stderr)
                sys.exit(1)
            except PermissionError:
                print(f"Error: Permission denied accessing '{file_path}'.", file=sys.stderr)
                sys.exit(1)
            except OSError as exc:
                print(f"OS error while processing '{file_path}': {exc}", file=sys.stderr)
                sys.exit(1)
            except Exception as exc:
                print(f"Unexpected error: {exc}", file=sys.stderr)
                sys.exit(1)
        
        def create_consolidated_file(self) -> Tuple[str, List[str], float]:
            """
            Create the final consolidated file with project structure and file contents.
            
            Returns:
                Tuple containing:
                - Path to the processed output file
                - List of processed source files
                - Output file size in KB
            """
            # Discover and filter files
            all_files = self.discover_all_files()
            source_files = self.filter_files_by_extension(all_files)
            
            # Add additional files if specified
            if self.additional_files:
                for file_path in self.additional_files:
                    abs_path = os.path.abspath(file_path)
                    if abs_path not in source_files:
                        source_files.append(abs_path)
        
            # Remove ignored files
            if self.ignored_files:
                ignored_abs_paths = [os.path.abspath(f) for f in self.ignored_files]
                source_files = [f for f in source_files 
                            if os.path.abspath(f) not in ignored_abs_paths]
            
            # Additional safety check: remove files from ignored directories
            if self.ignored_directories:
                source_files = self.remove_files_from_ignored_directories(
                    source_files, self.ignored_directories
                )
            
            # Create the header with project structure
            header = self._create_file_header()
            
            # Write header to output file
            with open(self.output_file_path, "w", encoding="utf-8") as outfile:
                outfile.write(header)
            
            # Process each source file
            processed_count = self._process_source_files(source_files)
            
            # Compress the final output file
            compressed_path = self.compress_file_content(self.output_file_path)
            file_size_kb = self.get_file_size_kb(self.output_file_path)
            
            return compressed_path, source_files, file_size_kb
        
        def _create_file_header(self) -> str:
            """Create the header section of the output file."""
            directory_tree = self.generate_directory_tree(self.source_directory)
            
            return f"""{self.ai_agent_prompt}
    PROJECT STRUCTURE:
    {'-'*40}
    {directory_tree}
    {'='*80}
    FILE CONTENTS:
    {'='*80}
    """
        
        def _process_source_files(self, source_files: List[str]) -> int:
            """
            Process each source file and append to output file.
            
            Args:
                source_files: List of source files to process
                
            Returns:
                Number of successfully processed files
            """
            processed_count = 0
            
            for file_path in source_files:
                relative_path = os.path.relpath(file_path, self.source_directory)
                
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        file_content = infile.read()
                except Exception as e:
                    click.echo(click.style(
                        f"⚠️  Could not read {relative_path}: {e}", fg='yellow'
                    ))
                    continue
                
                # Append file content with proper formatting
                self._append_file_content(relative_path, file_content)
                
                processed_count += 1
                
                # Show progress every 10 files
                if processed_count % 10 == 0:
                    click.echo(f"📦 Processed {processed_count}/{len(source_files)} files...")
            
            return processed_count
        
        def _append_file_content(self, relative_path: str, file_content: str) -> None:
            """
            Append a single file's content to the output file.
            
            Args:
                relative_path: Relative path of the file
                file_content: Content of the file
            """
            separator = f"\n{'-'*60}\n"
            
            with open(self.output_file_path, "a", encoding="utf-8") as outfile:
                outfile.write(
                    f"{separator}"
                    f"📁 File: {relative_path}\n"
                    f"{'-'*60}\n"
                    f"## File content: \n{file_content}\n"
                )
        
        def process(self) -> Tuple[str, List[str], float]:
            """
            Main method to process the codebase.
            
            This is the primary entry point for using the CodebaseProcessor.
            
            Returns:
                Tuple containing:
                - Path to the processed output file
                - List of processed source files  
                - Output file size in KB
            """
            return self.create_consolidated_file()
        
except Exception as error:
        print(error)




@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    epilog="""
\b
EXAMPLES:
    Basic usage (creates myproject_codebase.txt):
        $ codesqueeze myproject

    Include additional file types:
        $ codesqueeze myproject -e md -e yaml -e txt

    Exclude specific directories:
        $ codesqueeze myproject --ignore-dir tests --ignore-dir __pycache__

    Exclude specific files:
        $ codesqueeze myproject -i config.py -i secrets.json

    Include non-code files and set custom output:
        $ codesqueeze myproject -f README.md -f docs/notes.txt -o complete_project.txt

    Copy result directly to clipboard:
        $ codesqueeze myproject --copy

    Complex example with multiple options:
        $ codesqueeze myproject -e md -e yaml -i config.py --ignore-dir tests -f LICENSE -o project_export.txt --copy

\b
SUPPORTED FILE TYPES (by default):
    Programming: .py .js .ts .java .cpp .c .cs .go .rs .rb .php .swift .kt .scala
    Web: .html .css .jsx .tsx .vue .svelte .scss
    Scripts: .sh .bash .ps1 .bat .cmd
    Data: .sql .json .xml .yaml .yml
    And many more...

\b
NOTES:
    • Files are compressed (whitespace removed) to save space
    • Output includes project structure tree and file contents
    • Perfect for sharing with AI assistants like ChatGPT, Claude, or GitHub Copilot
    • Use --copy to get a ready-to-paste prompt for AI tools
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
    help="Include additional file extensions (without dot). Can be used multiple times.",
)
@click.option(
    "-i",
    "--ignore",
    multiple=True,
    metavar="FILE",
    help="Exclude specific files from processing. Path relative to PROJECT_DIR.",
)
@click.option(
    "--ignore-dir",
    "--ignore-directory", 
    "ignore_directory",
    multiple=True,
    metavar="DIR",
    help="Exclude entire directories from processing. Path relative to PROJECT_DIR.",
)
@click.option(
    "-f",
    "--add-files",
    multiple=True,
    metavar="FILE",
    help="Force include specific files, even if they don't match normal extensions.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    metavar="FILENAME",
    help="Custom output filename (default: PROJECT_DIR_codebase.txt).",
)
@click.option(
    "-c",
    "--copy",
    is_flag=True,
    help="Copy the generated file content to clipboard as an AI-ready prompt.",
)
def cli(directory, extra_extensions, ignore, ignore_directory, add_files, output, copy):
    """
    Transform your entire codebase into a single, AI-friendly text file.

    \b
    PROJECT_DIR: The directory containing your project to process
    
    \b
    WHAT IT DOES:
    • Scans your project directory recursively
    • Includes all common programming language files automatically  
    • Creates a structured text file with project tree + file contents
    • Compresses whitespace to maximize content in AI context windows
    • Generates files perfect for ChatGPT, Claude, and other AI assistants

    \b
    AUTOMATICALLY IGNORED:
    • Dependencies: node_modules, vendor, __pycache__, .git
    • Build outputs: dist, build, target
    • IDE files: .vscode, .idea
    • Binary and media files
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
    collector = CodebaseProcessor(
        source_directory=directory,
        additional_extensions=extra_extensions,
        ignored_files=processed_ignored,
        ignored_directories=processed_ignored_dirs,
        additional_files=processed_add_files,
        output_file=output
    )
    
    # Generate the codebase file
    final_file, processed_files, total_size_kb = collector.process()
    
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
