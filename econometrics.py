import numpy as np
import pandas as pd
import statsmodels.api as sm

# Step 1: Data Simulation
np.random.seed(0)  # For reproducibility
n = 1000  # Number of observations
education = np.random.normal(12, 2, n)  # Average 12 years of education, with some variation
experience = np.random.normal(10, 5, n)  # Average 10 years of experience, with some variation
epsilon = np.random.normal(0, 1, n)  # Normally distributed error term
wage = 10 + 2*education + 1.5*experience + epsilon  # Generating wages

data = pd.DataFrame({'Wage': wage, 'Education': education, 'Experience': experience})

# Step 2: Model Estimation
X = sm.add_constant(data[['Education', 'Experience']])  # Adding a constant term for the intercept
model = sm.OLS(data['Wage'], X).fit()  # Fitting the model

# Step 3: Results Interpretation
print(model.summary())
