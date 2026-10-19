"""
Migration Files Deletion Tool
==============================
Deletes migration files from:
1. migrations folders inside apps (classic mode)
2. Central migrations folder by environment (development/production/testing)

Usage:
    python delete_migrations.py                    # Delete from all sources
    python delete_migrations.py --env development  # Delete from specific env only
    python delete_migrations.py --env production
    python delete_migrations.py --env testing
    python delete_migrations.py --apps-only        # Delete from app folders only
    python delete_migrations.py --central-only     # Delete from central folder only
    python delete_migrations.py --list             # List available environments
    python delete_migrations.py --dry-run          # Preview without deleting
"""

import os
import argparse
import shutil
from pathlib import Path


# Excluded directories
EXCLUDED_DIRS = [
    'erp_env', 'venv', '.venv', 'env', 'udsenv',
    'project', '.git', 'node_modules', '__pycache__',
    'site-packages'
]

# Central migrations folder path
CENTRAL_MIGRATIONS_PATH = Path('migrations')


def get_available_environments() -> list:
    """Get available environments in central folder"""
    envs = []
    if CENTRAL_MIGRATIONS_PATH.exists():
        for item in CENTRAL_MIGRATIONS_PATH.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                envs.append(item.name)
    return sorted(envs)


def list_environments():
    """Display available environments"""
    envs = get_available_environments()
    print("\n[+] Available environments in migrations/:")
    print("=" * 40)
    
    if not envs:
        print("  [!] No environments found")
        return
    
    for env in envs:
        env_path = CENTRAL_MIGRATIONS_PATH / env
        app_count = sum(1 for item in env_path.iterdir() 
                       if item.is_dir() and not item.name.startswith('_'))
        print(f"  [*] {env}/ ({app_count} apps)")
    
    print()


def delete_migration_files_from_apps(dry_run: bool = False) -> int:
    """
    Delete migration files from migrations folders inside apps
    (classic mode)
    """
    deleted_count = 0
    
    print("\n[*] Deleting from app folders...")
    print("-" * 40)
    
    for root, dirs, files in os.walk("."):
        # Exclude unwanted directories
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue
        
        # Skip central folder
        if root.startswith('./migrations') or root.startswith('.\\migrations'):
            continue
        
        # Search for migrations folders
        if 'migrations' in dirs:
            migration_path = os.path.join(root, 'migrations')
            
            for file_name in os.listdir(migration_path):
                file_path = os.path.join(migration_path, file_name)
                
                # Delete Python files (except __init__.py)
                if file_name != '__init__.py' and file_name.endswith('.py'):
                    if dry_run:
                        print(f"  [PREVIEW] {file_path}")
                    else:
                        print(f"  [DELETE] {file_path}")
                        os.remove(file_path)
                    deleted_count += 1
                
                # Delete .pyc files
                elif file_name.endswith('.pyc'):
                    if dry_run:
                        print(f"  [PREVIEW] {file_path}")
                    else:
                        print(f"  [DELETE] {file_path}")
                        os.remove(file_path)
                    deleted_count += 1
                
                # Delete __pycache__ folder
                elif file_name == '__pycache__' and os.path.isdir(file_path):
                    if dry_run:
                        print(f"  [PREVIEW] {file_path}/")
                    else:
                        print(f"  [DELETE] {file_path}/")
                        shutil.rmtree(file_path)
                    deleted_count += 1
    
    return deleted_count


def delete_migration_files_from_central(env: str = None, dry_run: bool = False) -> int:
    """
    Delete migration files from central folder
    
    Args:
        env: Specific environment (None = all environments)
        dry_run: Preview only without deleting
    """
    deleted_count = 0
    
    if not CENTRAL_MIGRATIONS_PATH.exists():
        print(f"\n[!] Central folder not found: {CENTRAL_MIGRATIONS_PATH}")
        return 0
    
    # Determine environments to delete
    if env:
        envs = [env]
    else:
        envs = get_available_environments()
    
    print(f"\n[*] Deleting from central folder...")
    print("-" * 40)
    
    for env_name in envs:
        env_path = CENTRAL_MIGRATIONS_PATH / env_name
        
        if not env_path.exists():
            print(f"  [!] Environment not found: {env_name}")
            continue
        
        print(f"\n  [ENV] {env_name}/")
        
        # Iterate through all files in environment
        for app_dir in env_path.rglob('*'):
            if app_dir.is_file():
                # Delete Python files (except __init__.py)
                if app_dir.name != '__init__.py' and app_dir.suffix == '.py':
                    if dry_run:
                        print(f"     [PREVIEW] {app_dir}")
                    else:
                        print(f"     [DELETE] {app_dir}")
                        app_dir.unlink()
                    deleted_count += 1
                
                # Delete .pyc files
                elif app_dir.suffix == '.pyc':
                    if dry_run:
                        print(f"     [PREVIEW] {app_dir}")
                    else:
                        print(f"     [DELETE] {app_dir}")
                        app_dir.unlink()
                    deleted_count += 1
    
    return deleted_count


def delete_pycache_from_central(dry_run: bool = False) -> int:
    """Delete __pycache__ folders from central folder"""
    deleted_count = 0
    
    if not CENTRAL_MIGRATIONS_PATH.exists():
        return 0
    
    for pycache_dir in CENTRAL_MIGRATIONS_PATH.rglob('__pycache__'):
        if pycache_dir.is_dir():
            if dry_run:
                print(f"     [PREVIEW] {pycache_dir}/")
            else:
                print(f"     [DELETE] {pycache_dir}/")
                shutil.rmtree(pycache_dir)
            deleted_count += 1
    
    return deleted_count


def main():
    parser = argparse.ArgumentParser(
        description='Migration Files Deletion Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--env', '-e',
        choices=['development', 'production', 'testing', 'dev', 'prod', 'test'],
        help='Delete from specific environment only'
    )
    
    parser.add_argument(
        '--apps-only', '-a',
        action='store_true',
        help='Delete from app folders only (classic mode)'
    )
    
    parser.add_argument(
        '--central-only', '-c',
        action='store_true',
        help='Delete from central folder only'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available environments only'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview files without deleting'
    )
    
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    args = parser.parse_args()
    
    # Convert shortcuts
    env_map = {'dev': 'development', 'prod': 'production', 'test': 'testing'}
    env = env_map.get(args.env, args.env) if args.env else None
    
    # List environments only
    if args.list:
        list_environments()
        return
    
    print("\n" + "=" * 50)
    print("[*] Migration Files Deletion Tool")
    print("=" * 50)
    
    if args.dry_run:
        print("[!] PREVIEW MODE - No files will be deleted")
    
    # Warning message and confirmation
    if not args.dry_run and not args.yes:
        print("\n" + "!" * 50)
        print("\n  [WARNING] All migration files will be deleted!")
        print("  [SOURCES]:")
        
        if not args.central_only:
            print("     - migrations folders inside apps")
        
        if not args.apps_only:
            if env:
                print(f"     - Central folder: migrations/{env}/")
            else:
                print("     - Central folder: migrations/ (all environments)")
        
        print("\n  [TIP] Use --dry-run to preview first")
        print("\n" + "!" * 50)
        
        confirm = input("\n  Continue? (y/n): ").strip().lower()
        
        if confirm not in ['y', 'yes']:
            print("\n  [X] Cancelled.\n")
            return
        
        print("\n  [OK] Deleting...\n")
    
    total_deleted = 0
    
    # Delete from app folders
    if not args.central_only:
        total_deleted += delete_migration_files_from_apps(args.dry_run)
    
    # Delete from central folder
    if not args.apps_only:
        total_deleted += delete_migration_files_from_central(env, args.dry_run)
        total_deleted += delete_pycache_from_central(args.dry_run)
    
    # Summary
    print("\n" + "=" * 50)
    if args.dry_run:
        print(f"[PREVIEW] {total_deleted} files/folders would be deleted")
    else:
        print(f"[DONE] {total_deleted} files/folders deleted")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
