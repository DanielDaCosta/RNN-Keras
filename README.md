# Multiple-Outputs and Multiple-Losses RNN in Keras
The project consists of a Multi-Label Text Classifier project using a RNN from Keras.

The dataset consists of disaster messages that are classified into 36 different classes. The goal of the project is to classify an input message into these different classes.

The goal of the project is to explain how to deal with **Multiple-Outputs and Multiple-Losses RNN in Keras**. The project comes across this issue https://github.com/keras-team/keras/issues/8011 and presents a validy solution.

There are two approches on the project:
- Creating the Embeddings using Keras Embedding Layer
- Using [Glove](https://nlp.stanford.edu/projects/glove/) pre-trained embedding

You can check the [Medium Post](https://medium.com/@danieldacosta_75030/text-classifier-with-multiple-outputs-and-multiple-losses-in-keras-4b7a527eb858) for further details.

## Dataset
The dataset consists of disaster messages that are classified into 36 different classes. The dataset in highly imbalanced, having different distributions for each class. In order to reduce this problem a class weighted approach was used, where we make the classifier aware of the imbalanced data by incorporating the weights of classes into the cost function.

In the RNN model, a ```class_weight``` paramater was set in order to reduce the imbalaced distributions problems.

## Acknowledgments and References
- Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. GloVe: Global Vectors for Word Representation.
- https://medium.com/towards-artificial-intelligence/keras-for-multi-label-text-classification-86d194311d0e
- https://stats.stackexchange.com/questions/323961/how-to-define-multiple-losses-in-machine-learning
- https://github.com/keras-team/keras/issues/8011
