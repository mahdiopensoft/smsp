"""
folders_commit.py
=================
A custom, interactive Git CLI that allows you to easily commit files on a per-folder basis.

Features:
- Reads from `allow_folders.txt` to strictly limit which folders can be committed.
- Automatically generates `allow_folders.txt` if it doesn't exist, skipping ignored folders.
- Respects your `.gitignore` configuration perfectly.
- Supports bulk committing, custom messages, file-level inspection, and push.

Usage:
1. Run `python folders_commit.py`.
2. The script will present a menu of modified folders that are listed in `allow_folders.txt`.
3. Enter numbers or names (e.g., '1,3' or 'src, public') to auto-commit those folders.
4. Use '<targets> -m "My message"' (e.g., '1,3 -m "Fix bug"' or 'src -m "Update"') to commit folders with a specific custom message.
5. Use '<targets> -v' (e.g., '1 -v' or 'src -v') to view the specific modified files inside a folder.
6. Use 'undo' to safely revert your last commit.
7. Use 'push' to push all commits to your remote repository.
"""

import subprocess
import os
import sys
import fnmatch

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Change these variables to set your default push destination
DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "mr_amer"

# ==============================================================================
# UTILITIES
# ==============================================================================
def run_git(*args, check=False):
    """
    Central wrapper for all Git commands.
    Returns the subprocess.CompletedProcess result.
    """
    result = subprocess.run(
        ['git', *args],
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"❌ Git Command Failed: git {' '.join(args)}")
        if result.stderr:
            print(f"Error Details:\n{result.stderr.strip()}")
    return result

# ==============================================================================
# 1. ALLOWED FOLDERS PARSER
# ==============================================================================
def load_allow_folders():
    """
    Reads allow_folders.txt. If it doesn't exist, it auto-generates it by finding
    all directories in the current folder.
    """
    allow_file = 'allow_folders.txt'
    if not os.path.exists(allow_file):
        print(f"\n[INFO] '{allow_file}' not found. Generating it automatically...")
        try:
            # List all directories and files in root, excluding hidden ones
            items_to_add = [d for d in os.listdir('.') if not d.startswith('.')]
            
            # Skip items that are already ignored by .gitignore
            ignore_patterns = load_gitignore_patterns()
            valid_items = [d for d in items_to_add if not is_path_ignored(d, ignore_patterns)]
            
            # Separate into folders and files
            valid_folders = [d for d in valid_items if os.path.isdir(d)]
            valid_files = [d for d in valid_items if os.path.isfile(d)]
            
            with open(allow_file, 'w', encoding='utf-8') as f:
                f.write("# ========================================================\n")
                f.write("# ALLOWED FOLDERS AND FILES LIST\n")
                f.write("# ========================================================\n")
                f.write("# This file controls which folders and root files are ALLOWED to be committed.\n")
                f.write("# If an item is not listed here, it will be HIDDEN from the commit menu.\n")
                f.write("# You can delete lines to hide items, or manually add items.\n")
                f.write("# ========================================================\n\n")
                
                f.write("# --- FOLDERS ---\n")
                for d in sorted(valid_folders):
                    f.write(f"{d}\n")
                    
                f.write("\n# --- FILES ---\n")
                for d in sorted(valid_files):
                    f.write(f"{d}\n")
            
            # Write a helpful usage text
            print("=" * 60)
            print(f"✅ Generated {allow_file}.")
            print("   This file controls which folders and files are ALLOWED to be committed.")
            print("   Please open 'allow_folders.txt' and DELETE any items")
            print("   you want to hide from the commit menu.")
            print("=" * 60 + "\n")
            
        except Exception as e:
            print(f"Error creating {allow_file}: {e}")
            return set()
            
    allowed = set()
    with open(allow_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Normalize path
            line = line.replace('\\', '/')
            if line.startswith('./'):
                line = line[2:]
            if line and not line.startswith('#'):
                allowed.add(line.lower())
    return allowed

def is_folder_allowed(folder, allowed_set):
    """
    Checks if a folder path is in the allowed list.
    """
    parts = folder.split('/')
    for i in range(len(parts)):
        sub = '/'.join(parts[:i+1]).lower()
        if sub in allowed_set:
            return True
    return False

# ==============================================================================
# 2. GITIGNORE PARSER
# ==============================================================================
def load_gitignore_patterns():
    """
    Reads the .gitignore file directly from the filesystem and extracts the rules.
    Returns a tuple of (ignore_patterns, exception_patterns).
    """
    ignore_patterns = []
    exception_patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith('#'):
                    # Strip trailing slash to make pattern matching simpler
                    if line.endswith('/'):
                        line = line[:-1]
                    
                    if line.startswith('!'):
                        exception_patterns.append(line[1:])
                    else:
                        ignore_patterns.append(line)
    return ignore_patterns, exception_patterns

def is_path_ignored(path, rules):
    """
    Checks if a given file path matches any of the parsed .gitignore rules.
    Supports negations (e.g., '!filename.py').
    """
    ignore_patterns, exception_patterns = rules
    
    def matches_patterns(subp, part, patterns):
        for pattern in patterns:
            if pattern.startswith('/'):
                p = pattern[1:]
                if fnmatch.fnmatch(subp, p):
                    return True
            else:
                if fnmatch.fnmatch(part, pattern) or fnmatch.fnmatch(subp, pattern):
                    return True
        return False

    parts = path.split('/')
    is_ignored = False
    
    # We check the file itself, and every parent directory it belongs to.
    for i in range(len(parts)):
        subpath = '/'.join(parts[:i+1])
        current_part = parts[i]
        
        if matches_patterns(subpath, current_part, ignore_patterns):
            is_ignored = True
            
        if matches_patterns(subpath, current_part, exception_patterns):
            is_ignored = False
            
    return is_ignored

# ==============================================================================
# 3. GIT STATUS FETCHING
# ==============================================================================
def get_modified_items():
    """
    Runs `git status --porcelain` to find all modified, deleted, or untracked files.
    Filters them by allow_folders.txt AND .gitignore.
    """
    try:
        result = run_git('status', '--porcelain')
        
        items = set() 
        file_details = {} 
        
        # Load our custom rules
        ignore_patterns = load_gitignore_patterns()
        allowed_folders = load_allow_folders()
        
        for line in result.stdout.splitlines():
            if len(line) > 3:
                # The first two characters represent the Git status (e.g., 'M ', '??', ' D')
                status = line[:2].strip()
                
                # The rest is the file path. We strip surrounding quotes if they exist.
                path = line[3:].strip('"')
                
                # Skip the file if it matches our manual .gitignore rules
                if is_path_ignored(path, ignore_patterns):
                    continue
                
                # Extract the directory containing the file
                folder = os.path.dirname(path).replace('\\', '/')
                
                if folder == "":
                    # If there's no folder, it's a root file.
                    # Allow it if the specific filename is in allow_folders, OR if "." or "root" is there.
                    if "." in allowed_folders or "root" in allowed_folders or path.lower() in allowed_folders:
                        items.add(('file', path))
                        if 'root' not in file_details:
                            file_details['root'] = []
                        file_details['root'].append((status, path))
                else:
                    # Folder must be in the allow_folders.txt list
                    if not is_folder_allowed(folder, allowed_folders):
                        continue
                        
                    items.add(('folder', folder))
                    if folder not in file_details:
                        file_details[folder] = []
                    # Store the raw path for git add, and the status for displaying
                    file_details[folder].append((status, path))
                    
        # Sort the final list so folders appear at the top, and root files at the bottom
        sorted_items = sorted(list(items), key=lambda x: (0 if x[0] == 'folder' else 1, x[1]))
        return sorted_items, file_details
    
    except Exception as e:
        print(f"Error checking git status: {e}")
        return [], {}

# ==============================================================================
# 4. INTERACTIVE PULL SUB-MENU
# ==============================================================================
def get_remote_diff_items(remote, branch):
    print(f"\n☁️ Fetching {remote}/{branch}...")
    run_git('fetch', remote, branch, check=True)
    
    # Get files different between local HEAD and remote branch
    res = run_git('diff', '--name-only', f'HEAD...{remote}/{branch}')
    if res.returncode != 0:
        return [], {}
        
    items = set() 
    file_details = {} 
    
    ignore_patterns = load_gitignore_patterns()
    allowed_folders = load_allow_folders()
    
    for path in res.stdout.splitlines():
        path = path.strip()
        if not path: continue
        if is_path_ignored(path, ignore_patterns):
            continue
            
        folder = os.path.dirname(path).replace('\\', '/')
        if folder == "":
            if "." in allowed_folders or "root" in allowed_folders or path.lower() in allowed_folders:
                items.add(('file', path))
                if 'root' not in file_details:
                    file_details['root'] = []
                file_details['root'].append(('M', path))
        else:
            if not is_folder_allowed(folder, allowed_folders):
                continue
            items.add(('folder', folder))
            if folder not in file_details:
                file_details[folder] = []
            file_details[folder].append(('M', path))
            
    sorted_items = sorted(list(items), key=lambda x: (0 if x[0] == 'folder' else 1, x[1]))
    return sorted_items, file_details

def interactive_pull_menu(remote, branch, items, file_details):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n☁️ ALLOWED ITEMS CHANGED IN {remote}/{branch}:")
        print("-" * 55)
        for i, (item_type, name) in enumerate(items):
            if item_type == "folder":
                file_count = len(file_details[name])
                print(f"[{i+1}] 📁 {name} ({file_count} file(s))")
            else:
                print(f"[{i+1}] 📄 {name}")
        print("-" * 55)
        
        print("\n🛠️  PULL COMMANDS:")
        print("  <numbers/names> : Pull specific items (e.g., '1,3' or 'src')")
        print("  all             : Pull everything listed above")
        print("  <targets> -v    : View exact files changed inside a folder (e.g., 1 -v)")
        print("  q               : Cancel and return to main menu")
        
        choice = input("\nYour choice: ").strip()
        choice_lower = choice.lower()
        
        if choice_lower == 'q' or not choice_lower:
            return
            
        if '-v' in choice_lower:
            target = choice_lower.replace('-v', '').strip()
            if target:
                matched_items = []
                try:
                    idx = int(target) - 1
                    if 0 <= idx < len(items):
                        matched_items.append(items[idx])
                except ValueError:
                    for item in items:
                        if target.lower() in item[1].lower():
                            matched_items.append(item)
                if not matched_items:
                    print(f"❌ Could not find any item matching '{target}'.")
                else:
                    for item_type, name in matched_items:
                        print(f"\n🔍 Details for '{name}':")
                        if item_type == 'folder':
                            for status, path in file_details[name]:
                                print(f"  {path}")
                        else:
                            for status, path in file_details['root']:
                                if path == name:
                                    print(f"  {path}")
            else:
                print("❌ Please specify a number or name, e.g., '1 -v'")
            input("\nPress Enter to continue...")
            continue
            
        selected_items = []
        if choice_lower == 'all':
            selected_items = items
        else:
            selected_set = set()
            for part in choice.split(','):
                part = part.strip()
                if not part: continue
                try:
                    idx = int(part) - 1
                    if 0 <= idx < len(items):
                        selected_set.add(items[idx])
                    else:
                        print(f"❌ Warning: Number '{part}' is out of range.")
                except ValueError:
                    matched = False
                    for item in items:
                        if part.lower() in item[1].lower():
                            selected_set.add(item)
                            matched = True
                    if not matched:
                        print(f"❌ Warning: Could not find '{part}'.")
            selected_items = [item for item in items if item in selected_set]
            
        if not selected_items:
            input("\nPress Enter to continue...")
            continue
            
        # SAFETY CHECK
        print("\n🔍 Checking for uncommitted local changes...")
        local_status = run_git('status', '--porcelain')
        uncommitted_files = []
        for line in local_status.stdout.splitlines():
            if len(line) > 3:
                path = line[3:].strip('"')
                uncommitted_files.append(path.replace('\\', '/'))
                
        conflict_detected = False
        for item_type, name in selected_items:
            for un_file in uncommitted_files:
                if item_type == 'folder' and (un_file.startswith(name + '/') or un_file == name):
                    print(f"❌ Error: You have uncommitted changes in '{un_file}'.")
                    conflict_detected = True
                elif item_type == 'file' and un_file == name:
                    print(f"❌ Error: You have uncommitted changes in '{name}'.")
                    conflict_detected = True
                    
        if conflict_detected:
            print("\n🚨 PULL ABORTED: Please commit, stash, or undo your local changes in these folders first!")
            input("\nPress Enter to return to menu...")
            continue
            
        # Pull
        print("\n🚀 PULLING (CHECKOUT)...")
        success_count = 0
        for item_type, name in selected_items:
            print(f"-> Pulling '{name}' from {remote}/{branch}...")
            paths_to_checkout = [path for status, path in file_details[name]] if item_type == 'folder' else [name]
            res = run_git('checkout', f'{remote}/{branch}', '--', *paths_to_checkout, check=True)
            if res.returncode == 0:
                success_count += 1
                
        print(f"\n✅ Successfully pulled {success_count} item(s)! (They are now staged in your git index)")
        
        items = [item for item in items if item not in selected_items]
        if not items:
            print("✅ All changed items from this branch have been pulled.")
            input("\nPress Enter to return to main menu...")
            return
            
        input("\nPress Enter to refresh the list...")

# ==============================================================================
# 5. MAIN INTERACTIVE CLI
# ==============================================================================
def main():
    while True:
        # Clear terminal screen for a clean, refreshing UI every time the loop restarts
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Fetch the latest items
        items, file_details = get_modified_items()
        
        if not items:
            # Check if there are unpushed commits
            res = run_git('log', f'{DEFAULT_REMOTE}/{DEFAULT_BRANCH}..HEAD', '--oneline')
            if res.returncode == 0:
                unpushed = res.stdout.strip().splitlines()
            else:
                unpushed = []
                
            if unpushed:
                print("\n✅ All modified files have been committed.")
                print(f"☁️  However, you have {len(unpushed)} unpushed commit(s)!")
                print("Would you like to push them to the remote repository now?")
                print("  y : Push")
                print("  n : Quit")
                
                choice = input("\nYour choice: ").strip().lower()
                if choice == 'y':
                    print(f"\n☁️ Pushing to {DEFAULT_REMOTE} {DEFAULT_BRANCH}...")
                    run_git('push', DEFAULT_REMOTE, DEFAULT_BRANCH, check=True)
                return
            else:
                print("\n✅ No modified files found (and no unpushed commits).")
                return

        # ---------------------------------------------------------
        # DISPLAY MENU
        # ---------------------------------------------------------
        print("\n📁 ALLOWED MODIFIED ITEMS:")
        print("-" * 55)
        for i, (item_type, name) in enumerate(items):
            if item_type == "folder":
                # Display folder with the number of modified files inside it
                file_count = len(file_details[name])
                print(f"[{i+1}] 📁 {name} ({file_count} file(s))")
            else:
                # Display standalone root file
                print(f"[{i+1}] 📄 {name}")
        print("-" * 55)
        
        print("\n🛠️  COMMANDS:")
        print("  <numbers/names> [-p]   : Auto-commit items (add -p to push after) (e.g., '1,3 -p')")
        print("  <targets> -m \"msg\" [-p]: Commit with custom message and optionally push")
        print("  all [-p]               : Auto-commit everything (and optionally push)")
        print("  <targets> -v           : View exact files modified inside a folder (e.g., 1 -v)")
        print("  undo                   : Undo the last commit safely")
        print("  push                   : Push all your commits to the remote repository")
        print("  pull <branch>          : Pull specific folders from a remote branch (e.g. pull dev)")
        print("  q                      : Quit")
        
        # Get user input
        choice = input("\nYour choice: ").strip()
        choice_lower = choice.lower()
        
        if choice_lower == 'q' or not choice_lower:
            print("Canceled. Exiting...")
            return
            
        # Check if the user appended '-p' to the end of their command
        should_push = False
        if choice_lower.endswith('-p'):
            should_push = True
            choice = choice[:-2].strip()
            choice_lower = choice_lower[:-2].strip()
            
        # ---------------------------------------------------------
        # COMMAND: PULL
        # ---------------------------------------------------------
        if choice_lower.startswith('pull'):
            parts = choice.split()
            if len(parts) >= 2:
                remote = DEFAULT_REMOTE
                branch = parts[1]
                
                # Allow overriding remote (e.g. pull origin dev)
                if len(parts) >= 3:
                    remote = parts[1]
                    branch = parts[2]
                    
                remote_items, remote_details = get_remote_diff_items(remote, branch)
                if not remote_items:
                    print(f"\n✅ No allowed folders have changed in {remote}/{branch} compared to your local branch.")
                    input("\nPress Enter to continue...")
                else:
                    interactive_pull_menu(remote, branch, remote_items, remote_details)
            else:
                print(f"❌ Please specify a branch, e.g., 'pull {DEFAULT_BRANCH}'")
                input("\nPress Enter to continue...")
            continue
            
        # ---------------------------------------------------------
        # COMMAND: PUSH
        # ---------------------------------------------------------
        if choice_lower.startswith('push'):
            parts = choice.split()
            remote = DEFAULT_REMOTE
            branch = DEFAULT_BRANCH
            
            # Allow overriding: e.g. "push origin dev"
            if len(parts) >= 2:
                remote = parts[1]
            if len(parts) >= 3:
                branch = parts[2]
                
            print(f"\n☁️ Pushing to remote '{remote}' on branch '{branch}'...")
            run_git('push', remote, branch, check=True)
            input("\nPress Enter to continue...")
            continue
            
        # ---------------------------------------------------------
        # COMMAND: VIEW FILES (-v)
        # ---------------------------------------------------------
        if '-v' in choice_lower and '"' not in choice and "'" not in choice:
            target = choice_lower.replace('-v', '').strip()
            if target:
                matched_items = []
                try:
                    idx = int(target) - 1
                    if 0 <= idx < len(items):
                        matched_items.append(items[idx])
                except ValueError:
                    # Treat as string search
                    for item in items:
                        if target.lower() in item[1].lower():
                            matched_items.append(item)
                            
                if not matched_items:
                    print(f"❌ Could not find any item matching '{target}'.")
                else:
                    for item_type, name in matched_items:
                        print(f"\n🔍 Details for '{name}':")
                        if item_type == 'folder':
                            for status, path in file_details[name]:
                                print(f"  [{status}] {path}")
                        else:
                            for status, path in file_details['root']:
                                if path == name:
                                    print(f"  [{status}] {path}")
            else:
                print("❌ Please specify a number or name, e.g., '1 -v' or 'src -v'")
            input("\nPress Enter to continue...")
            continue
            
        # ---------------------------------------------------------
        # COMMAND: UNDO COMMIT
        # ---------------------------------------------------------
        if choice_lower.startswith('undo'):
            parts = choice_lower.split()
            count = 1
            if len(parts) > 1:
                try:
                    count = int(parts[1])
                except ValueError:
                    print("❌ Invalid number for undo.")
                    input("\nPress Enter to continue...")
                    continue
            
            # Find out which files are in the commits we are about to undo
            diff_res = run_git('diff', '--name-only', f'HEAD~{count}', 'HEAD')
            if diff_res.returncode != 0:
                print(f"❌ Error: Could not find {count} commit(s) to undo. (Are you at the first commit?)")
                input("\nPress Enter to continue...")
                continue
            undone_files = diff_res.stdout.splitlines()
            
            print(f"\n⏪ Undoing the last {count} commit(s)...")
            res = run_git('reset', f'HEAD~{count}', check=True)
            
            if res.returncode == 0:
                print("\n📂 FILES UNDONE (These files are no longer committed):")
                if undone_files:
                    for f in undone_files:
                        print(f"  - {f}")
                else:
                    print("  (No files were changed in these commits)")
            else:
                print("\n❌ Failed to undo commits.")
                
            input("\nPress Enter to continue...")
            continue
            
        # ---------------------------------------------------------
        # COMMAND: CUSTOM MESSAGE (-m)
        # ---------------------------------------------------------
        elif '-m' in choice_lower or choice_lower.startswith('m '):
            # Parse inputs like: 1,2 -m "My message" or m src "My message"
            try:
                quote_char = '"'
                if '"' not in choice and "'" in choice:
                    quote_char = "'"
                    
                if quote_char in choice:
                    parts = choice.split(quote_char)
                    if len(parts) >= 2:
                        before_quote = parts[0]
                        custom_msg = parts[1].strip()
                        
                        # Extract targets by removing '-m' or 'm '
                        target = before_quote.lower().replace('-m', '').strip()
                        if target.startswith('m '):
                            target = target[2:].strip()
                        
                        selected_set = set()
                        for part in target.split(','):
                            part = part.strip()
                            if not part: continue
                            
                            try:
                                idx = int(part) - 1
                                if 0 <= idx < len(items):
                                    selected_set.add(items[idx])
                            except ValueError:
                                for item in items:
                                    if part.lower() in item[1].lower():
                                        selected_set.add(item)
                                        
                        matched_items = [item for item in items if item in selected_set]
                        
                        if not matched_items:
                            print(f"❌ Could not find any item matching '{target}'.")
                        else:
                            for item_type, name in matched_items:
                                print(f"\n🚀 Committing '{name}' with custom message: '{custom_msg}'")
                                
                                if item_type == 'folder':
                                    files_to_add = [path for status, path in file_details[name]]
                                    run_git('add', *files_to_add, check=True)
                                else:
                                    run_git('add', name, check=True)
                                    
                                res = run_git('commit', '-m', custom_msg, check=True)
                                
                                if res.returncode == 0:
                                    print(f"✅ Successfully committed!")
                            
                            if should_push:
                                print(f"\n☁️ Auto-pushing to {DEFAULT_REMOTE} {DEFAULT_BRANCH}...")
                                run_git('push', DEFAULT_REMOTE, DEFAULT_BRANCH, check=True)
                else:
                    print("❌ Format must be: <targets> -m \"Your message\" (quotes are required around the message)")
            except Exception as e:
                print(f"❌ Invalid input for custom message: {e}")
            
            input("\nPress Enter to continue...")
            continue
            
        # ---------------------------------------------------------
        # COMMAND: AUTO COMMIT BY NUMBERS, NAMES OR 'ALL'
        # ---------------------------------------------------------
        selected_items = []
        if choice_lower == 'all':
            selected_items = items
        else:
            selected_set = set()
            for part in choice.split(','):
                part = part.strip()
                if not part:
                    continue
                
                try:
                    idx = int(part) - 1
                    if 0 <= idx < len(items):
                        selected_set.add(items[idx])
                    else:
                        print(f"❌ Warning: Number '{part}' is out of range.")
                except ValueError:
                    # Treat as string search
                    matched = False
                    for item in items:
                        if part.lower() in item[1].lower():
                            selected_set.add(item)
                            matched = True
                    if not matched:
                        print(f"❌ Warning: Could not find any item matching '{part}'.")
            
            # Convert back to list while keeping original order
            selected_items = [item for item in items if item in selected_set]
            
        if not selected_items:
            # We already warned them about invalid names/numbers
            input("\nPress Enter to continue...")
            continue
            
        print("\n🚀 COMMITTING...")
        success_count = 0
        for item_type, name in selected_items:
            # Generate a clean, automatic commit message from the path name
            auto_msg = name.replace('./', '')
            
            print(f"-> Adding & Committing '{name}' with message: '{auto_msg}'")
            
            # Add only the specific files that passed the gitignore check
            if item_type == 'folder':
                files_to_add = [path for status, path in file_details[name]]
                run_git('add', *files_to_add, check=True)
            else:
                run_git('add', name, check=True)
                
            res = run_git('commit', '-m', auto_msg, check=True)
            
            if res.returncode == 0:
                success_count += 1
            
        print(f"\n✅ Successfully created {success_count} auto-commit(s)!")
        
        if should_push and success_count > 0:
            print(f"\n☁️ Auto-pushing to {DEFAULT_REMOTE} {DEFAULT_BRANCH}...")
            run_git('push', DEFAULT_REMOTE, DEFAULT_BRANCH, check=True)
            
        input("\nPress Enter to refresh the list...")

# Ensure the script runs when executed directly
if __name__ == "__main__":
    main()
