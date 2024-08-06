# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree, plot_tree
import matplotlib.pyplot as plt

# Importing the dataset
try:
    training_dataset = pd.read_csv('Training.csv')
    test_dataset = pd.read_csv('Testing.csv')
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Slicing and Dicing the dataset
X = training_dataset.iloc[:, 0:132].values
y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Implementing the Decision Tree Classifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols = training_dataset.columns[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
def execute_bot():
    print("Please reply with yes/Yes or no/No for the following symptoms")
    
    def print_disease(node):
        node = node[0]
        val = node.nonzero()
        disease = labelencoder.inverse_transform(val[0])
        return disease

    def tree_to_code(tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        symptoms_present = []
        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print(name + " ?")
                ans = input().strip().lower()
                if ans == 'yes':
                    val = 1
                elif ans == 'no':
                    val = 0
                else:
                    print("Invalid response, please answer with yes or no.")
                    return recurse(node, depth)

                if val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                print(f"You may have {present_disease}")
                print()
                red_cols = dimensionality_reduction.columns
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
                print(f"Symptoms present: {list(symptoms_present)}")
                print()
                print(f"Symptoms given: {list(symptoms_given)}")
                print()
                confidence_level = (1.0 * len(symptoms_present)) / len(symptoms_given)
                print(f"Confidence level: {confidence_level}")
                print()
                
                # Load doctor dataset
                try:
                    doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name', 'Description'])
                except FileNotFoundError as e:
                    print(f"Error: {e}")
                    return

                doctors = pd.DataFrame()
                doctors['name'] = doc_dataset['Name']
                doctors['link'] = doc_dataset['Description']
                doctors['disease'] = dimensionality_reduction.index

                row = doctors[doctors['disease'] == present_disease[0]]
                if not row.empty:
                    print(f'Consult: {row["name"].values[0]}')
                    print(f'Visit: {row["link"].values[0]}')
                else:
                    print("No doctor information available for this disease.")
                
        recurse(0, 1)

    tree_to_code(classifier, cols)

# Execute the bot
execute_bot()
