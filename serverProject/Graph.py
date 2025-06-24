import json
import os
import io
import zipfile
from datetime import datetime

import matplotlib.pyplot as plt
from fastapi import UploadFile, File
import analyze


class Graph:
    def __init__(self, file: UploadFile = File(...)):
        self.graph_image = []
        self.file = file
        self.output_path = os.path.join(
            r'C:\Users\user1\Desktop\B הנדסאים\Python2\projects\serverProject', 'Graphs'
        )
        os.makedirs(self.output_path, exist_ok=True)

    def get_graphs_images(self):
        count_error_for_file = {}
        zip_bytes = io.BytesIO(self.file.file.read())

        with zipfile.ZipFile(zip_bytes) as z:
            print("Zip file opened successfully.")
            for file_info in z.infolist():
                print(f"Found file: {file_info.filename}")
                if file_info.filename.endswith('.py'):
                    with z.open(file_info) as f:
                        code_str = f.read().decode('utf-8')

                        # יצירת שם תיקייה ייחודי לכל קובץ לפי הנתיב בתוך ה-ZIP, בלי הסיומת .py
                        safe_filename = file_info.filename.replace("/", "__").replace("\\", "__")
                        safe_name_without_ext = os.path.splitext(safe_filename)[0]
                        file_graph_dir = os.path.join(self.output_path, safe_name_without_ext)
                        os.makedirs(file_graph_dir, exist_ok=True)

                        print("Creating histogram graph...")
                        self.create_histogram_graph(code_str, file_graph_dir)
                        print("Histogram graph created.")

                        print("dict_problems after get_functions_length:", analyze.dict_problems)
                        analyze.get_file_length(code_str)
                        print("dict_problems after get_file_length:", analyze.dict_problems)
                        analyze.get_find_unused_variables(code_str)
                        print("dict_problems after get_find_unused_variables:", analyze.dict_problems)
                        analyze.get_find_missing_docstrings(code_str)
                        print("dict_problems after get_find_missing_docstrings:", analyze.dict_problems)

                        print("Creating pie chart...")
                        self.create_pie_chart(file_graph_dir)
                        print("Pie chart created.")

                        count_error_for_file[file_info.filename] = sum(analyze.dict_problems.values())

        analyze.dict_problems.clear()

        print("Creating bar chart...")
        self.create_bar_chart(count_error_for_file)
        print("Bar chart created.")

        total_issues_today = sum(count_error_for_file.values())
        self.save_daily_issues_history(total_issues_today)

        print("Creating line chart...")
        self.create_line_chart()
        print("Line chart created.")

        return self.graph_image

    def create_histogram_graph(self, code_str: str, output_dir: str):
        func_length = analyze.get_functions_length(code_str)
        function_names = list(func_length.keys())
        lengths = list(func_length.values())

        bars = plt.bar(function_names, lengths, color=['red' if length > 20 else 'blue' for length in lengths])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, str(yval), ha='center', va='bottom')

        plt.axhline(y=20, color='green', linestyle='--')
        plt.title('Function Lengths')
        plt.xlabel('Function Names')
        plt.ylabel('Number of Lines')
        plt.xticks(rotation=45)
        plt.tight_layout()

        output_file = os.path.join(output_dir, "histogram.png")
        plt.savefig(output_file)
        self.graph_image.append(output_file)
        plt.close()

    def create_pie_chart(self, output_dir: str):
        sizes = [max(0, value) for value in analyze.dict_problems.values()]
        labels = list(analyze.dict_problems.keys())

        if sum(sizes) == 0:
            sizes = [1]
            labels = ["No problems"]

        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'] * (len(sizes) // 4 + 1)

        plt.figure(figsize=(8, 6))
        wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                                           startangle=140, colors=colors[:len(sizes)],
                                           wedgeprops=dict(edgecolor='w', linewidth=1.5),
                                           textprops=dict(size=12))

        plt.axis('equal')
        plt.title('Distribution of Problems by Type', fontsize=16)
        plt.legend(wedges, labels, title="Types of Problems", loc="lower left", bbox_to_anchor=(-0.1111, -0.1))
        plt.setp(autotexts, size=12, weight="bold", color="white")

        output_file = os.path.join(output_dir, "pie_chart.png")
        plt.savefig(output_file)
        self.graph_image.append(output_file)
        plt.close()

    def create_bar_chart(self, count_error_for_file):
        files = list(count_error_for_file.keys())
        counts = list(count_error_for_file.values())

        plt.figure(figsize=(10, 5))
        plt.bar(files, counts, color='#ff9999', edgecolor='black')
        plt.title("Number of Issues per File")
        plt.xlabel("File Name")
        plt.ylabel("Issues Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_file = os.path.join(self.output_path, "bar_chart.png")
        plt.savefig(output_file)
        self.graph_image.append(output_file)
        plt.close()


    def create_line_chart(self):
        project_root = os.path.dirname(self.output_path)
        history_file = os.path.join(project_root, "daily_issues_history.json")

        if not os.path.exists(history_file):
            return

        with open(history_file, 'r') as f:
            history = json.load(f)

        dates = list(history.keys())
        counts = list(history.values())

        plt.figure(figsize=(10, 5))
        plt.plot(dates, counts, marker='o', linestyle='-', color='teal')
        plt.title("Issues Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Issues")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        output_file = os.path.join(self.output_path, "line_chart.png")
        plt.savefig(output_file)
        self.graph_image.append(output_file)
        plt.close()


    def save_daily_issues_history(self, total_issues: int):
        project_root = os.path.dirname(self.output_path)
        history_file = os.path.join(project_root, "daily_issues_history.json")
        today = datetime.today().strftime('%Y-%m-%d')

        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[today] = total_issues

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4)


