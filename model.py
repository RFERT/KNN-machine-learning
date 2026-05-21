import pandas as pd
from pandas import DataFrame, Series

class KNN:
    def __init__(self):
        self.k_neighbours = 1
        self.k_scores = []

    def fit(self, X_train:DataFrame, y_train:pd.Series):
        self.X_train = X_train
        self.y_train = y_train
    
    def predict(self, X_test:DataFrame):
        """
        Predict the target of the X_test value(s)
        """
        predictions = []
        for x in X_test:
            distances = []
            for x_train in self.X_train:
                distances.append(self.compute_euclidian_distance(x_train, x))
            distances, indexes = self.sorter_desc(distances)
            _k_distances, k_indexes = pd.Series(distances[:self.k_neighbours]), pd.Series(indexes[:self.k_neighbours])
            predictions.append(Series.mode(self.y_train[k_indexes]))
        return predictions
            

    def compute_euclidian_distance(self, a, b) -> float:
        """Compute euclidian distance between the point a and b for any dimension"""
        if type(a)=="<class 'pandas.Series'>" and type(b)=="<class 'pandas.Series'>":
            return ((a[0]-b[0])**2+ ((a[index]-b[index])**2 for index in range(1,len(a))))**0.5
        if type(a) == "<class 'int'>" and type(b) == "<class 'int'>":
            return ((a-b)**2)**0.5
        else:
            print("Erreurs de types dans l'appel à KNN.compute_euclidian_distance()")
            print(f"Type de a : {type(a)}")
            print(f"Type de b : {type(b)}")
            print("Types supportés : <class 'pandas.Series'> & <class 'int'>")
            raise TypeError     # Don't abuse please I cannot adapt it for every type.... I HAVE A LIFE !!!!

    def sort_desc(self, tab):
        """
        sort the tab table by desc
        Deprecated =(
        """
        sorted = tab[0]
        for element_index in range(1,len(tab)):
            placed = False
            for index in range(len(sorted)):
                if tab[element_index]>sorted[index]:
                    sorted = sorted[:index] + [tab[element_index]] + sorted[index+1:]
                    placed = True
                    break
            if placed == False:
                sorted.append(tab[element_index])
            tab = tab[1:]
        return sorted
    
    def sorter_desc(self, tab):
        """
        Sort the table and return the sorted table and the original indexes in the new order
        """
        indexes, sorted = [], []
        for _ in range(len(tab)):
            indexes.append(tab.index(max(tab)))
            sorted.append(tab.pop(indexes[-1]))
        return sorted, indexes
    
    def evaluate(self, X_test, y_test):
        """
        evaluate the model accuracy
        """
        y_pred = self.predict(X_test=X_test)
        score = 0
        for i in range(len(y_pred)):
            score += 1 if y_pred[i] == y_test[i] else 0
        return score/len(y_pred)
    
    def grid_search(self, X_valid, y_valid):
        self.k_scores += [self.evaluate(X_test=X_valid, y_test=y_valid)]    # Load the K score in the attribute to use it just after
        self.k_neighbours += 2      # Increment by 2 to test the next odd value (odd to avoid equalities in the neighbours max count)
        if self.evaluate(X_test=X_valid, y_test=y_valid) > self.k_scores[-1]:
            self.grid_search(X_valid, y_valid)      # if we didn't see the lowing value we continue the process (recursive 👈😁👆)
        else:
            self.k_neighbours -= 2                  # if we saw the lowing value we come back to the perfect one and then announce this to the happy user (nice guy is there)
            print(f"k-value found: {self.k_neighbours}")    # Hope he's gona be soooo happy

# Please excuse me for the 2 AM comments ;)