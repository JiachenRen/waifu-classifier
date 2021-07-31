import tensorflow as tf
from scripts.get_dataset import get_waifu_dataset, wv, vectorize
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Input, Flatten, Dense, Dropout, Activation
from tensorflow.keras.initializers import Constant
from tensorflow.keras import Sequential
from tensorflow.keras.losses import MeanSquaredError

print('Loading dataset...')
X, y = get_waifu_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print('Building model...')
embedding = Embedding(
    input_dim=len(wv.index_to_key),
    output_dim=100,
    embeddings_initializer=Constant(wv.vectors),
    trainable=False
)
model = Sequential()
model.add(Input(shape=(100,), dtype="int64"))
model.add(embedding)
model.add(Conv1D(64, 5, activation="relu"))
model.add(MaxPooling1D(5))
model.add(Conv1D(32, 3, activation="relu"))
model.add(MaxPooling1D(3))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.3))
model.add(Activation(activation='relu'))
model.add(Dense(1, activation='linear'))
model.summary()

# Training
model.compile(loss=MeanSquaredError(), optimizer=tf.keras.optimizers.Adam(1e-3))
model.fit(X_train, y_train, batch_size=64, epochs=10, validation_data=(X_test, y_test))

predicted_scores = model.predict(X_test)
print('Predicted:')
print(predicted_scores)
print('Actual:')
print(y_test)

while True:
    desc = input('Description: ')
    score = model.predict(vectorize([desc]))[0]
    print(f'Rank: {score}')
