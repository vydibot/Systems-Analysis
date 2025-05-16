# Systematic Analysis of Kaggle Competition: Santa 2024

📝 **Authors**:  
- Jairo Arturo Barrera Mosquera (`20222020142`)  
- Gabriela Martinez Silva (`20231020205`)  
📅 **Date**: MAY 2025  

---
## Contents

### Workshops
1. **Workshop 1**: [Systems Analysis For Santa Keagle Problem](/Workshop%201)

2. **Workshop 2**: [Systems Architecture For Santa Keagle Problem](/Workshop%202)

### Catch-Up

1. **Catch-Up Material**: [Systems Architecture For Santa Keagle Problem](/Catch-Up)

---

## 🎯 Competition Overview
**Goal**: Minimize perplexity of scrambled Christmas-themed text passages by reordering words into coherent sequences.  
**Evaluation Metric**: Average perplexity (lower = better) using the **Gemma 2 9B** language model.  

### 🗂 Dataset
- **Data Structure**: Jumbled passages from Christmas stories.  
- **Submission Data**: Submissions must permute words in `sample_submission.csv`. (Same data using)
- **Constraints**:  
  - Words can only be reordered (*no modifications/additions/deletions*).  
  - Valid permutations must include all original words.  

---

## 🔍 System Analysis
### 📥 Input
- Scrambled word sequences (1 per row).  
- **Functional Requirements**:  
  - Process sentences *as-provided* by Kaggle.  

### 🏗️ Architecture

The system follows a modular approach, designed to efficiently process shuffled word lists and reconstruct coherent passages. The key components are:

1.  **Normalized Input:**
    * **Description:** Handles raw input data, validates format, normalizes word representations (preserving original case for output), and counts word occurrences.
    * **Justification:** Ensures data integrity, validates input, and prepares data for downstream processing.

2.  **Define Templates:**
    * **Description:** Performs linguistic analysis to infer grammatical structures and potential sentence patterns, generating probabilistic templates or constraints to guide permutation search.
    * **Justification:** Reduces complexity by focusing the search space and provides structural guidance for generation.

3.  **Generate Permutations:**
    * **Description:** The core search engine that creates candidate sentence orderings using intelligent search strategies (e.g., A*, Simulated Annealing, Genetic Algorithms), guided by an external Evaluator module.
    * **Justification:** Implements the core functionality and manages the combinatorial explosion of possible permutations.

---

### ⚙️ System Requirements

**Functional Requirements (FRs):**
* **Sentence Usage:** The system must operate only on the shuffled sentences provided by Kaggle.
* **Word Constraints:** The system must not add, modify, or remove any words from the original input.
* **Sequence Length Handling:** The system must be capable of processing sequences of varying lengths.

**Non-Functional Requirements (NFRs):**
* **Perplexity:** The final sentence should have a low perplexity score.
* **Semantic Coherence:** The resulting sentence must be grammatically and semantically correct.

---

### 📉 Sensitivity and Chaos

* **Sensitivity:** The model is highly sensitive to input permutations; small changes can significantly affect perplexity scores. Sensitivity is influenced by text length (combinatorial explosion), grammatical structure ambiguity, and lexical distribution (common vs. rare words).
* **Chaos and Randomness:** Small changes in word position can cause drastic perplexity changes, sometimes favoring grammatically incorrect phrases. The combinatorial explosion ($n!$ permutations) for $n$ words makes exhaustive evaluation computationally infeasible for larger inputs.

---  

### 📤 Output
- `.csv` file mapping `id` to optimized passage.  

