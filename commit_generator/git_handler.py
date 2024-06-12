import subprocess

class GitHandler:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_change_summary(self):
        try:
            result = subprocess.run(['git', 'diff', '--name-only', '--cached'], cwd=self.repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            result.check_returncode()
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting change summary: {e.stderr}")
            return None

    def has_staged_changes(self):
        try:
            result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=self.repo_path)
            return result.returncode != 0
        except subprocess.CalledProcessError as e:
            print(f"Error checking staged changes: {e.stderr}")
            return False
