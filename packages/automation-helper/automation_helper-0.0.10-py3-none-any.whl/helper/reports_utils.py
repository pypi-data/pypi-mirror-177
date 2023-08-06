import csv
import os
import datetime
import shutil
import pandas as pd


def writeOutCSV(output_filename_local, dict_list_local):
    if output_filename_local.split("\\")[-1] not in os.listdir("\\".join(output_filename_local.split("\\")[:-1])):
        with open(output_filename_local, "w", newline='') as fh:
            csv_writer = csv.DictWriter(fh, dict_list_local[0].keys())
            csv_writer.writeheader()
    with open(output_filename_local, "a+", newline='') as fh:
        csv_writer = csv.DictWriter(fh, dict_list_local[0].keys())
        csv_writer.writerows(dict_list_local)


def addDateToString(string_local, date=None):
    if date is not None:
        string_local = string_local.replace('--DATE--', date)
    else:
        string_local = string_local.replace('--DATE--', datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    return string_local.encode(encoding='utf-8-sig').decode(encoding='utf-8-sig')


def createFolderFromAbspath(relative_path, n_backs):

    """

    USE CASES:
    :relative_path: "Folder1", n_backs = 0:
       :return Code will generate a Folder1 inside os.path.abspath("")
    :relative_path: "Folder1\\Folder2", n_backs = 0:
       :return Code will generate a Folder1\\Folder2 inside os.path.abspath("")
    :relative_path: "Folder1\\Folder2\\Folder3", n_backs = 2:
       :return will generate a Folder1\\Folder2\\Folder3 inside two parent paths of os.path.abspath("")
    In all cases the fcn returns the lowest (most child) path.
    """

    folders_to_create = relative_path.split("\\")
    if n_backs > 0:
        start_path = "\\".join(os.path.abspath("").split("\\")[:-n_backs])
    else:
        start_path = os.path.abspath("")
    for folder_to_create in folders_to_create:
        path_previous_to_folder = "\\".join([start_path] + folders_to_create[:folders_to_create.index(folder_to_create)])
        folder_to_create_full_path = "\\".join([path_previous_to_folder, folder_to_create])
        if folder_to_create not in os.listdir(path_previous_to_folder):
            os.mkdir(folder_to_create_full_path)
    return "\\".join([start_path, relative_path])


def generateStrDatesFromRange(str_in, sep):
    if sep not in str_in:
        range_out = [str_in]
    else:
        start, end = str_in.split(sep)
        dates_dt = pd.date_range(start, end).tolist()
        range_out = [date_dt.strftime("%Y-%m-%d") for date_dt in dates_dt]
    return range_out


def findFilesWithDate(path_files, date_in, ext):
    files_in_path = os.listdir(path_files)
    files_in_path_ext = [file for file in files_in_path if "." in file and ext == file.split(".")[1]]
    files_in_date = [f"{path_files}\\{file}" for file in files_in_path_ext if date_in in file]
    return files_in_date


def extendPath(path_in, str_to_replace_in=None):

    """
    RECIEVES path_in = "str_to_replace\\..." and merges it to C:\\Users\\User
    IF str_to_replace is None, assumes beginning
    """

    base_path = "\\".join(os.path.abspath("").split("\\")[0:3])
    if str_to_replace_in is None:
        path_out = base_path + "\\" + path_in
    else:
        path_out = path_in.replace(str_to_replace_in, base_path)
    return path_out


def invertJson(dict_in):

    """
    RECEIVE DICT AS:

    {
        "KEY_1": "VAL_1",
        "KEY_2": "VAL_2"
    }
    :AND RETURN:
    {
        "VAL_1": "KEY_1",
        "VAL_2": "KEY_2"
    }
    """

    dict_out = {}
    for key in dict_in:
        value = dict_in[key]
        dict_out[value] = key
    return dict_out


def dfHandler(df_in, df_appended_in):
    if df_in.empty:
        df_appended = df_in
    else:
        df_appended = pd.concat([df_appended_in, df_in], ignore_index=True)
    return df_appended


def generateWeekDatesData(date_in="", format_in="%Y-%m-%d"):
    if date_in == "":
        date_in = datetime.datetime.today().strftime(format_in)
    today = datetime.datetime.strptime(date_in, format_in)
    this_monday = (today - datetime.timedelta(days=today.weekday()))
    this_tuesday = this_monday + datetime.timedelta(days=1)
    this_wednesday = this_monday + datetime.timedelta(days=2)
    this_thursday = this_monday + datetime.timedelta(days=3)
    this_friday = this_monday + datetime.timedelta(days=4)
    this_saturday = this_monday + datetime.timedelta(days=5)
    this_sunday = this_monday + datetime.timedelta(days=6)
    dates_list_dt = [this_monday, this_tuesday, this_wednesday, this_thursday, this_friday, this_saturday, this_sunday]
    dates_list_str = [date.strftime(format_in) for date in dates_list_dt]
    dict_out = {
        "STR": dates_list_str,
        "DT": dates_list_dt
    }
    return dict_out


def goBackNPaths(path_in, n):
    for i in range(n):
        path_in = os.path.split(path_in)[0]
    return path_in


def moveToOutputFolder(file_name, output_folder):
    src_file_path = os.path.join(os.path.abspath(""), file_name)
    shutil.move(src_file_path, output_folder)
    return output_folder + os.path.basename(src_file_path)


def deDuplicate(path_in):
    csv_read = pd.read_csv(path_in, encoding='iso-8859-1')
    csv_read = csv_read.drop_duplicates()
    csv_read.to_csv(path_in, encoding='iso-8859-1', index=False)
