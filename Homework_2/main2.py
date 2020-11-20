import numpy as np
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt
import test_data
from pathlib import Path
from sklearn import naive_bayes



csv_path = Path('generate_data/data66666_10000.csv')
df = pd.read_csv(csv_path)

X = np.array(df.iloc[:, 1:-1])
y = np.array(df.iloc[:, -1:])#.reshape(-1,)  # 橫的直的都吃

clf = tree.DecisionTreeClassifier(random_state=666, max_depth=4, criterion='entropy')
clf = clf.fit(X, y)
# gnb = naive_bayes.GaussianNB()
# y_gnb = gnb.fit(X, y)

test_data, test_target = test_data.gererate_test_data(10000)
result_clf = clf.predict(test_data)
# result_gnb = gnb.predict(test_data)
print(clf.score(X, y))
# print(gnb.score(X, y))

print((result_clf == test_target).sum() / len(test_target))
print(clf.score(test_data, test_target))
# print((result_gnb == test_target).sum() / len(test_target))
# print(gnb.score(test_data, test_target))

tree.plot_tree(clf, filled=True)
plt.show()
# tree.export_graphviz(clf)
