import csv

def extract_questions(csv_path, output_txt_path):
    with open(csv_path, mode='r', encoding='windows-1252', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        question_indices = [i for i, h in enumerate(headers) if h.strip() == "Your research question."]

        questions = []
        for row in reader:
            for index in question_indices:
                if index < len(row):
                    value = row[index].strip()
                    if value:
                        questions.append(value)

    with open(output_txt_path, mode='w', encoding='utf-8') as f:
        for q in questions:
            f.write(q + '\n')

    print(f"✅ Extracted {len(questions)} questions to: {output_txt_path}")

if __name__ == "__main__":
    csv_file = input("📄 Enter path to CSV file: ").strip()
    txt_file = input("📝 Enter path for output TXT file: ").strip()
    extract_questions(csv_file, txt_file)
