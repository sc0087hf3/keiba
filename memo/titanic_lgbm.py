import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# データ読み込み
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 欠損値補完（inplace=False で警告回避）
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# 特徴量と目的変数
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target = 'Survived'
X = df[features].copy()
y = df[target].copy()

# カテゴリ変数を明示的に変換
for col in ['Sex', 'Embarked', 'Pclass']:
    X[col] = X[col].astype('category')

# 学習・テスト分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBMデータ形式
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test)

# ハイパーパラメータ
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'learning_rate': 0.05,
    'verbose': -1
}

# モデル学習（early stoppingはcallback形式で）
model = lgb.train(
    params,
    train_data,
    valid_sets=[test_data],
    valid_names=["valid"],
    callbacks=[lgb.early_stopping(10)]
)

# 予測と評価
y_pred = model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)
print(f"Accuracy: {accuracy_score(y_test, y_pred_binary):.4f}")

# 特徴量重要度
lgb.plot_importance(model, importance_type='gain', max_num_features=10)
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig("feature_importance.png")  # グラフ表示できない環境でも保存
