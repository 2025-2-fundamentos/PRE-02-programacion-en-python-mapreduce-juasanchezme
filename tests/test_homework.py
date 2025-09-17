import os
import shutil
import time
from collections import defaultdict
from toolz.itertoolz import concat
import re


# Ruta base (sube un nivel desde el script actual)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILES_DIR = os.path.join(BASE_DIR, "files")


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    input_dir = os.path.join(FILES_DIR, "input")
    raw_dir = os.path.join(FILES_DIR, "raw")

    os.makedirs(input_dir, exist_ok=True)

    raw_files = os.listdir(raw_dir)
    for i in range(n):
        for f in raw_files:
            src = os.path.join(raw_dir, f)
            dst = os.path.join(input_dir, f"copy_{i}_{f}")
            shutil.copy(src, dst)


def load_input(input_directory):
    """Read all files in input directory and return lines"""
    sequence = []
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            sequence.extend(f.readlines())
    return sequence




def preprocess_line(x):
    """Preprocess the line x"""
    # Minúsculas y quitar caracteres que no sean letras/números/espacios
    x = x.strip().lower()
    x = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", x)  # conserva letras y números
    return x


def map_line(x):
    """Map line into (word, 1) pairs"""
    words = preprocess_line(x).split()
    return [(w, 1) for w in words if w]


def mapper(sequence):
    """Apply map_line to each element"""
    return list(concat(map(map_line, sequence)))


def shuffle_and_sort(sequence):
    """Group values by key"""
    grouped = defaultdict(list)
    for k, v in sequence:
        grouped[k].append(v)
    return grouped.items()


def compute_sum_by_group(group):
    """Compute sum of values for a given key"""
    key, values = group
    return key, sum(values)


def reducer(sequence):
    """Reduce grouped key-value pairs"""
    return [compute_sum_by_group(g) for g in sequence]


def create_directory(directory):
    """Create Output Directory"""
    os.makedirs(directory, exist_ok=True)


def save_output(output_directory, sequence):
    """Save Output"""
    filepath = os.path.join(output_directory, "part-00000")
    with open(filepath, "w", encoding="utf-8") as f:
        for k, v in sorted(sequence, key=lambda x: -x[1]):
            f.write(f"{k}\t{v}\n")


def create_marker(output_directory):
    """Create Marker"""
    filepath = os.path.join(output_directory, "_SUCCESS")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Job completed successfully.\n")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":
    input_dir = os.path.join(FILES_DIR, "input")
    output_dir = os.path.join(FILES_DIR, "output")

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(input_dir, output_dir)

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")