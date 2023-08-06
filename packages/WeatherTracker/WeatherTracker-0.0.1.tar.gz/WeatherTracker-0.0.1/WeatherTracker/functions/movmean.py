import numpy as np


def movmean(arr, N: int = 3):
    """
    Compute centered moving average of 1d array. Averaging window is asymmetric for elements N/2 from the beginning and end.
    :param arr: numpy array to be analyzed
    :type arr: numpy.ndarray
    :param N: total width of centered moving average window
    :type N: int
    :return: numpy.ndarray containing moving average of arr
    """
    ret = np.array([])
    for i in range(len(arr)):
        if N % 2 == 0:
            n = int(N / 2)
            if i - n < 0:
                val = np.sum(arr[0:i + n]) / len(arr[0:i + n])
            elif i + n > len(arr) - 1:
                val = np.sum(arr[i - n:len(arr)]) / len(arr[i - n:len(arr)])
            else:
                val = np.sum(arr[i - n:i + n]) / N
        else:
            n = int((N - 1) / 2)
            if i - n < 0:
                val = np.sum(arr[0:i + n + 1]) / len(arr[0:i + n + 1])
            elif i + n > len(arr) - 1:
                val = np.sum(arr[i - n:len(arr)]) / len(arr[i - n:len(arr)])
            else:
                val = np.sum(arr[i - n:i + n + 1]) / N
        ret = np.append(ret, val)
    return ret