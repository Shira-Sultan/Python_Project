import ctypes
import os
import File
import shutil

from Commit import Commit


class Repository:

    def __init__(self):
        self.repo_path = os.getcwd()
        self.dict_commits = {}


    def init(self):
        if not os.path.exists(os.path.join(self.repo_path, ".wit")):
            File.create_folder(self.repo_path, ".wit")
            wit_path = os.path.join(self.repo_path, ".wit")
            ctypes.windll.kernel32.SetFileAttributesW(wit_path, 2)  # תקייה נסתרת
            File.create_folder(wit_path, "commits")
            File.create_folder(wit_path, "staging")
            print(fr"Initialized empty Wit repository in {self.repo_path}\.wit")
        else:
            print(fr"Reinitialized existing Wit repository in {self.repo_path}\.wit")


    def add(self, file_name):
        if File.search_file(os.getcwd(), file_name):
            shutil.copy(fr"{os.getcwd()}\{file_name}",fr"{self.repo_path}\.wit\staging\{file_name}")
            print("The file added successfully.")


    def commit(self, m):
        cur_commit = Commit(m)
        print(cur_commit)
        commit_path = os.path.join(self.repo_path, '.wit', 'commits')
        File.create_folder(commit_path, str(cur_commit.hash_commit))

        for dirpath, dirnames, filenames in os.walk(self.repo_path): # נתיב לספרייה הנוכחית, שמות ספריות המשנה בספרייה הנוכחית, שמות הקבצים בספרייה הנוכחית
            if not dirpath.startswith(os.path.join(self.repo_path, '.wit')):
                for filename in filenames:
                    staging_file_path = os.path.join(self.repo_path, '.wit', 'staging', filename)
                    source_file_path = os.path.join(dirpath, filename)

                    if not os.path.exists(staging_file_path):
                        shutil.copy(source_file_path, os.path.join(commit_path, str(cur_commit.hash_commit)))  # Copy each file individually

        # Copy staging area files
        shutil.copytree(os.path.join(self.repo_path, '.wit', 'staging'), os.path.join(commit_path, str(cur_commit.hash_commit)), dirs_exist_ok=True)
        File.empty_folder(os.path.join(self.repo_path, '.wit', 'staging'))

        self.dict_commits[f"{cur_commit.hash_commit}"] = cur_commit
        print("The commit was successful.")
        for key, value in self.dict_commits.items():
            print(f"hash_commit: {key}")
            print(f"date: {value.date}")
            print(f"message: {value.message}")


    def log(self):
        # for commit_hash in self.dict_commits.items():
        #     print(fr"{commit_hash}: {self.dict_commits[commit_hash]}")

        for key, value in self.dict_commits.items():
            print(f"hash_commit: {key}")
            print(f"date: {value.date}")
            print(f"message: {value.message}")


    def status(self):
        if  os.listdir(os.path.join(self.repo_path, '.wit', 'staging')):
            print("There are uncommitted changes.")
        else:
            print("There are no uncommitted changes.")


    def checkout(self, hash_commit):
        cur_commit_path = os.path.join(self.repo_path, '.wit', 'commits', hash_commit)
        File.clear_and_copy(cur_commit_path, self.repo_path)
