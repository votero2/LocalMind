
from agents.reviewer_agent import review

question = """
Build a linear regression model to predict house prices
without leaking information from the test dataset.
"""

implementation = """
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

X = data[["area", "bedrooms", "bathrooms"]]
y = data["price"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
"""

print("=== REVIEWER AGENT TEST ===")

result = review(question, implementation)

print(result)