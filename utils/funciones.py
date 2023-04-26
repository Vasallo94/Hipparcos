from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt


def fritas(df):
    """
    Given a pandas DataFrame, encodes all categorical (object) columns using
    Label Encoding and returns a copy of the encoded DataFrame.
    Parameters:
    - df: pandas DataFrame
    Returns:
    - df_encoded: pandas DataFrame
    - encoder_info: list of dicts
    """
    df_encoded = df.copy()  # Make a copy of the original DataFrame
    # Select the categorical columns of the DataFrame
    object_columns = df_encoded.select_dtypes(include=["object"]).columns
    encoder_info = []  # Initialize a list to store the encoder information

    for column in object_columns:
        le = LabelEncoder()  # Create a new LabelEncoder for each categorical column
        # Fit and transform the LabelEncoder on the column
        df_encoded[column] = le.fit_transform(df_encoded[column].astype(str))
        encoder_info.append({  # Store the encoder information in a dictionary
            'column': column,
            'labels': list(le.classes_),  # List the original labels
            'codes': list(le.transform(le.classes_))  # List the encoded codes
        })

    # Return the encoded DataFrame and the encoder information
    return df_encoded, encoder_info


def bravas(df, target_column, min_k=2, max_k=15):
    """
    Given a pandas DataFrame, a target column name, a range of k values and a
    minimum number of samples per fold, performs K-NN regression using cross-validation
    to find the best value of k (number of neighbors) based on the mean squared error.
    Parameters:
    - df: pandas DataFrame
    - target_column: str, name of the target column
    - min_k: int, minimum number of neighbors to consider
    - max_k: int, maximum number of neighbors to consider
    Returns:
    - best_k: int, best value of k found
    """
    # Instantiate a LabelEncoder object
    le = LabelEncoder()
    # Make a copy of the input DataFrame
    df_encoded = df.copy()
    # Select object columns (categorical) of df_encoded
    object_columns = df_encoded.select_dtypes(include=['object']).columns
    # Iterate over each categorical column and apply Label Encoding
    for column in object_columns:
        df_encoded[column] = le.fit_transform(df_encoded[column].astype(str))
    # Impute missing values using the mean of each column
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(
        df_encoded), columns=df_encoded.columns)
    # Separate the predictors (X) from the target (y)
    X = df_imputed.drop(target_column, axis=1)
    y = df_imputed[target_column]
    # Define a pipeline for K-NN regression
    pipeline = Pipeline(steps=[('model', KNeighborsRegressor(n_neighbors=3))])
    # Set the hyperparameters to tune
    params = {'model__n_neighbors': [3, 5, 7],
              'model__weights': ['uniform', 'distance']}
    best_k = 0
    best_score = -np.inf
    # Iterate over a range of k values and perform cross-validation
    for k in range(min_k, max_k+1):
        kf = KFold(n_splits=k, shuffle=True, random_state=42)
        grid_search = GridSearchCV(
            pipeline, params, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X, y)
        # Keep track of the best k and best score found so far
        if grid_search.best_score_ > best_score:
            best_score = grid_search.best_score_
            best_k = k
    # Return the best value of k found
    return best_k


def mojo_picon(df: pd.DataFrame, n_neighbors: int) -> pd.DataFrame:
    """
    Imputes missing values in a dataframe using the K-Nearest Neighbors (KNN) strategy.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to be imputed.
    n_neighbors : int
        The number of nearest neighbors to consider for imputation. You should use your previous best_k result.
    Returns
    -------
    pd.DataFrame
        A copy of the original dataframe with missing values in numeric columns imputed with KNN.
    """
    # Make a copy of the original dataframe
    df_imputed = df.copy()
    # Create a KNNImputer object with the specified number of neighbors
    imputer = KNNImputer(n_neighbors=n_neighbors)
    # Select the numeric columns of the copied dataframe
    numeric_columns = df_imputed.select_dtypes(
        include=['int64', 'float64']).columns
    # Impute missing values in the numeric columns of the copied dataframe using KNNImputer
    df_imputed[numeric_columns] = imputer.fit_transform(
        df_imputed[numeric_columns])
    # Return the copied dataframe with imputed missing values
    return df_imputed


def des_fritas(df_encoded, encoder_info):
    """
    Given a pandas DataFrame that has been encoded with the `fritas()` function and the encoder
    information dictionary returned by that function, decodes all categorical columns and returns
    a copy of the original DataFrame with the encoded columns replaced by their original values. 
    This function replaces any codes that are not in the original list of labels with -1

    Parameters:
    - df_encoded: pandas DataFrame
    - encoder_info: list of dicts

    Returns:
    - df_decoded: pandas DataFrame
    """
    df_decoded = df_encoded.copy()  # Make a copy of the encoded DataFrame

    # Loop over each encoder in the encoder_info dictionary
    for encoder in encoder_info:
        column = encoder['column']
        labels = encoder['labels']
        codes = encoder['codes']
        le = LabelEncoder()  # Create a new LabelEncoder for the column
        le.classes_ = np.array(labels)  # Set the original labels
        # Replace NaN values in the encoded column with -1
        df_decoded[column].fillna(-1, inplace=True)
        # Replace any codes that are not in the original list of labels with -1
        df_decoded[column].where(
            df_decoded[column].isin(codes), -1, inplace=True)
        # Inverse transform the codes
        df_decoded[column] = le.inverse_transform(
            df_decoded[column].astype(int))

    return df_decoded


def pure(df, method='minmax'):
    """
    Scales the values of a pandas DataFrame using either the MinMaxScaler or the StandardScaler.
    Parameters:
    df (pandas.DataFrame): the DataFrame to be scaled
    method (str): the scaling method to use; must be either 'minmax' or 'standard' (default 'minmax')
    Returns:
    pandas.DataFrame: the scaled DataFrame
    sklearn.preprocessing scaler: the scaler object used for scaling
    Raises:
    ValueError: if method is not 'minmax' or 'standard'
    """
    scaler = None
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()

    if scaler:
        # Fit and transform the DataFrame using the scaler
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        # Return the scaled DataFrame and the scaler object
        return df_scaled, scaler
    else:
        raise ValueError("method must be either 'minmax' or 'standard'")


def cortar_en_tiritas(df, target_column, test_size=0.2, random_state=None):
    """
    This function splits a pandas DataFrame into training and testing sets, and returns the resulting data splits.
    Parameters:
    - df: a pandas DataFrame object containing the data to be split
    - target_column: a string representing the name of the target column to be used for prediction
    - test_size: a float between 0 and 1 representing the proportion of the data to be used for testing
    - random_state: an int or None representing the seed used by the random number generator
    Returns:
    - X_train: a pandas DataFrame object containing the features used for training
    - X_test: a pandas DataFrame object containing the features used for testing
    - y_train: a pandas Series object containing the target values used for training
    - y_test: a pandas Series object containing the target values used for testing
    """

    # Remove the target column from the DataFrame and store it in y
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    # Split the data into training and testing sets using the train_test_split function
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state)

    # Return the resulting data splits
    return X_train, X_test, y_train, y_test


def evaluar_papata(model, X_test, y_test):
    """
    Evaluates a regression model on a test set and returns the mean squared error (MSE),
    mean absolute error (MAE), and R-squared (R2) score.
    Args:
        model: A trained regression model.
        X_test: Test set features.
        y_test: Test set target values.
    Returns:
        A dictionary containing the MSE, MAE, and R2 scores.
    """
    # Use the trained model to make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate the MSE, MAE, and R2 scores between the predicted values and the actual values
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Return the scores as a dictionary
    return {"mse": mse, "mae": mae, "r2": r2}


def papas_perdidas(df):
    """
    Calculates the number and percentage of missing values in each column of a Pandas DataFrame.
    Args:
        df: A Pandas DataFrame.
    Returns:
        A new DataFrame that contains the number and percentage of missing values in each column.
    """
    # Count the number of missing values in each column
    missing_values = df.isnull().sum()

    # Calculate the percentage of missing values in each column
    missing_values_percentage = 100 * missing_values / len(df)

    # Combine the missing value counts and percentages into a single DataFrame
    missing_values_table = pd.concat(
        [missing_values, missing_values_percentage], axis=1)

    # Rename the columns of the new DataFrame
    missing_values_table.columns = ['Missing Values', 'Percentage']

    # Return the new DataFrame
    return missing_values_table


def correlation_papa(df, annot=True, figsize=(10, 10), cmap='coolwarm'):
    """
    Plots a correlation heatmap for the columns in a Pandas DataFrame.
    Args:
        df: A Pandas DataFrame.
        annot: Whether or not to display the correlation coefficients on the heatmap. Default is True.
        figsize: The size of the heatmap plot. Default is (10, 10).
        cmap: The color map to use for the heatmap. Default is 'coolwarm'.
    Returns:
        None.
    """
    # Calculate the correlation coefficients for the columns in the DataFrame
    corr = df.corr()

    # Create a new plot with the specified figure size
    plt.figure(figsize=figsize)

    # Create a heatmap plot of the correlation coefficients with the specified color map
    sns.heatmap(corr, annot=annot, cmap=cmap)

    # Display the plot
    plt.show()


def replace_outliers(df, f=1.5):
    """
    Reemplaza los valores atípicos en las columnas numéricas del DataFrame `df`
    con los límites inferior y superior. Los valores atípicos se definen como
    aquellos que se encuentran fuera del rango definido por el rango intercuartílico
    (IQR) multiplicado por el factor de escala `f`. Luego, la función convierte
    los valores numéricos a int o float según corresponda.

    Args:
        df (pandas.DataFrame): El DataFrame que se usará para reemplazar los valores atípicos.
        f (float, optional): El factor de escala para el rango intercuartílico.
            Por defecto es 1.5.

    Returns:
        pandas.DataFrame: El DataFrame `df` con los valores atípicos reemplazados y
        los valores numéricos convertidos.
    """

    # Selecciona solo las columnas numéricas
    numeric_cols = df.select_dtypes(include='number').columns

    # Calcula los cuartiles y el rango intercuartílico para cada columna numérica
    Q1 = df[numeric_cols].quantile(0.25)  # primer cuartil
    Q3 = df[numeric_cols].quantile(0.75)  # tercer cuartil
    IQR = Q3 - Q1  # rango intercuartílico
    lower_bound = Q1 - f * IQR  # límite inferior
    upper_bound = Q3 + f * IQR  # límite superior

    # Reemplaza los valores atípicos por los límites inferior y superior para cada columna numérica
    for col in numeric_cols:
        df.loc[df[col] < lower_bound[col], col] = lower_bound[col]
        df.loc[df[col] > upper_bound[col], col] = upper_bound[col]

    # Convierte los valores numéricos a int o float según corresponda
    if df[numeric_cols].applymap(lambda x: x.is_integer() if isinstance(x, float) else True).all().all():
        df[numeric_cols] = df[numeric_cols].astype(float)
    else:
        df[numeric_cols] = df[numeric_cols].astype(int)

    # Retorna el dataframe con los valores atípicos reemplazados y los valores numéricos convertidos
    return df
