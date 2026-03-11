# Dataset Splitter Script

A simple and reliable Python tool for splitting image classification datasets into **train**, **validation**, and **test** sets.

This script is part of the **AI Computer Vision Dataset Toolkit** and is designed to make preparing datasets for machine learning models fast and easy.

It works with datasets organized by class folders and automatically generates a clean dataset structure ready for training.

---

# Features

- Splits datasets into **train / val / test**
- Preserves class folder structure
- Configurable split ratios
- Reproducible splits with random seed
- Copy or move files
- Handles duplicate filenames safely
- Optional nested folder scanning
- Generates a `labels.csv` file
- Prints dataset statistics summary

No external Python libraries required.

---

# Dataset Structure (Input)

The script expects your dataset to be organized into **class folders** like this:

- dataset/
  - cat/ 
    - img1.jpg
    - img2.jpg
  - dog/
    - img3.jpg
    - img4.jpg
  - bird/
    - img5.jpg


Each folder name becomes the **class label**.

---

# Output Structure

After running the script, the dataset will look like this:

- output_dataset/
  - train/ 
    - cat/
    - dog/
    - bird/
  - val/
    - cat/ 
    - dog/ 
    - bird/ 
  - test/ 
    - cat/ 
    - dog/ 
    - bird/
  - labels.csv


---

# Installation

This script requires **Python 3.8+**.

Check your Python version:

```bash
python --version
```

---

# Example Usage

```bash
python split_dataset.py ^
--input "C:\datasets\images" ^
--output "C:\datasets\split_dataset" ^
--train 0.8 --val 0.1 --test 0.1
```
This is an example command to run the script in Windows Command Prompt. The user will need to update
the input and output directories in the command's arguements. The user can also tweak the train, val, and test
split ratios. The ratios used in the example are 80% train, 10% validation, and 10% test.

---

# Arguements

| Argument                 | Description                                 |
| ------------------------ | ------------------------------------------- |
| `--input`                | Input dataset folder                        |
| `--output`               | Output dataset folder                       |
| `--train`                | Training split ratio                        |
| `--val`                  | Validation split ratio                      |
| `--test`                 | Test split ratio                            |
| `--seed`                 | Random seed for reproducibility             |
| `--mode`                 | `copy` or `move` files                      |
| `--min-images-per-class` | Minimum number of images required per class |
| `--flatten`              | Scan nested subfolders for images           |

---

# Generated labels.csv

The script also generates a labels.csv file to help track each run of the script. The labels.csv file
will be formatted like this:  
split,class_name,filename,relative_path  
train,cat,img001.jpg,train/cat/img001.jpg  
val,dog,img012.jpg,val/dog/img012.jpg  
test,bird,img021.jpg,test/bird/img021.jpg  

This can be useful for:
- dataset analysis  
- loading datasets in pandas  
- ML pipelines  
- dataset documentation

---

# Supported Image Formats

- jpg
- jpeg
- png
- bmp
- tif
- tiff
- webp

---

# License

This script is part of the **AI Computer Vision Dataset Toolkit**.

You may use it for personal and commercial projects.

Redistribution or resale of the script alone is not permitted without permission.

---

# Author

Created for the **AI Computer Vision Dataset Toolkit**.

Designed to help simplify dataset preparation for machine learning and computer vision workflows.