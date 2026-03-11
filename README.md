# AI Dataset Toolkit (Free Trial)

A lightweight **Python dataset splitter for machine learning datasets**. This tool quickly splits an image dataset into **train, validation, and test folders**, making it easy to prepare datasets for **computer vision training workflows** such as **YOLO, COCO, and image classification models**.

This repository contains the **free trial script** from the larger **AI Dataset Toolkit**.

---

# Why This Tool Exists

Preparing datasets is one of the most tedious steps in a machine learning workflow. Many developers search for ways to:

* split datasets into train validation test sets
* organize image datasets for machine learning
* prepare datasets for YOLO training
* create train validation splits for computer vision

The **dataset_splitter.py** script automates this process and creates a clean dataset structure ready for training.

---

# Features

* Split image datasets into **train / validation / test sets**
* Randomized dataset splitting
* Works with **image classification datasets**
* Compatible with **computer vision pipelines**
* Simple Python CLI tool
* Extremely lightweight (no heavy dependencies)

---

# Example Dataset Structure

Before splitting:

```
dataset/
  class1/
    img1.jpg
    img2.jpg
  class2/
    img3.jpg
    img4.jpg
```

After running the dataset splitter:

```
dataset_split/
  train/
  val/
  test/
```

Each directory will contain properly distributed images from the original dataset.

---

# Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/AIComputerVisionDatasetToolkit-Trial
cd AIComputerVisionDatasetToolkit-Trial
```

Ensure you have Python installed:

```
python --version
```

Python **3.8+** is recommended.

---

# Usage

Run the dataset splitter from the command line:

```
python dataset_splitter.py --input dataset/ --output dataset_split/
```

Example output:

```
Splitting dataset...
Train: 8000 images
Validation: 1000 images
Test: 1000 images
Done.
```

This command will automatically split your dataset into **training, validation, and test sets for machine learning training**.

---

# Common Use Cases

This script is useful if you need to:

* split a dataset for **machine learning training**
* prepare a dataset for **YOLO training**
* create **train validation test splits for computer vision**
* organize large **image classification datasets**
* quickly generate a **dataset split for deep learning experiments**

Many ML engineers use similar scripts when preparing datasets for frameworks such as:

* PyTorch
* TensorFlow
* Ultralytics YOLO
* Detectron2

---

# Included in This Free Trial

This repository includes:

```
dataset_splitter.py
```

The full toolkit includes additional dataset preparation tools.

---

# Full AI Dataset Toolkit

The **full version of the AI Dataset Toolkit** includes additional scripts designed to clean and prepare computer vision datasets:

✔ Dataset Splitter
✔ Duplicate Image Remover
✔ Dataset Validator

These tools help automate **dataset preparation for machine learning and computer vision workflows**.

Get the full toolkit here:

👉 [**Gumroad Link**](https://nickdelago.gumroad.com/l/AIComputerVisionDatasetToolkit)

---

# Future Tools Planned

The full toolkit may expand with additional utilities such as:

* COCO to YOLO annotation converter
* dataset balancing tools
* image dataset augmentation
* dataset quality reports

These tools are designed to simplify **dataset engineering for machine learning practitioners**.

---

# Contributing

Suggestions and improvements are welcome. If you have ideas for improving the dataset splitter or adding additional dataset preparation tools, feel free to open an issue.

---

# License

This repository is licensed under the **MIT License**.

See the LICENSE file for details.

---

# Keywords

machine learning dataset splitter
python dataset splitter
split dataset train validation test python
computer vision dataset preparation
yolo dataset tools
image dataset organization python
