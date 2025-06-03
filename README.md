# CS50P-FinalProject

## BASIC MATCHING RESUME MODEL

#### Video Demo:  <[URL HERE](https://youtu.be/NTB5l9Hl7XQ)>

#### Description:
This Python-based resume matching tool allows users to compare resumes against a job description using NLP techniques like CountVectorizer and cosine similarity.
The tool extracts emails, calculates a similarity score, and generates a sorted list of applicants in a CSV file based on the highest match. It uses pandas for data handling, and scikit-learn for NLP processing.

## Features:
- Indexing each resume file to prevent name collisions in case multiple files have identical names within   the same folder
- New files can be added anytime, with the system re-evaluating and re-sorting all files (old files and new files) automatically
- Extracts emails from resumes.
- Calculates a similarity score between resumes and job description.
- Sorts and saves the shortlisted applicants in a CSV file.

## How to use:
- You should run 'pip install' to install pandas, scikit-learn, numpy, pypdf, beforhand.
- Provide a job description and a folder of received resumes.
- It processes each resume individually, comparing its content against the job description using NLP techniques.
- A relevance score is assigned to each resume based on similarity.
- The model also extracts the applicant’s email address from each resume.
- Results, including scores and emails, are stored in a pandas DataFrame, sorted in descending order by score for easy review and further analysis using pandas or similar data analysis libraries.

## CSV output
- name,score,email
- resume_folder_name/001,66.44,saralee@neuecon.edu
- resume_folder_name/002,63.44,jstein.ai@gmail.com
- resume_folder_name/000,61.57,alexnguyen@uni.edu


## Technologies Used:
- Python
- pandas
- scikit-learn
- Regular Expressions (re)

## Note
This model matches words to words but does not comprehend the meaning of the words. Therefore, it is advisable to manually review the results








