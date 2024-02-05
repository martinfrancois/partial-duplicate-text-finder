import os
import difflib


def calculate_similarity(text1, text2):
    d = difflib.SequenceMatcher(None, text1, text2)
    return d.ratio()


def find_partial_duplicates(folder_path, similarity_threshold=0.8):
    file_list = os.listdir(folder_path)
    duplicates = {}

    for i, file1 in enumerate(file_list):
        print("File " + str(i) + " " + file1)
        with open(os.path.join(folder_path, file1), 'r', encoding='utf-8', errors='ignore') as f1:
            try:
                text1 = f1.read()
            except UnicodeDecodeError:
                continue

            for file2 in file_list[i + 1:]:
                with open(os.path.join(folder_path, file2), 'r', encoding='utf-8', errors='ignore') as f2:
                    try:
                        text2 = f2.read()
                    except UnicodeDecodeError:
                        continue

                    similarity = calculate_similarity(text1, text2)
                    if similarity >= similarity_threshold:
                        duplicates[file1] = duplicates.get(file1, []) + [file2]

    return duplicates


if __name__ == "__main__":
    folder_path = "/home/user/docs"
    similarity_threshold = 0.8
    partial_duplicate_files = find_partial_duplicates(folder_path, similarity_threshold)

    if partial_duplicate_files:
        print("Partial duplicate files found:")
        for file, duplicates in partial_duplicate_files.items():
            print(f"{file} partial duplicates: {duplicates}")
    else:
        print("No partial duplicate files found.")
