import ast
import os
import re
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from app.models import *
from config import settings
import mca
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np
import uuid


def index(request):
    return render(request, "app/index.html")


def result_technique(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]
        techniques = save_file_and_get_related_techniques(uploaded_file)
        external_ids_str = extract_unique_external_ids(techniques)
        matrix_data = get_matrix_data()

        context = {
            "techniques": techniques,
            "t_external_id": external_ids_str,
            **matrix_data
        }
        return render(request, "app/result/technique.html", context)
    return redirect("index")


def result_similarity(request):
    if request.method == "POST":
        print(request.FILES.values())
        file_data, filenames, technique_external_ids_str = process_files(request.FILES.values())
        df = create_dataframe(file_data)
        similarities = mca_analysis(df)
        matrix_data = get_matrix_data()

        context = {
            "file_data": file_data,
            "similarities": similarities,
            "filenames": filenames,
            "t_external_ids_str": technique_external_ids_str,
            **matrix_data
        }
        return render(request, "app/result/similarity.html", context)
    return redirect("index")

"""
def get_related_techniques(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    technique_ids = set()

    for event in root.iter("{http://schemas.microsoft.com/win/2004/08/events/event}Event"):
        data_elements = event.findall("{http://schemas.microsoft.com/win/2004/08/events/event}EventData/{http://schemas.microsoft.com/win/2004/08/events/event}Data")

        for data_element in data_elements:
            if data_element.attrib["Name"] != "Image": continue

            image_name = data_element.text.split("\\")[-1].split(".")[0]

            matching_commands = Commands.objects.using("attack").filter(command__icontains=image_name).all()

            technique_ids.update(command.technique_id for command in matching_commands)

    related_techniques = Techniques.objects.using("attack").filter(id__in=list(technique_ids))
    return related_techniques
"""

def get_related_techniques(csv_file):
    with open(os.path.join("./", 'replace_rule.txt'), 'r') as f:
        dictionary_string = f.read()
        replace_rule = ast.literal_eval(dictionary_string)

    special_techniques=[]
    commands_list=[]

    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f: # f: ログ
            if "CommandLine: " in line and "ParentCommandLine: " not in line:
                line = line.replace("CommandLine: ", "")

                #T1059 is the most frequently used technique
                """
                if "powershell.exe" in line or "cmd" in line:
                    line=line.replace("powershell.exe","")
                    if "T1059" not in special_techniques:
                        special_techniques.append("T1059")
                """
                for pattern, replacement in replace_rule.items():
                    line = re.sub(pattern, replacement, line)

                if line not in commands_list:
                    commands_list.append(line.strip())
    technique_id_set = set()
    for command in commands_list:
        match_records = Commands.objects.using("attack").filter(command__icontains=command).all()
        for record in match_records:
            technique_id_set.add(record.technique_id)
    
    results=Techniques.objects.using("attack").filter(id__in=list(technique_id_set))
    return results


def save_file_and_get_related_techniques(file):
    storage = FileSystemStorage()
    filename = storage.save(f"{uuid.uuid4()}.csv", file)
    """
    filename = storage.save(f"{uuid.uuid4()}.xml", file)
    with storage.open(filename, "a") as f:
        f.write("</Events>")
    """
    file_path = storage.path(filename)
    techniques = get_related_techniques(file_path)
    storage = FileSystemStorage()
    storage.delete(file_path)
    return techniques

def process_files(files):
    file_data = []
    filenames = []
    technique_external_ids_str = []

    for file in files:
        techniques = save_file_and_get_related_techniques(file)
        file_data.append({file.name: techniques})
        filenames.append(file.name)
        technique_external_ids_str.append(extract_unique_external_ids(techniques))

    return file_data, filenames, technique_external_ids_str


def extract_unique_external_ids(techniques):
    external_ids = [technique["external_id"].split(".")[0] for technique in techniques.values("external_id")]
    unique_external_ids = set(external_ids)
    external_id_str = ", ".join("." + external_id for external_id in unique_external_ids)
    return external_id_str


def create_dataframe(file_list):
    all_techniques = set()

    for file in file_list:
        for techniques in file.values():
            all_techniques.update(techniques)

    all_techniques_list = list(all_techniques)

    truth_lists = []
    filenames = []

    for file in file_list:
        for filename, techniques in file.items():
            filenames.append(filename)
            truth_list = [1 if technique in techniques else 0 for technique in all_techniques_list]
            truth_lists.append(truth_list)

    df = pd.DataFrame(truth_lists, index=filenames, columns=all_techniques_list)
    return df


def mca_analysis(df_truth_table):
    mca_counts = mca.MCA(df_truth_table, benzecri=False)
    row_coords = mca_counts.fs_r(1)

    labels = df_truth_table.index.values

    results_mca = [[label, x, y] for label, x, y in zip(labels, row_coords[:, 0], row_coords[:, 1])]
    
    x_coords = [result[1] for result in results_mca]
    y_coords = [result[2] for result in results_mca]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    normalized_results = [{result[0]: [(result[1] - x_min) / (x_max - x_min),
                                        (result[2] - y_min) / (y_max - y_min)]} for result in results_mca]

    similarities = calculate_similarities(normalized_results)

    return similarities


def similarity_percentage(coord1, coord2):
    distance = np.linalg.norm(coord1 - coord2)
    max_distance = np.sqrt(2)

    similarity = 1 - (distance / max_distance)
    similarity_percentage = similarity * 100

    return similarity_percentage


def calculate_similarities(input_data):
    coordinates = np.array([list(item.values())[0] for item in input_data])
    labels = [list(item.keys())[0] for item in input_data]

    first_elem_coord = coordinates[0]

    similarities = {}
    for i, coord in enumerate(coordinates):
        if i != 0:
            similarity = similarity_percentage(first_elem_coord, coord)
            rounded_similarity = round(similarity, 1)
            similarities[labels[i]] = rounded_similarity

    return similarities


def get_matrix_data():
    reasons = Reasons.objects.using("attack").select_related(
        "tactic",
        "technique"
    ).filter(
        technique__is_subtechnique=False
    ).values(
        "tactic__external_id",
        "technique__external_id",
        "technique__name"
    ).order_by("technique__name")

    tactic_external_ids = [
        "TA0043", "TA0042", "TA0001", "TA0002", "TA0003", "TA0004",
        "TA0005", "TA0006", "TA0007", "TA0008", "TA0009", "TA0011",
        "TA0010", "TA0040"]

    grouped_reasons = {tactic_id: [] for tactic_id in tactic_external_ids}
    for reason in reasons:
        tactic_external_id = reason["tactic__external_id"]
        if tactic_external_id in grouped_reasons:
            grouped_reasons[tactic_external_id].append(reason)
    return grouped_reasons

