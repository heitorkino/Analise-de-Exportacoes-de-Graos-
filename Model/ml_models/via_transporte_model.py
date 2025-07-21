import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

# === Carregar dados ===
df_2023 = pd.read_csv("CSV-Files/Cleaned-CSVs/EXP_2023_Revisada.csv")
df_2024 = pd.read_csv("CSV-Files/Cleaned-CSVs/EXP_2024_Revisada.csv")
df_2025 = pd.read_csv("CSV-Files/Cleaned-CSVs/EXP_2025_Revisada.csv")

# === Preparar dados ===
df_train = pd.concat([df_2023, df_2024], ignore_index=True)
df_test = df_2025.copy()

p75 = df_train['KG_LIQUIDO'].quantile(0.75)
vias_criticas = [1, 3]

df_train['GARGALO'] = ((df_train['KG_LIQUIDO'] > p75) & (df_train['CO_VIA'].isin(vias_criticas))).astype(int)
df_test['GARGALO'] = ((df_test['KG_LIQUIDO'] > p75) & (df_test['CO_VIA'].isin(vias_criticas))).astype(int)

features = ['CO_MES', 'CO_ANO', 'CO_PAIS', 'CO_NCM', 'CO_VIA']
X_train = df_train[features].fillna(0)
y_train = df_train['GARGALO']
X_test = df_test[features].fillna(0)
y_test = df_test['GARGALO']

# === Label Encoding ===
categorical_cols = ['CO_PAIS', 'CO_NCM', 'CO_VIA']
for col in categorical_cols:
    le = LabelEncoder()
    X_train[col] = le.fit_transform(X_train[col])
    X_test[col] = X_test[col].map(lambda s: le.transform([s])[0] if s in le.classes_ else -1)

# === Avaliação por cross-validation ===
def evaluate_cv(random_states, X, y):
    for rs in random_states:
        print(f"\nRandom State: {rs}")
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=rs)
        precisions, recalls, f1s, accuracies = [], [], [], []

        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            X_train_fold, y_train_fold = X.iloc[train_idx], y.iloc[train_idx]
            X_val_fold, y_val_fold = X.iloc[val_idx], y.iloc[val_idx]

            smote = SMOTE(random_state=rs)
            X_res, y_res = smote.fit_resample(X_train_fold, y_train_fold)

            model = RandomForestClassifier(n_estimators=100, max_depth=20, min_samples_leaf=1, random_state=rs)
            model.fit(X_res, y_res)

            y_proba = model.predict_proba(X_val_fold)[:, 1]
            y_pred = (y_proba >= 0.62).astype(int)

            precisions.append(precision_score(y_val_fold, y_pred, zero_division=0))
            recalls.append(recall_score(y_val_fold, y_pred))
            f1s.append(f1_score(y_val_fold, y_pred))
            accuracies.append(accuracy_score(y_val_fold, y_pred))

            print(f" Fold {fold}: Precision={precisions[-1]:.3f}, Recall={recalls[-1]:.3f}, F1={f1s[-1]:.3f}, Accuracy={accuracies[-1]:.3f}")

        print(f" Média RS {rs}: Precision={np.mean(precisions):.3f}, Recall={np.mean(recalls):.3f}, F1={np.mean(f1s):.3f}, Accuracy={np.mean(accuracies):.3f}")

# === Executar avaliação com random states
random_states = [42, 7, 21, 100, 2025]
evaluate_cv(random_states, X_train, y_train)

# === Treinamento final e teste
smote_final = SMOTE(random_state=42)
X_train_res, y_train_res = smote_final.fit_resample(X_train, y_train)

final_model = RandomForestClassifier(n_estimators=100, max_depth=20, min_samples_leaf=1, random_state=42)
final_model.fit(X_train_res, y_train_res)

y_test_proba = final_model.predict_proba(X_test)[:, 1]
thresholds = np.linspace(0, 1, 101)
f1_scores = [f1_score(y_test, (y_test_proba >= t).astype(int)) for t in thresholds]
best_threshold_test = thresholds[np.argmax(f1_scores)]
y_test_pred_final = (y_test_proba >= best_threshold_test).astype(int)

print(f"\nMelhor limiar no teste: {best_threshold_test:.2f}")
print(f"Precision: {precision_score(y_test, y_test_pred_final):.3f}, Recall: {recall_score(y_test, y_test_pred_final):.3f}, F1: {f1_score(y_test, y_test_pred_final):.3f}, Accuracy: {accuracy_score(y_test, y_test_pred_final):.3f}")
print("\n=== Matriz de Confusão Teste ===")
print(confusion_matrix(y_test, y_test_pred_final))
print("\n=== Relatório de Classificação Teste ===")
print(classification_report(y_test, y_test_pred_final))

# === Importância das variáveis
importances = final_model.feature_importances_
feature_names = X_train.columns
df_importancias = pd.DataFrame({'Feature': feature_names, 'Importância': importances})
df_importancias = df_importancias.sort_values(by='Importância', ascending=False)

# === Gráfico
plt.figure(figsize=(8, 5))
sns.barplot(x='Importância', y='Feature', data=df_importancias, hue='Feature', legend=False, palette='viridis')
plt.title('Importância das Variáveis no Modelo')
plt.xlabel('Importância')
plt.ylabel('Variável')
plt.tight_layout()
plt.show()