import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import (
    add_project, get_all_projects, delete_project, 
    get_total_stats, get_language_breakdown,
    get_top_projects, get_average_metrics_by_language
)
from analytics import calculate_developer_score, get_developer_insights
from ai_helper import get_developer_bio
from pdf_report import generate_pdf_report
from github_api import sync_github_repos_to_db
import database

st.set_page_config(page_title="GitHub Stats Dashboard", layout="wide")

st.title("📊 GitHub Stats Dashboard")
st.write("Analyze any GitHub user's repositories, performance metrics, and insights")
st.caption("Built with Streamlit, Python, and GitHub API")

# Main search interface
st.sidebar.title("Search")
github_username = st.sidebar.text_input("Enter GitHub Username", placeholder="e.g., torvalds, guido, facebook")

if st.sidebar.button("📊 Analyze User", use_container_width=True):
    if github_username:
        # Clear previous data
        projects = get_all_projects()
        for project in projects:
            delete_project(project[0])
        
        # Fetch new user's repos
        with st.spinner(f"Analyzing {github_username}'s repositories..."):
            success, message = sync_github_repos_to_db(database, github_username)
            if success:
                st.sidebar.success(message)
                st.rerun()
            else:
                st.sidebar.error(message)
    else:
        st.sidebar.error("Please enter a GitHub username!")

# Display analysis
projects = get_all_projects()

if not projects:
    st.info("👈 Enter a GitHub username in the sidebar to get started!")
else:
    # Calculate score and insights
    score_data = None
    insights = None
    bio = None
    
    if calculate_developer_score:
        try:
            score_data = calculate_developer_score(projects)
            insights = get_developer_insights(projects)
        except Exception as e:
            st.sidebar.warning(f"Could not calculate score: {e}")
    
    if get_developer_bio and insights:
        try:
            bio = get_developer_bio(insights)
        except Exception as e:
            st.sidebar.warning(f"Could not generate bio: {e}")
    
    # Show current user
    st.sidebar.divider()
    st.sidebar.write(f"**Currently analyzing:** `{github_username}`")
    
    # Download PDF button
    if generate_pdf_report and score_data and insights:
        try:
            pdf_buffer = generate_pdf_report(github_username, projects, score_data, insights, bio)
            st.sidebar.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"{github_username}_github_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.sidebar.error(f"Error generating PDF: {e}")
    
    # ============ OVERVIEW ============
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analytics", "📋 Projects", "🔬 Detailed Analysis"])
    
    with tab1:
        st.subheader(f"Repository Statistics for @{github_username}")
        
        # Developer Score Card
        if score_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Developer Score", f"{score_data['total_score']}/100")
            with col2:
                st.metric("Star Score", f"{score_data['star_score']}/30")
            with col3:
                st.metric("Activity Score", f"{score_data['activity_score']}/25")
            
            st.divider()
        
        # AI Generated Bio
        if bio:
            st.subheader("🤖 AI-Generated Developer Bio")
            st.info(bio)
            st.divider()
        
        stats = get_total_stats()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Repositories", stats['total_projects'])
        with col2:
            st.metric("Total Stars", stats['total_stars'])
        with col3:
            st.metric("Total Forks", stats['total_forks'])
        with col4:
            st.metric("Total Commits", stats['total_commits'])
        
        st.divider()
        
        # Overview charts
        df = pd.DataFrame(projects, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Most Starred Repositories")
            top_repos = df.nlargest(10, 'Stars')[['Name', 'Stars']]
            fig = px.bar(top_repos, x='Stars', y='Name', orientation='h', 
                        color='Stars', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Languages Used")
            lang_data = pd.DataFrame(get_language_breakdown(), columns=['Language', 'Count', 'Total_Stars'])
            fig = px.pie(lang_data, values='Count', names='Language', 
                        title="Repository Distribution by Language")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Detailed Analytics")
        
        df = pd.DataFrame(projects, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_stars = df['Stars'].mean()
            st.metric("Average Stars per Repository", f"{avg_stars:.1f}")
        with col2:
            avg_commits = df['Commits'].mean()
            st.metric("Average Commits per Repository", f"{avg_commits:.1f}")
        with col3:
            avg_forks = df['Forks'].mean()
            st.metric("Average Forks per Repository", f"{avg_forks:.1f}")
        
        st.divider()
        
        # Distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stars Distribution")
            fig = px.histogram(df, x='Stars', nbins=15, 
                             color_discrete_sequence=['#3b82f6'],
                             title="How are stars distributed across repositories?")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Commits Distribution")
            fig = px.histogram(df, x='Commits', nbins=15,
                             color_discrete_sequence=['#10b981'],
                             title="How are commits distributed?")
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Scatter plot
        st.subheader("Stars vs Commits Correlation")
        fig = px.scatter(df, x='Commits', y='Stars', size='Forks', 
                        hover_data=['Name', 'Language'],
                        color='Language', 
                        title="Relationship between commits and stars")
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Language analysis
        st.subheader("Average Metrics by Language")
        lang_stats = get_average_metrics_by_language()
        lang_df = pd.DataFrame(lang_stats, columns=['Language', 'Avg Stars', 'Avg Forks', 'Avg Commits', 'Projects'])
        
        fig = px.bar(lang_df, x='Language', y=['Avg Stars', 'Avg Forks'], 
                    barmode='group',
                    title="Average performance by language")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(lang_df, use_container_width=True)
    
    with tab3:
        st.subheader("📋 Repository List")
        
        df = pd.DataFrame(projects, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
        
        # Search/filter
        search = st.text_input("Search repositories", placeholder="Filter by name or language...")
        
        if search:
            df = df[(df['Name'].str.contains(search, case=False)) | 
                   (df['Language'].str.contains(search, case=False))]
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Stars (Highest)", "Commits (Most)", "Forks (Most)", "Name (A-Z)"])
        
        if sort_by == "Stars (Highest)":
            df = df.sort_values('Stars', ascending=False)
        elif sort_by == "Commits (Most)":
            df = df.sort_values('Commits', ascending=False)
        elif sort_by == "Forks (Most)":
            df = df.sort_values('Forks', ascending=False)
        else:
            df = df.sort_values('Name')
        
        # Display projects
        for idx, row in df.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"### [{row['Name']}]({row['URL']})")
                if row['Description']:
                    st.write(row['Description'])
                st.caption(f"Language: {row['Language']}")
            
            with col2:
                st.write(f"⭐ **{row['Stars']}**")
                st.write(f"🔀 **{row['Forks']}**")
                st.write(f"📝 **{row['Commits']}**")
            
            st.divider()
    
    with tab4:
        st.subheader("🔬 Advanced Analysis")
        
        df = pd.DataFrame(projects, columns=['ID', 'Name', 'Description', 'Stars', 'Forks', 'Language', 'Commits', 'URL', 'Created', 'Updated'])
        
        # Calculate efficiency metrics
        df['Stars_per_Commit'] = (df['Stars'] / (df['Commits'] + 1)).round(2)
        df['Forks_per_Star'] = (df['Forks'] / (df['Stars'] + 1)).round(3)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Most Efficient (Stars per Commit)")
            efficient = df[['Name', 'Stars', 'Commits', 'Stars_per_Commit']].sort_values('Stars_per_Commit', ascending=False).head(10)
            fig = px.bar(efficient, x='Stars_per_Commit', y='Name', orientation='h',
                        color='Stars_per_Commit', color_continuous_scale='RdYlGn',
                        title="Which repos get stars with minimal commits?")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("👥 Most Forked (Relative to Stars)")
            forked = df[['Name', 'Stars', 'Forks', 'Forks_per_Star']].sort_values('Forks_per_Star', ascending=False).head(10)
            fig = px.bar(forked, x='Forks_per_Star', y='Name', orientation='h',
                        color='Forks_per_Star', color_continuous_scale='Blues',
                        title="Which repos are forked most relative to stars?")
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.subheader("📊 Detailed Metrics Table")
        display_df = df[['Name', 'Stars', 'Commits', 'Forks', 'Language', 'Stars_per_Commit', 'Forks_per_Star']].copy()
        display_df = display_df.sort_values('Stars', ascending=False)
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
        
        st.divider()
        
        # Summary insights
        st.subheader("💡 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            most_starred = df.loc[df['Stars'].idxmax()]
            st.write(f"**Most Starred Repository:**")
            st.write(f"`{most_starred['Name']}`")
            st.write(f"⭐ {most_starred['Stars']} stars")
        
        with col2:
            most_forked = df.loc[df['Forks'].idxmax()]
            st.write(f"**Most Forked Repository:**")
            st.write(f"`{most_forked['Name']}`")
            st.write(f"🔀 {most_forked['Forks']} forks")
        
        with col3:
            most_commits = df.loc[df['Commits'].idxmax()]
            st.write(f"**Most Active Repository:**")
            st.write(f"`{most_commits['Name']}`")
            st.write(f"📝 {most_commits['Commits']} commits")