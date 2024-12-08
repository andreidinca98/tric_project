

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
file_path = 'terrorist-attacks new.csv'
data = pd.read_csv(file_path)

print (data.shape)

data.dtypes

data.isnull().sum()

data = data.rename(columns={'Entity': 'Country', 'Terrorist attacks': 'Attacks'})
data = data[['Country', 'Year', 'Attacks']]  # Remove unnecessary columns , meaning Entity code that is not present on all rows

#Convert string into number in countries column
label_encoder = LabelEncoder()
data['Country_encoded'] = label_encoder.fit_transform(data['Country'])

# Define features (Country and Year) and target (Attacks)
inputs = data[['Country_encoded', 'Year']]
attacks = data['Attacks']

# data nroamlization
scaler = StandardScaler()
inputs_scaled = scaler.fit_transform(inputs)

# data splitiing into train set and test set
from sklearn.model_selection import train_test_split
inputs_train, inputs_test, attacks_train, attacks_test = train_test_split(inputs_scaled, attacks, test_size=0.05, random_state=42)

# train the model with the best hyperparameters
best_params = {
    'bootstrap': False,
    'max_depth': 10,
    'max_features': 'sqrt',
    'min_samples_leaf': 1,
    'min_samples_split': 2,
    'n_estimators': 50
}

model = RandomForestRegressor(
    random_state=42,
    **best_params
)

model.fit(inputs_train, attacks_train)

# Evaluation of the model
attacks_pred = model.predict(inputs_test)
mse = mean_squared_error(attacks_test, attacks_pred)
r2 = r2_score(attacks_test, attacks_pred)

print(f"Test Set MSE: {mse}")
print(f"R^2 Score on Test Set: {r2}")

country_input = input("Enter the country: ")
year_input = int(input("Enter the year: "))

# Encode the input country
if country_input not in label_encoder.classes_:
    print("Country not found in dataset.")
else:
    country_encoded = label_encoder.transform([country_input])[0]

    user_features = scaler.transform([[country_encoded, year_input]])

    prediction = int(model.predict(user_features))
    print(f"Predicted number of terrorist attacks in {country_input} ({year_input}): {prediction}")
