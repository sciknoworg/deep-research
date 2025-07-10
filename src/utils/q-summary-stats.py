import csv
from collections import Counter, defaultdict

def analyze_questions(csv_path):
    with open(csv_path, mode='r', encoding='windows-1252', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        # Find all matching indices
        q_indices = [i for i, h in enumerate(headers) if h.strip() == "Your research question."]
        subdomain_indices = [i for i, h in enumerate(headers) if h.strip() == "Which fine-grained sub-domain or sub-discipline in Ecology would you say is the context to your research question?"]
        purpose_indices = [i for i, h in enumerate(headers) if h.strip() == "What is the purpose of your question?"]

        if not (q_indices and subdomain_indices and purpose_indices):
            print("❌ Required columns not found.")
            return

        question_entries = []
        subdomains = Counter()
        purposes = Counter()

        for row in reader:
            for qi, si, pi in zip(q_indices, subdomain_indices, purpose_indices):
                if qi < len(row):
                    question = row[qi].strip()
                    subdomain = row[si].strip() if si < len(row) else "N/A"
                    purpose = row[pi].strip() if pi < len(row) else "N/A"
                    if question:
                        question_entries.append((question, subdomain, purpose))
                        subdomains[subdomain] += 1
                        purposes[purpose] += 1

    print("📊 Summary Statistics")
    print("--------------------")
    print(f"Total valid questions: {len(question_entries)}\n")

    print("Top Sub-domains:")
    for sub, count in subdomains.most_common():
        print(f"  - {sub}: {count}")

    print("\nTop Purposes:")
    for purp, count in purposes.most_common():
        print(f"  - {purp}: {count}")

if __name__ == "__main__":
    csv_file = input("📄 Enter path to CSV file: ").strip()
    analyze_questions(csv_file)
