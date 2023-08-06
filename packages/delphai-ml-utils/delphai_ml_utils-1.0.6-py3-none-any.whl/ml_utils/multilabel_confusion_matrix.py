import numpy as np


def multilabel_confusion_matrix(y_true, preds):
    """
    Calculates confusion matrix for multi-label classification task.
    Reference: paper "Multi-label Classifier Performance Evaluation
    with Confusion Matrix", https://aircconline.com/csit/papers/vol10/csit100801.pdf

    Inputs are one-hot numpy arrays of shape (N, q)
    where:
        N - number of examples
        q - number of labels per target

    Output is confusion matrix numpy array of shape (q, q)
    """

    # difference of labels sets
    def diff_of_labels(a, b):
        inds = np.setdiff1d(np.where(a == 1), np.where(b == 1))
        difference = np.zeros(len(a))
        difference[inds] = 1
        return difference

    # intersection of labels sets
    def intersection_of_labels(a, b):
        inds = np.intersect1d(np.where(a == 1), np.where(b == 1))
        inersection = np.zeros(len(a))
        inersection[inds] = 1
        return inersection

    q = y_true.shape[1]

    confusion_matrix = np.zeros((q, q))

    # algorithm proposed in the paper
    for y, z in zip(y_true, preds):
        if np.all(y == z):
            confusion_matrix += np.diag(y)
        else:
            if diff_of_labels(y, z).sum() == 0:
                confusion_matrix += np.outer(
                    intersection_of_labels(y, z), diff_of_labels(z, y)
                ) + sum(y) * np.diag(y) / sum(z)
            # if prediction is empty, no update for matrix
            elif diff_of_labels(z, y).sum() == 0 and sum(z) == 0:
                continue
            elif diff_of_labels(z, y).sum() == 0 and sum(z) != 0:
                confusion_matrix += np.outer(diff_of_labels(y, z), z) / sum(
                    z
                ) + np.diag(z)
            else:
                confusion_matrix += np.outer(
                    diff_of_labels(y, z), diff_of_labels(z, y)
                ) / sum(diff_of_labels(z, y)) + np.diag(intersection_of_labels(y, z))

    return confusion_matrix


# Compute modified confusion matrix for multi-class, multi-label tasks.
def compute_modified_confusion_matrix(labels, outputs):
    # Compute a binary multi-class, multi-label confusion matrix, where the rows
    # are the labels and the columns are the outputs.
    num_recordings, num_classes = np.shape(labels)
    confusion_matrix = np.zeros((num_classes, num_classes))

    # Iterate over all of the recordings.
    for i in range(num_recordings):
        # Calculate the number of positive labels and/or outputs.
        normalization = float(
            max(np.sum(np.any((labels[i, :], outputs[i, :]), axis=0)), 1)
        )
        # Iterate over all of the classes.
        for j in range(num_classes):
            # Assign full and/or partial credit for each positive class.
            if labels[i, j]:
                for k in range(num_classes):
                    if outputs[i, k]:
                        confusion_matrix[j, k] += 1.0 / normalization

    return confusion_matrix


def compute_modified_confusion_matrix_v2(labels, outputs):
    """
    This function calculates a multilabel confusion matrix where
    only misclassified instances land outside of the main diagonal.
    The contribution to the misclassificaiton is split evenly between
    all true labels, i.e. if there are n true labels and the label
    j was incorrectly assigned, 1/n will be added to all entries
    (i, j) where i are all the true labels.
    Furthermore, each row is normalized by the number of instances
    there the label i is true.
    Thus, the rows of the matrix do not necessarily add to 1,
    but instead faithfully represent the fraction of the data
    that leads to specific classifitations.
    Finally, the last row in the matrix represents the data points with
    no true classification. Here the contribution to each misclassification
    is one and the row is normalized by the number of such points.
    """
    num_recordings, num_classes = np.shape(labels)
    confusion_matrix = np.zeros((num_classes + 1, num_classes))
    class_counts = np.zeros(num_classes + 1)
    for label in labels:
        if not any(np.array(label)):
            # No labels in this point
            class_counts[-1] += 1
            continue
        for i, val in enumerate(label):
            if val:
                class_counts[i] += 1
    class_counts[class_counts == 0] = 1  # Prevent division by 0

    for i in range(num_recordings):
        indices_true_instances = np.where(np.array(labels[i]) == 1)[0]
        number_true_instances = len(indices_true_instances)
        if number_true_instances == 0:
            # no true labels in this point
            confusion_matrix[-1, :] += np.array(outputs[i]) / class_counts[-1]
        else:
            for j in range(num_classes):
                # Assign full and/or partial credit for each positive class.
                if outputs[i, j] and labels[i, j]:
                    confusion_matrix[j, j] += 1 / class_counts[j]
                elif outputs[i, j] and not labels[i, j]:
                    for index in indices_true_instances:
                        confusion_matrix[index, j] += 1 / (
                            number_true_instances * class_counts[index]
                        )

    return confusion_matrix
