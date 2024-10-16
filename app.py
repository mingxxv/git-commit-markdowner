import subprocess
import datetime
import os

# Set your Markdown file path
markdown_file_path = "git_commits.md"

def get_git_username():
    # Get the Git user name from the config
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True, text=True, check=True
        )
        username = result.stdout.strip()
        print(f"Debug: Retrieved Git user name - '{username}'")
        return username
    except subprocess.CalledProcessError as e:
        print(f"Error getting Git user name: {e}")
        return None

def is_git_repo(path):
    # Check if a directory is a Git repository
    return os.path.isdir(os.path.join(path, ".git"))

def get_git_commits_for_repo(repo_path, author, date_str):
    # Prepare the git log command with debug statements
    command = [
        "git", "-C", repo_path, "log", "--all",
        f"--author={author}",
        f"--since={date_str}",
        f"--until={date_str}",
        "--date=short"
    ]
    print(f"Debug: Running command in repo {repo_path}: {' '.join(command)}")

    # Run the git log command
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Debug: Command output received.")
        if result.stdout:
            print(f"Debug: Found commits in {repo_path}:\n{result.stdout}")
        else:
            print(f"Debug: No commits found for {repo_path} on this date.")
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running git log command in {repo_path}: {e}")
        return []

def append_commits_to_markdown(date_str, commits, repo_path):
    with open(markdown_file_path, "a") as file:
        # Add a new date section
        file.write(f"## Commits for {date_str} in {repo_path}\n")
        if commits:
            for commit in commits:
                file.write(f"- {commit}\n")
            file.write("\n")  # Add an empty line for spacing
        else:
            file.write("No commits made on this date.\n\n")
        print(f"Debug: Commits appended to {markdown_file_path}")

def get_date_input():
    # Prompt the user to enter a date or use the current date
    today = datetime.date.today().strftime("%Y-%m-%d")
    date_str = input(f"Enter the date (YYYY-MM-DD) or press Enter to use today ({today}): ").strip()
    
    # Validate the date format if provided, otherwise use today's date
    if date_str:
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date as YYYY-MM-DD.")
            return get_date_input()  # Recursively prompt again if date is invalid
    else:
        date_str = today
    
    print(f"Debug: Using date - {date_str}")
    return date_str

def main():
    author = get_git_username()
    if author:
        date_str = get_date_input()
        
        # Traverse through directories and log commits
        home_dir = os.path.expanduser("~")  # Start from the user's home directory
        for root, dirs, files in os.walk(home_dir):
            for dir in dirs:
                repo_path = os.path.join(root, dir)
                if is_git_repo(repo_path):
                    commits = get_git_commits_for_repo(repo_path, author, date_str)
                    append_commits_to_markdown(date_str, commits, repo_path)
        
        print(f"Commits for {date_str} have been added to {markdown_file_path}")

if __name__ == "__main__":
    main()
