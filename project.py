import os
import pandas as pd
from pypdf import PdfReader
from sys import exit
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def main():
    results = []
    print("Only support file with '.txt' of '.pdf' extensions")
    jd = jd_input()
    cv_s = list(cv_inputs())

    if cv_s is None or (jd is None or jd == ""):
        print("File/Folder is not found")
        exit(1)

    for name, cv in cv_s:
        results += [{"name": name, "score": c_vector(jd, cv)}]

    print(output(results, cv_s))


# get a shorted list


def output(results_copy, cvs_copy):
    """
    Matching scores and email addresses are stored in a DataFrame.
    Resumes with a specific filename are added once to the output DataFrame,
    which is then sorted in descending order by the matching score.

    """
    applicants = []
    for name, cv in cvs_copy:
        pattern = r"(?P<e>[a-zA-Z0-9._%+\.]+@([a-zA-Z0-9.]+\.)+[\w]{2,})"
        extract = re.search(pattern, cv)
        email = extract.group("e")

        for result in results_copy:
            if name == result["name"]:
                applicants.append({
                    "name": name,
                    "score": f"{result['score']:.02f}",
                    "email": email if email else "N/A"
                })

    return data_f(applicants)


def data_f(lit):
    """ Create DataFrame and wirte extracted data to a csv file """
    df = pd.DataFrame(lit)

    if os.path.exists("shorted_list.csv"):
        # read exsiting data
        try:
            df_existing = pd.read_csv("shorted_list.csv")
            # add new data to exsiting data
            df_new = pd.concat([df_existing, df], ignore_index=True)
        except pd.errors.EmptyDataError:
            df_new = df

        df_new["score"] = df_new["score"].astype(float)
        df = df_new

    df = df.sort_values(by="score", ascending=False, ignore_index=True)
    df.to_csv("shorted_list.csv", index=False)

    return df


# get job description


def jd_input():
    jd = input("What is the job description? ")
    if jd is None:
        return
    if not extension_check(jd):
        return
    try:
        text = text_extraction(jd)
    except FileNotFoundError:
        return
    return text

# get resume


def cv_inputs():
    """
    Extracts resumes from the input folder,
    formatting each resume filename to a numerical format to avoid collisions.
    Returns one resume at a time for comparison against the job description.

    """
    jds = []


    while True:
        folder = input("I help with resume evaluating! ")
        try:
            jds = [jd for jd in os.listdir(folder) if os.path.isfile(os.path.join(folder, jd))
                   and extension_check(jd)]
        except FileNotFoundError:
            print("Invalid folder")
            continue
        else:
            if len(jds) >= 1:
                break
            continue

    indexing_jds = name_transform(folder, jds)
    return cv_return(indexing_jds)



def cv_return(jds_lit):
    """ This is a generator. It generates one resume at a time to compare with the job description """
    for jd in jds_lit:
        try:
            text = text_extraction(jd)
        except FileNotFoundError:
            return
        name = jd.split(".")[0]
        yield (name, text)




def name_transform(folder, lit):
    """ This name_transform function trace back to the file to where it is
    in the folder and form that filename to digits"""


    indexing_jds = []
    for i, jd in enumerate(sorted(lit)):  # enumarate gets both index and the element inside jds
        if not name_formatted(i, jd):
            ext = jd.split(".")[-1]
            index = str(i)
            newname = f"{index.zfill(3)}.{ext}" #ADJUSTING HERE IF THERE IS MORE THAN 999
            old_path = os.path.join(folder, jd)
            new_path = os.path.join(folder, newname)

            try:
                os.rename(old_path, new_path)
                indexing_jds.append(new_path)
            except FileNotFoundError:
                print(f"Having problem import {jd}")
                pass
    return indexing_jds



# to only formate new file, no re-formatted
def name_formatted(n, name):
    """
    Checks if the resume filename is formatted as a number by comparing it with its position in the resume list.
    If the filename's number can be converted to an integer and matches its index in the list,
    it is considered correctly formatted.
    If not, the filename will be formatted, compared to the job description, and then added to the output DataFrame.

    """
    if name.endswith(".pdf"):
        name = name.replace(".pdf", "")
    else:
        name = name.replace(".txt", "")
    try:
        return int(name) == n
    except ValueError:
        return False

# check for valid extension


def extension_check(s):
    return s.strip().endswith((".txt", ".pdf"))


# read the input file

def text_extraction(s):

    """
    Reads the input file. This function expects either a .pdf or .txt file extension,
    but it works best with PDFs where the text is not overlayed.
    The function returns a long string, which can be used later for cosine similarity calculations.

    """

    text = ""
    text_li = []
    if s.endswith(".pdf"):
        try:
            reader = PdfReader(s)
        except ValueError:
            return
        for page in reader.pages:
            text_li.append(page.extract_text().strip().lower())

    else:
        try:
            with open(s, "r") as file:
                lines = file.readlines()
        except ValueError:
            return
        for line in lines:
            text_li.append(line.strip().lower())

    text = " ".join(text_li)

    if text is None:
        return
    return text


# vectorize important words


def c_vector(jd, cv):
    """
    Takes two strings as input, identifies matching words between them,
    and calculates a score based on the number of matching words.

    """

    vectorizer = CountVectorizer(stop_words="english")
    try:
        jd_vec, cv_vec = vectorizer.fit_transform([jd, cv])
    except ValueError:
        return 0.0
    return cosine_similarity(jd_vec, cv_vec)[0][0] * 100


if __name__ == "__main__":
    main()
