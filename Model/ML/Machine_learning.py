import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE

# ======== 1. Carregar os dados ========
path_base = 'c:/Users/Aluno/Desktop/Analise-de-Exportacoes-de-Graos-/CSV/Tratados/'

arquivos = ['exportacoes_2023.csv', 'exportacoes_2024.csv', 'exportacoes_2025.csv']

df = pd.concat([pd.read_csv(path_base + arq) for arq in arquivos], ignore_index=True)

# ======== 2. Definir target binário "GARGALO" ========
peso_medio = df['KG_LIQUIDO'].mean()
vias_criticas = [1, 3]

df['GARGALO'] = ((df['CO_VIA'].isin(vias_criticas)) & (df['KG_LIQUIDO'] > peso_medio)).astype(int)

# ======== 3. Selecionar features ========
features = ['CO_MES', 'CO_ANO', 'CO_PAIS', 'CO_BLOCO_ECONOMICO', 'CO_NCM', 'CO_VIA']
X = df[features]
y = df['GARGALO']

# ======== 4. Pré-processamento ========
cat_features = ['CO_PAIS', 'CO_BLOCO_ECONOMICO', 'CO_NCM', 'CO_VIA']
num_features = ['CO_MES', 'CO_ANO']

ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_cat = ohe.fit_transform(X[cat_features])
X_num = X[num_features].to_numpy()

X_final = np.hstack([X_num, X_cat])

# ======== 5. Dividir treino e teste ========
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42, stratify=y)

# ======== 6. Balancear com SMOTE ========
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

# ======== 7. Treinar modelo ========
model = RandomForestClassifier(random_state=42, class_weight='balanced')
model.fit(X_train_bal, y_train_bal)

# ======== 8. Avaliação inicial ========
y_pred = model.predict(X_test)
print("Matriz de Confusão:")
print(confusion_matrix(y_test, y_pred))
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# ======== 9. Ajuste de threshold ========
y_probs = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls)
best_idx = np.argmax(f1_scores)
best_threshold = thresholds[best_idx]

print(f"\nMelhor threshold para F1-score: {best_threshold:.3f}")

y_pred_adj = (y_probs >= best_threshold).astype(int)

print("Avaliação com threshold ajustado:")
print(confusion_matrix(y_test, y_pred_adj))
print(classification_report(y_test, y_pred_adj))
