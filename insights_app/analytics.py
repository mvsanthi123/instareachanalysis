# insights_app/analytics.py
print("Analytics file loaded successfully")
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_squared_log_error,
    mean_absolute_percentage_error
)
import os

# Ensure plots directory exists
def ensure_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Load and preprocess dataset
def load_data(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    df.columns = df.columns.str.strip()
    df.fillna(0, inplace=True)
    return df

# Generate a word cloud from a column
def generate_wordcloud(data_column, output_path):
    text = " ".join(data_column.astype(str))
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path)
    plt.close()

# Plot impressions over time
def plot_impressions_over_time(df, output_path):
    plt.figure(figsize=(10, 6))
    df.groupby('Date')['Impressions'].sum().plot()
    plt.title("Impressions Over Time")
    plt.xlabel("Date")
    plt.ylabel("Impressions")
    plt.grid()
    plt.savefig(output_path)
    plt.close()

# Pie chart and bar chart for interaction distribution
def plot_interaction_distribution(df, output_dir):
    interactions = df[['Likes', 'Comments', 'Shares', 'Saves']].sum()
    
    plt.figure(figsize=(6, 6))
    interactions.plot.pie(autopct='%1.1f%%')
    plt.title("Interaction Distribution (Pie)")
    plt.ylabel("")
    plt.savefig(os.path.join(output_dir, 'interaction_pie.png'))
    plt.close()

    plt.figure(figsize=(8, 6))
    interactions.plot.bar(color='skyblue')
    plt.title("Interaction Distribution (Bar)")
    plt.ylabel("Count")
    plt.savefig(os.path.join(output_dir, 'interaction_bar.png'))
    plt.close()

# Correlation heatmap
def plot_correlation_matrix(df, output_path):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.savefig(output_path)
    plt.close()

# Relationship plots
def plot_relationship(df, x, y, output_path, title):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig(output_path)
    plt.close()

# Evaluate regression model
def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    rmsle = np.sqrt(mean_squared_log_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'RMSLE': rmsle,
        'MAPE': mape
    }

# (Optional test usage block)
if __name__ == '__main__':
    df = load_data('static/insights_app/images/Instagram data.csv')
    ensure_output_dir('static/insights_app/images')

    generate_wordcloud(df['Caption'], 'static/insights_app/images/caption_wc.png')
    generate_wordcloud(df['Hashtags'], 'static/insights_app/images/hashtag_wc.png')

    plot_impressions_over_time(df, 'static/insights_app/images/impressions.png')
    plot_interaction_distribution(df, 'static/insights_app/images')
    plot_correlation_matrix(df, 'static/insights_app/images/correlation_matrix.png')

    plot_relationship(df, 'Likes', 'Impressions', 'static/insights_app/images/likes_vs_reach.png', 'Likes vs Impressions')
    plot_relationship(df, 'Profile Visits', 'Follows', 'static/insights_app/images/profile_vs_follows.png', 'Profile Visits vs Follows')
    plot_relationship(df, 'Comments', 'Impressions', 'static/insights_app/images/comments_vs_impressions.png', 'Comments vs Impressions')
    plot_relationship(df, 'Saves', 'Impressions', 'static/insights_app/images/saves_vs_impressions.png', 'Saves vs Impressions')
