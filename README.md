# PCA and Classification
This repository contains a project that applies **Principal Component Analysis (PCA)** for dimensionality reduction and trains **classification models** on the **MNIST-784 dataset**, a widely used benchmark for handwritten digit recognition.

## 📌 Project Overview

The **MNIST dataset** consists of **28x28 grayscale images** of handwritten digits (0-9), each represented as a **784-dimensional vector**. In this project, we explore how **PCA** can reduce the dimensionality while preserving essential features for classification.

For more details on the dataset:
- [Original MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
- [OpenML MNIST-784](https://www.openml.org/d/554)

## 🚀 Approach

### 1️⃣ Data Preprocessing
- **Load MNIST-784 dataset** from OpenML  
- **Normalize pixel values** (0-255 → 0-1)  
- **Flatten images** into vectors  

### 2️⃣ Dimensionality Reduction with PCA
- Compute **principal components**  
- Reduce dataset to **lower dimensions**  
- Visualize **explained variance ratio** to select optimal PCs  

### 3️⃣ Classification Models
- Train models on **original and PCA-reduced data**:
  - Logistic Regression  
  - Support Vector Machines (SVM)  
  - Random Forest 
- Compare performance based on **accuracy, precision, recall**  

### 4️⃣ Evaluation & Insights
- Analyze **classification accuracy vs. number of PCs**  
- Visualize **digit clusters** in **2D PCA space**  
- Compare **performance trade-offs** (speed vs. accuracy)  

## 📊 Dataset

The dataset consists of:
- **70,000 grayscale images** (60,000 train, 10,000 test)  
- **28x28 pixel resolution** per digit  
- **Flattened 784-dimensional feature vectors**  
