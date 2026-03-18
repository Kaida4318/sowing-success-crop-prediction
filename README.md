# Sowing Success: AI-Driven Crop Recommendation 🌾

### 🎯 Objective
To help farmers optimize crop yields by predicting the best crop type based on soil Nitrogen (N), Phosphorous (P), Potassium (K), and pH levels.

### 📊 Key Results
* **Best Model:** SVM (RBF Kernel) with **73% Accuracy**.
* **MVP Feature:** **Potassium (K)** was identified as the strongest individual predictor (F1-score: 0.18).
* **Impact:** Demonstrates how low-cost soil testing (prioritizing K) can still provide high-value insights.

### 🛠️ Tech Stack
* **Python** (Pandas, NumPy)
* **Scikit-Learn** (Logistic Regression, SVM, StandardScaler)
* **Matplotlib & Seaborn** (Confusion Matrix Heatmaps)

<table>
  <tr>
    <td><img src="correlation matrix.png" width="400"></td>
    <td>
      <b>Key Insights from Correlation:</b><br><br>
      • <b>P & K Connection:</b> High correlation (0.74) suggests these nutrients often move together.<br>
      • <b>pH Independence:</b> Low correlation shows pH provides a unique environmental signal.<br>
      • <b>Model Impact:</b> These relationships explain why some "Problem Pairs" (like Rice and Jute) are harder for the model to separate.
    </td>
  </tr>
</table>
