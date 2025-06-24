from fastapi import FastAPI, UploadFile, File
from zipfile import ZipFile
from io import BytesIO

from Graph import Graph
from Alert import Alert

app = FastAPI()


@app.post("/analyze")
async def graph_analysis(file: UploadFile = File(...)):
    graph = Graph(file)
    return graph.get_graphs_images()


@app.post("/alert")
async def alert_analysis(file: UploadFile):
    contents = await file.read()
    zip_file = BytesIO(contents)
    alerts = []

    with ZipFile(zip_file, 'r') as z:
        print("Zip file opened successfully. in alert")
        for file_info in z.infolist():
            print(f"Found file: {file_info.filename}")
            if file_info.filename.endswith(".py"):
                with z.open(file_info) as f:
                    alert = Alert(f, file_info.filename)
                    alerts.extend(alert.get_alerts())

    return alerts
