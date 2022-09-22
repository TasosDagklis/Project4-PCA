# -*- coding: utf-8 -*-
"""MNIST_784.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qHtxZBO9xQ_qHEeFLT2lteQBXddPblXL
"""

import numpy as np
np.set_printoptions(precision=3)
from IPython.display import Markdown
import matplotlib.pyplot as plt
import time

from sklearn.datasets import fetch_openml
from sklearn.preprocessing import LabelEncoder

X, y_str = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)

X = X.astype(float)
le = LabelEncoder().fit(y_str)
y = le.transform(y_str)

#split the data into training set and test set
X_train = X[:60000, :60000]
X_test = X[60000:, :]
y_train = y[:60000]
y_test = y[60000:]

#print the characteristics of the dataset
display(Markdown("**Number of Instances**: " + str(X.shape[0]) + "<br>" + 
                 "**Number of attributes**: " + str(X.shape[1]) + "<br>" + 
                 "**Max X**: " + str(np.max(X)) + "<br>" +
                 "**Min X**: " + str(np.min(X)) + "<br>" +
                 "**Max y**: " + str(np.max(y)) + "<br>" +
                 "**Min y**: " + str(np.min(y))))

display(Markdown("**Mean feature values:**"))
print(np.mean(X, 0))

display(Markdown("**Std of feature values:**"))
print(np.std(X, 0))

"""#Ταξινόμηση με όλα τα δεδομένα"""

#Classification with Extremely Randomized Trees
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score

start=time.time()
trees = ExtraTreesClassifier(n_jobs=-1)
trees.fit(X_train, y_train,)
y_pred = trees.predict(X_test)
stop=time.time()
print("Error rate: {:.3f}".format(1-accuracy_score(y_test, y_pred)))
print("Χρόνος που απαιτήθηκε: {:.3f}".format(stop-start))

"""Αρκετά χαμηλό Error rate!

#Μείωση Διαστάσεων
Υπολογίζουμε τις κύριες συνιστώσες όλου του training set. Για να εφαρμόσουμε PCA απαιτείται scaling των δεδομένων.
"""

#Dimensionality reduction with PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

start=time.time()
pca = PCA().fit(X_train)
stop = time.time()
X_train_trans = pca.transform(X_train)
X_test_trans = pca.transform(X_test)

print("Χρόνος που απαιτήθηκε: {:.3f}".format(stop-start))
print("Η πρώτη συνιστώσα περιγράφει το {:.3f}% της συνολικής διασποράς.".format(pca.explained_variance_ratio_[0]*100))

"""#Απεικόνιση των πρώτων 200 κύριων συνιστωσών


"""

plt.figure(figsize=(18,10))
plt.bar(range(200),pca.explained_variance_ratio_[0:200])
plt.title("Ποσοστό ερμηνευόμενης διασποράς των 200 πρώτων συνιστωσών")
plt.xlabel("# κύριας συνιστώσας")
plt.ylabel("% ερμηνευόμενης διασποράς")

plt.show()

"""# Ταξινόμηση στο χώρο των κύριων συνιστωσών"""

start=time.time()
trees = ExtraTreesClassifier(n_jobs=-1)
trees.fit(X_train_trans, y_train,)
y_pred = trees.predict(X_test_trans)
stop=time.time()
print("Error rate: {:.3f}".format(1-accuracy_score(y_pred, y_test)))
print("Χρόνος που απαιτήθηκε: {:.3f}".format(stop-start))

"""Διαπιστώνουμε ότι η PCA έπειτα από κλιμάκωση και με χρήση όλων των συνιστωσών οδηγεί σε χαμηλότερες επιδόσεις και αυξάνει το χρόνο εκπαίδευσης.

# **Ταξινόμηση με λιγότερες συνιστώσες**
"""

from sklearn.model_selection import cross_validate

n_components = range(5,100,5)
explained_var_ratios = []
error_rates = []
time_needed = []

for n in n_components:
  X_train_trans_red=X_train_trans[:,:n]

  trees = ExtraTreesClassifier(n_jobs=-1)

  cv_results = cross_validate(trees,X_train_trans_red, y_train)
  time_needed.append(np.mean(cv_results['fit_time']))
  explained_var_ratios.append(np.sum(pca.explained_variance_ratio_[:n]))
  error_rates.append(1-np.mean(cv_results['test_score']))


plt.figure(figsize=(10,6))
plt.plot(n_components, explained_var_ratios, label='Explained var', marker = '.')
plt.plot(n_components, error_rates, label='Error rate', marker = 'o')
plt.plot(n_components, np.array(time_needed)/10, label='Time/10', marker = 'x')
plt.legend()

plt.show()

"""# **Τελική ταξινόμηση**

Βλέπουμε ότι μετά τις 50-60 συνιστώσες το σφάλμα δε μειώνεται σημαντικά. Θα δοκιμάσουμε ταξινόμηση του test set με προβολή στις 55 κύριες συνιστώσες.
"""

start=time.time()
X_train_trans_red_final=X_train_trans[:,:55]
X_test_trans_red_final=X_test_trans[:,:55]
trees = ExtraTreesClassifier(n_jobs=-1)
trees.fit(X_train_trans_red_final,y_train)
y_pred = trees.predict(X_test_trans_red_final)
stop=time.time()

print("Error rate: {:.3f}".format(1-accuracy_score(y_test, y_pred)))
print("Χρόνος που απαιτήθηκε: {:.3f}".format(stop-start))

"""Διαπιστώνουμε μια αύξηση του σφάλματος σε σχέση με την αρχική μας ταξινόμηση (0.049 αντί για 0.028) αλλά και μια πολύ σημαντική μείωση του χρόνου εκπαίδευσης, από 24 δευτερόλεπτα σε 6."""