import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

# Prep dataset
print('Prepare data')
data = pd.read_csv('data/btcusd.csv')
data['returns'] = data['close'] - data['close'].shift(1)
data['ma200'] = data.rolling(window=200).apply(lambda values: np.average(values))

# Discrete values
data['std30'] = data.rolling(window=30).apply(lambda values: np.round(np.stdev(values)))
data['std200'] = data.rolling(window=200).apply(lambda values: np.round(np.stdev(values)))
data['mom10'] = data['close'] - data['close'].shift(10) > 0
data['moving_average'] = data['close'] - data['ma200'] > 0
data = data.dropna()

# Setup pipeline
print('Create pipeline')
pipe_steps = [('scaler', StandardScaler()), ('descT', DecisionTreeClassifier())]
check_params = {'descT_criterion': ['gini', 'entropy'],
                'descT_max_depth': np.arrange(3, 15)}
pipeline = Pipeline(pipe_steps)

# Setup features and labels
# Features = independent vars
# Labels = dependable vars
feature_cols = ['std30', 'std200', 'mom10', 'moving_average']
# what is pd.get_dummies ??

# Setup Tree
# clf = DecisionTreeClassifier(criterion='gini', max_depth=4)
# clf.fit(features, labels)

