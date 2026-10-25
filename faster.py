import os
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor


def calculate_similarity(text1, text2, shingle_length=10):
    m, n = len(text1), len(text2)
    max_similarity = 0

    for i in range(m - shingle_length + 1):
        for j in range(n - shingle_length + 1):
            shingle1 = text1[i:i + shingle_length]
            shingle2 = text2[j:j + shingle_length]

            d = SequenceMatcher(None, shingle1, shingle2)
            similarity = d.ratio()

            if similarity > max_similarity:
                max_similarity = similarity

    return max_similarity


def process_files(file_list, folder_path, similarity_threshold, max_file_size):
    duplicates = {}

    for i, file1 in enumerate(file_list):
        file1_path = os.path.join(folder_path, file1)
        file1_size = os.path.getsize(file1_path)

        if file1_size > max_file_size:
            continue

        with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
            try:
                text1 = f1.read()
            except UnicodeDecodeError:
                continue

            for file2 in file_list[i + 1:]:
                file2_path = os.path.join(folder_path, file2)
                file2_size = os.path.getsize(file2_path)

                if file2_size > max_file_size:
                    continue

                with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
                    try:
                        text2 = f2.read()
                    except UnicodeDecodeError:
                        continue

                    similarity = calculate_similarity(text1, text2)

                    if similarity >= similarity_threshold:
                        duplicates[file1] = duplicates.get(file1, []) + [file2]

    return duplicates


def find_partial_duplicates(folder_path, similarity_threshold=0.8, max_file_size=10 * 1024 * 1024):
    file_list = os.listdir(folder_path)
    small_files = file_list  # In this approach, we don't skip large files

    with ThreadPoolExecutor() as executor:
        chunk_size = 10  # Adjust this based on the number of files and system resources
        chunked_files = [small_files[i:i + chunk_size] for i in range(0, len(small_files), chunk_size)]
        futures = [executor.submit(process_files, chunk, folder_path, similarity_threshold, max_file_size)
                   for chunk in chunked_files]

        duplicates = {}
        for future in futures:
            result = future.result()
            duplicates.update(result)

    return duplicates


if __name__ == "__main__":
    folder_path = "/home/user/docs"
    similarity_threshold = 0.8
    max_file_size = 10 * 1024 * 1024
    partial_duplicate_files = find_partial_duplicates(folder_path, similarity_threshold, max_file_size)

    if partial_duplicate_files:
        print("Partial duplicate files found:")
        for file, duplicates in partial_duplicate_files.items():
            print(f"{file} partial duplicates: {duplicates}")
    else:
        print("No partial duplicate files found.")
