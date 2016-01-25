# Decision-Tree-Classfier

A Decision Tree classifier is built for predicting credit worthiness of applicants.

Over fitting: The code prunes noisy data, it keeps track of the different set of values
in the data and as soon as the count of positive and negative turns to become in the ratio of 1:9,
the minority is considered as noise and return the majority. In case there is Missing Data 
in the query, we consider all possible attribute value that can go in place of the ‘?’,
calculate the classification for each of them and return the majority.
