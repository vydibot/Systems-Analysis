# Systematic Analysis of Kaggle Competition: Santa 2024

📝 **Authors**:  
- Jairo Arturo Barrera Mosquera (`20222020142`)  
- Gabriela Martinez Silva (`20231020205`)  
📅 **Date**: March 2025  

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

### 🤖 Model Architecture
1. **Permutation Generation**:  
   - Use `itertools` to explore possible word orders.  
2. **Perplexity Evaluation**:  
   - Score each permutation using **Gemma 2B**.  
   - Select the sequence with *lowest perplexity*.  

### 📤 Output
- `.csv` file mapping `id` to optimized word sequence.  

---

## 📌 Conclusions
- Combines **NLP fluency** (Gemma 2B) with **combinatorial optimization**.  
- Computational limits arise from factorial growth (`n!`).  
- Perplexity metrics occasionally favor ungrammatical sequences.  

