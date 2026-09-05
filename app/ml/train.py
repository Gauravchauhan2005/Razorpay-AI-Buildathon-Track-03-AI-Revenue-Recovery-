import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from app.ml.features import FeatureEngineer

def load_data(filepath: str):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def main():
    print("Loading data...")
    try:
        raw_data = load_data("generator/data/batch_001.jsonl")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
        
    failed_payments = [d for d in raw_data if d.get("status") == "failed" and "recovered" in d]
    
    if not failed_payments:
        print("No failed payments with 'recovered' target found.")
        return
        
    engineer = FeatureEngineer()
    
    X = []
    y = []
    
    for row in failed_payments:
        features_dict = engineer.extract_features(row)
        X.append(engineer.to_feature_vector(features_dict))
        y.append(int(row["recovered"]))
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForestClassifier": RandomForestClassifier(random_state=42),
        "GradientBoostingClassifier": GradientBoostingClassifier(random_state=42)
    }
    
    best_model = None
    best_f1 = -1
    best_name = ""
    
    print(f"{'Model':<30} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'ROC-AUC':<10}")
    print("-" * 80)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        
        print(f"{name:<30} {acc:.4f}     {prec:.4f}     {rec:.4f}     {f1:.4f}     {auc:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_name = name
            
    print(f"\nBest model based on F1: {best_name}")
    print("Classification Report:")
    print(classification_report(y_test, best_model.predict(X_test)))
    
    joblib.dump(best_model, "app/ml/model.pkl")
    print("Saved best model to app/ml/model.pkl")

if __name__ == "__main__":
    main()
