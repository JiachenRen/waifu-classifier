from scripts.get_dataset import get_gender_dataset, calculate_centroid_vector
from sklearn.model_selection import cross_val_score, ShuffleSplit
import numpy as np
from sklearn.svm import SVC

print('Loading dataset...')
X, y = get_gender_dataset()

# Baseline naive classifier.
# Since there are so many more descriptions for female, the naive classifier always predict the description as for female.
print('Naive classifier accuracy: %0.2f' % ((~y).sum() / len(y)))

# SVM classifier
model = SVC(kernel='linear')

# Cross-validation score using KFolds
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
scores = cross_val_score(model, X, y, cv=cv)
print(f'Scores: {scores}')
print(f'Mean: {scores.mean()}, Std: {scores.std()}')

# Fit the model using the entire dataset
model.fit(X, y)

# Predict never-seen-before descriptions crafted by hand
while True:
    desc = input('Desciption: ')
    vector: np.array = calculate_centroid_vector(desc)
    prediction = model.predict(vector.reshape((1, -1)))[0]
    if prediction:
        print('Is male.')
    else:
        print('Is female.')
