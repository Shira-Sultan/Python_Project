import ctypes
import json
import os
import webbrowser

from colorama import Fore
from fastapi import requests

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


    def push(self):
        url = 'http://localhost:8000/'

        folders = [f for f in os.listdir(self.path_commiting) if os.path.isdir(os.path.join(self.path_commiting, f))]
        if not folders:
            print(Fore.RED + "No folders found in the commiting path")
            return

        folders = sorted(folders, key=lambda f: os.path.getmtime(os.path.join(self.path_commiting, f)))
        last_commit = folders[-1]

        folder_to_zip = os.path.join(self.path_commiting, last_commit)
        zip_base = folder_to_zip
        zip_path = zip_base + '.zip'

        shutil.make_archive(base_name=zip_base, format='zip', root_dir=folder_to_zip)

        try:
            with open(zip_path, 'rb') as file:
                files = {'file': ('MyFolder.zip', file, 'application/zip')}

                # שליחת בקשה ל-alert
                alert_resp = requests.post(url + 'alert', files=files)
                if alert_resp.status_code == 200:
                    alert_data = alert_resp.json()
                    print(Fore.GREEN + "Alert response:")
                    print(Fore.GREEN + json.dumps(alert_data, indent=4, ensure_ascii=False))
                else:
                    print(Fore.RED + f"Alert request failed: {alert_resp.status_code}")

                file.seek(0)
                files = {'file': ('MyFolder.zip', file, 'application/zip')}

                # שליחת בקשה ל-analyze
                graphs_resp = requests.post(url + 'analyze', files=files)
                for i in graphs_resp:
                    print(i)
                if graphs_resp.status_code == 200:
                    paths = graphs_resp.json()
                    print(Fore.CYAN + "\nOpening graph images...")
                    for path in paths:
                        webbrowser.open(path)
                else:
                    print(Fore.RED + f"Graphs request failed: {graphs_resp.status_code}")

        except Exception as e:
            print(Fore.RED + f"An error occurred: {str(e)}")

