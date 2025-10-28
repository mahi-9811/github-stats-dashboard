import pandas as pd
from database import get_all_projects

def calculate_developer_score(projects_data):
    """
    Calculate a developer score (0-100) based on various metrics
    """
    if not projects_data:
        return 0
    
    df = pd.DataFrame(projects_data, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
    
    # Calculate components (each weighted differently)
    
    # 1. Star Score (0-30 points) - total stars normalized
    # Use logarithmic scale for better distribution
    total_stars = df['Stars'].sum()
    import math
    star_score = min(30, math.log10(total_stars + 1) * 5)  # Logarithmic scale
    
    # 2. Activity Score (0-25 points) - based on commits
    total_commits = df['Commits'].sum()
    activity_score = min(25, math.log10(total_commits + 1) * 4)  # Logarithmic scale
    
    # 3. Diversity Score (0-20 points) - number of languages used
    languages = df['Language'].nunique()
    diversity_score = min(20, (languages / 15) * 20)  # 15 languages = 20 points
    
    # 4. Project Maturity Score (0-15 points) - average forks
    avg_forks = df['Forks'].mean()
    maturity_score = min(15, math.log10(avg_forks + 1) * 3)  # Logarithmic scale
    
    # 5. Consistency Score (0-10 points) - number of projects
    project_count = len(df)
    consistency_score = min(10, (project_count / 50) * 10)  # 50 projects = 10 points
    
    total_score = star_score + activity_score + diversity_score + maturity_score + consistency_score
    
    return {
        'total_score': round(total_score, 1),
        'star_score': round(star_score, 1),
        'activity_score': round(activity_score, 1),
        'diversity_score': round(diversity_score, 1),
        'maturity_score': round(maturity_score, 1),
        'consistency_score': round(consistency_score, 1)
    }

def get_developer_insights(projects_data):
    """
    Generate insights about the developer based on their repos
    """
    if not projects_data:
        return None
    
    df = pd.DataFrame(projects_data, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
    
    # Get top languages
    top_languages = df['Language'].value_counts().head(3).to_dict()
    
    # Get most successful repo
    best_repo = df.loc[df['Stars'].idxmax()]
    
    # Calculate metrics
    total_stars = df['Stars'].sum()
    total_commits = df['Commits'].sum()
    avg_stars = df['Stars'].mean()
    
    insights = {
        'total_projects': len(df),
        'total_stars': total_stars,
        'total_commits': total_commits,
        'avg_stars_per_project': round(avg_stars, 1),
        'top_languages': top_languages,
        'most_successful_repo': best_repo['Name'],
        'most_successful_repo_stars': best_repo['Stars'],
        'primary_language': df['Language'].mode()[0] if len(df['Language'].mode()) > 0 else 'Unknown'
    }
    
    return insights

def generate_bio_prompt(insights):
    """
    Generate a prompt for AI to create a developer bio
    """
    if not insights:
        return None
    
    top_langs = ', '.join(list(insights['top_languages'].keys()))
    
    prompt = f"""Based on the following GitHub profile data, write a short 2-3 sentence professional developer bio:

- Total Projects: {insights['total_projects']}
- Total Stars Across All Repos: {insights['total_stars']}
- Total Commits: {insights['total_commits']}
- Average Stars per Project: {insights['avg_stars_per_project']}
- Primary Languages: {top_langs}
- Most Successful Project: {insights['most_successful_repo']} ({insights['most_successful_repo_stars']} stars)
- Main Focus: {insights['primary_language']} developer

Write a professional, engaging bio that highlights their expertise and contributions. Keep it to 2-3 sentences."""
    
    return prompt