# insights_app/views.py

import os
from django.shortcuts import render
from .analytics import (
    load_data,
    generate_wordcloud,
    plot_impressions_over_time,
    plot_interaction_distribution,
    plot_correlation_matrix,
    plot_relationship,
    evaluate_model,
    ensure_output_dir
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dashboard(request):
    # Define paths
    data_path = os.path.join(BASE_DIR, 'insights_app', 'static', 'insights_app', 'Instagram data.csv')
    output_dir = os.path.join(BASE_DIR, 'insights_app', 'static', 'insights_app', 'images')
    ensure_output_dir(output_dir)

    # Load and process data
    df = load_data(data_path)

    # Generate wordclouds
    generate_wordcloud(df['Caption'], os.path.join(output_dir, 'caption_wc.png'))
    generate_wordcloud(df['Hashtags'], os.path.join(output_dir, 'hashtag_wc.png'))

    # Generate visualizations
    plot_interaction_distribution(df, output_dir)
    plot_correlation_matrix(df, os.path.join(output_dir, 'correlation_matrix.png'))
    plot_relationship(df, 'Likes', 'Impressions', os.path.join(output_dir, 'likes_vs_impressions.png'), 'Likes vs Impressions')
    plot_relationship(df, 'Profile Visits', 'Follows', os.path.join(output_dir, 'profile_vs_follows.png'), 'Profile Visits vs Follows')
    plot_relationship(df, 'Comments', 'Impressions', os.path.join(output_dir, 'comments_vs_impressions.png'), 'Comments vs Impressions')
    plot_relationship(df, 'Saves', 'Impressions', os.path.join(output_dir, 'saves_vs_impressions.png'), 'Saves vs Impressions')

    # Model evaluation (dummy)
    y_true = df['Impressions']
    y_pred = df['Likes']
    metrics = evaluate_model(y_true, y_pred)
    metrics['TT'] = '0.12s'  # Training time, hardcoded

    # Add metrics for Overview tab
    metrics['total_posts'] = len(df)
    metrics['total_impressions'] = int(df['Impressions'].sum())
    metrics['total_likes'] = int(df['Likes'].sum())
    metrics['top_hashtag'] = df['Hashtags'].mode()[0] if not df['Hashtags'].mode().empty else 'N/A'

    # Add trend chart data
    try:
        trend_df = df.groupby('Date')['Impressions'].sum().reset_index()
        metrics['reach_trend'] = {
            'labels': list(trend_df['Date'].astype(str)),
            'data': list(trend_df['Impressions'])
        }
    except Exception as e:
        metrics['reach_trend'] = {'labels': [], 'data': []}

    # List of plot paths for the frontend
    plots = [
        'insights_app/images/caption_wc.png',
        'insights_app/images/hashtag_wc.png',
        'insights_app/images/interactions_distribution.png',
        'insights_app/images/correlation_matrix.png',
        'insights_app/images/likes_vs_impressions.png',
        'insights_app/images/profile_vs_follows.png',
        'insights_app/images/comments_vs_impressions.png',
        'insights_app/images/saves_vs_impressions.png'
    ]

    return render(request, 'insights_app/dashboard.html', {'plots': plots, 'metrics': metrics})
