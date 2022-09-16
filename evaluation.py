from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score


def get_metrics(tests, contrasts, classifier):
    y_pred = []
    y_true = [1] * len(tests) + [0] * len(contrasts)

    for test in tests:
        y_pred.append(round(classifier(test)))

    for contrast in contrasts:
        y_pred.append(round(classifier(contrast)))

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    f1 = f1_score(y_true, y_pred)
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)

    return sensitivity, specificity, f1
