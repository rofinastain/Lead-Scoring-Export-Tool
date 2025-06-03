import pandas as pd


def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a score for each lead based on several criteria.
    Maximum score is 10.

    Parameters:
        df (pd.DataFrame): DataFrame containing the leads data.

    Returns:
        pd.DataFrame: DataFrame with additional columns 'Score' and 'Score Label'.
    """

    def calculate_score(row: pd.Series) -> int:
        """
        Helper function to calculate the score per row.

        Parameters:
            row (pd.Series): A row from the DataFrame.

        Returns:
            int: The calculated score (max 10).
        """
        score = 0

        # Criteria 1: Revenue > 3M (Weight: 3)
        if row['Revenue ($M)'] > 3:
            score += 3

        # Criteria 2: Employees > 15 (Weight: 3)
        if row['Employees'] > 15:
            score += 3

        # Criteria 3: Industry is Fintech, Healthtech, or Edtech (Weight: 2)
        if row['Industry'] in ['Fintech', 'Healthtech', 'Edtech']:
            score += 2

        # Criteria 4: Location is San Francisco, NY, or LA (Weight: 2)
        if row['Location'] in ['San Francisco, CA', 'New York, NY', 'Los Angeles, CA']:
            score += 2

        return score

    # Add 'Score' column
    df['Score'] = df.apply(calculate_score, axis=1)

    # Add 'Score Label' column based on the score
    df['Score Label'] = df['Score'].apply(
        lambda x: 'High' if x >= 8 else ('Medium' if x >= 5 else 'Low')
    )

    return df