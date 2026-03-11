#!/usr/bin/env python3
"""
split_dataset.py

Split an image classification dataset organized like:

input_dir/
    class_a/
        img1.jpg
        img2.jpg
    class_b/
        img3.jpg
        img4.jpg

Into:

output_dir/
    train/
        class_a/
        class_b/
    val/
        class_a/
        class_b/
    test/
        class_a/
        class_b/
    labels.csv

Features:
- configurable train/val/test ratios
- reproducible random seed
- copy or move files
- optional minimum images check
- labels.csv generation
- summary output

Usage example:
python split_dataset.py ^
    --input "C:\\datasets\\my_data" ^
    --output "C:\\datasets\\my_data_split" ^
    --train 0.8 --val 0.1 --test 0.1 ^
    --mode copy
"""

from __future__ import annotations

import argparse
import csv
import random
import shutil
from pathlib import Path
from typing import List, Tuple

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split an image classification dataset into train/val/test folders."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Input dataset folder containing class subfolders."
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output folder for the split dataset."
    )
    parser.add_argument(
        "--train",
        type=float,
        default=0.8,
        help="Train split ratio. Default: 0.8"
    )
    parser.add_argument(
        "--val",
        type=float,
        default=0.1,
        help="Validation split ratio. Default: 0.1"
    )
    parser.add_argument(
        "--test",
        type=float,
        default=0.1,
        help="Test split ratio. Default: 0.1"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible splits. Default: 42"
    )
    parser.add_argument(
        "--mode",
        choices=["copy", "move"],
        default="copy",
        help="Whether to copy or move files. Default: copy"
    )
    parser.add_argument(
        "--min-images-per-class",
        type=int,
        default=1,
        help="Minimum number of images required in a class folder. Default: 1"
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="If set, include images from nested subfolders inside each class folder."
    )
    return parser.parse_args()


def validate_ratios(train: float, val: float, test: float) -> None:
    total = train + val + test
    if abs(total - 1.0) > 1e-8:
        raise ValueError(
            f"Train/val/test ratios must sum to 1.0, but got {total:.6f}"
        )


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def get_class_directories(input_dir: Path) -> List[Path]:
    return sorted([p for p in input_dir.iterdir() if p.is_dir()])


def get_images_for_class(class_dir: Path, flatten: bool) -> List[Path]:
    if flatten:
        files = [p for p in class_dir.rglob("*") if is_image_file(p)]
    else:
        files = [p for p in class_dir.iterdir() if is_image_file(p)]
    return sorted(files)


def calculate_split_counts(
    n: int, train_ratio: float, val_ratio: float, test_ratio: float
) -> Tuple[int, int, int]:
    train_count = int(n * train_ratio)
    val_count = int(n * val_ratio)
    test_count = n - train_count - val_count

    # Ensure no negative counts due to weird edge cases
    if test_count < 0:
        test_count = 0

    return train_count, val_count, test_count


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def transfer_file(src: Path, dst: Path, mode: str) -> None:
    ensure_dir(dst.parent)
    if mode == "copy":
        shutil.copy2(src, dst)
    elif mode == "move":
        shutil.move(str(src), str(dst))
    else:
        raise ValueError(f"Unsupported mode: {mode}")


def make_unique_destination(dst: Path) -> Path:
    """
    Avoid overwriting if duplicate filenames exist within the same class/split.
    """
    if not dst.exists():
        return dst

    stem = dst.stem
    suffix = dst.suffix
    parent = dst.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def write_labels_csv(rows: List[dict], output_csv: Path) -> None:
    ensure_dir(output_csv.parent)
    fieldnames = ["split", "class_name", "filename", "relative_path"]

    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()

    validate_ratios(args.train, args.val, args.test)

    input_dir: Path = args.input
    output_dir: Path = args.output

    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist or is not a folder: {input_dir}")

    if output_dir.resolve() == input_dir.resolve():
        raise ValueError("Input and output directories must be different.")

    random.seed(args.seed)

    class_dirs = get_class_directories(input_dir)
    if not class_dirs:
        raise ValueError(f"No class subfolders found in input directory: {input_dir}")

    summary = []
    labels_rows = []

    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Mode:   {args.mode}")
    print(f"Seed:   {args.seed}")
    print("")

    total_images_all = 0

    for class_dir in class_dirs:
        class_name = class_dir.name
        images = get_images_for_class(class_dir, args.flatten)

        if len(images) < args.min_images_per_class:
            print(
                f"Skipping class '{class_name}' "
                f"(found {len(images)} images, minimum is {args.min_images_per_class})"
            )
            continue

        random.shuffle(images)

        n_total = len(images)
        n_train, n_val, n_test = calculate_split_counts(
            n_total, args.train, args.val, args.test
        )

        train_files = images[:n_train]
        val_files = images[n_train:n_train + n_val]
        test_files = images[n_train + n_val:]

        split_map = {
            "train": train_files,
            "val": val_files,
            "test": test_files,
        }

        for split_name, file_list in split_map.items():
            for src in file_list:
                dst = output_dir / split_name / class_name / src.name
                dst = make_unique_destination(dst)
                transfer_file(src, dst, args.mode)

                rel_path = dst.relative_to(output_dir).as_posix()
                labels_rows.append(
                    {
                        "split": split_name,
                        "class_name": class_name,
                        "filename": dst.name,
                        "relative_path": rel_path,
                    }
                )

        summary.append(
            {
                "class_name": class_name,
                "total": n_total,
                "train": len(train_files),
                "val": len(val_files),
                "test": len(test_files),
            }
        )

        total_images_all += n_total

    if not summary:
        raise ValueError("No valid class folders were processed.")

    labels_csv_path = output_dir / "labels.csv"
    write_labels_csv(labels_rows, labels_csv_path)

    print("Split complete.\n")
    print("Per-class summary:")
    print("-" * 60)
    for row in summary:
        print(
            f"{row['class_name']:<25} "
            f"total={row['total']:<6} "
            f"train={row['train']:<6} "
            f"val={row['val']:<6} "
            f"test={row['test']:<6}"
        )

    print("-" * 60)
    print(f"Classes processed: {len(summary)}")
    print(f"Total images:      {total_images_all}")
    print(f"labels.csv:        {labels_csv_path}")


if __name__ == "__main__":
    main()