import subprocess
import datetime

# Set your Markdown file path
markdown_file_path = "git_commits.md"

def get_git_commits_for_today():
    # Set the date for today
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Run the git log command
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--author=$(git config user.name)",
             f"--since={date_str}", f"--until={date_str}",
             "--pretty=format:%h %ad | %s", "--date=short"],
            capture_output=True, text=True, shell=True, check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def append_commits_to_markdown(commits):
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    with open(markdown_file_path, "a") as file:
        # Add a new date section
        file.write(f"## Commits for {date_str}\n")
        if commits:
            for commit in commits:
                file.write(f"- {commit}\n")
            file.write("\n")  # Add an empty line for spacing
        else:
            file.write("No commits made today.\n\n")

def main():
    commits = get_git_commits_for_today()
    append_commits_to_markdown(commits)
    print(f"Commits for today ({datetime.date.today()}) have been added to {markdown_file_path}")

if __name__ == "__main__":
    main()
