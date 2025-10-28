import sqlite3
from datetime import datetime

DB_FILE = 'portfolio.db'

# Initialize database on first run
def init_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        stars INTEGER DEFAULT 0,
        forks INTEGER DEFAULT 0,
        language TEXT,
        commits INTEGER DEFAULT 0,
        url TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Track star/fork history for growth analytics
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        stars INTEGER DEFAULT 0,
        forks INTEGER DEFAULT 0,
        commits INTEGER DEFAULT 0,
        recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # Add missing columns to existing table if they don't exist
    try:
        cursor.execute('ALTER TABLE projects ADD COLUMN updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

# Initialize on import
init_db()

def get_connection():
    """Create a new database connection"""
    conn = sqlite3.connect(DB_FILE)
    return conn

def add_project(name, description, stars, forks, language, commits, url):
    """Add a new project to database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO projects (name, description, stars, forks, language, commits, url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, description, stars, forks, language, commits, url))
    
    project_id = cursor.lastrowid
    
    # Record initial metrics in history
    cursor.execute('''
    INSERT INTO project_history (project_id, stars, forks, commits)
    VALUES (?, ?, ?, ?)
    ''', (project_id, stars, forks, commits))
    
    conn.commit()
    conn.close()
    return True

def get_all_projects():
    """Get all projects from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name, description, stars, forks, language, commits, url, created_date, updated_date 
    FROM projects 
    ORDER BY stars DESC
    ''')
    projects = cursor.fetchall()
    
    conn.close()
    return projects

def delete_project(project_id):
    """Delete a project by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM project_history WHERE project_id = ?', (project_id,))
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    return True

def update_project(project_id, name, description, stars, forks, language, commits, url):
    """Update an existing project"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE projects 
    SET name=?, description=?, stars=?, forks=?, language=?, commits=?, url=?, updated_date=CURRENT_TIMESTAMP
    WHERE id=?
    ''', (name, description, stars, forks, language, commits, url, project_id))
    
    # Record metrics update in history
    cursor.execute('''
    INSERT INTO project_history (project_id, stars, forks, commits)
    VALUES (?, ?, ?, ?)
    ''', (project_id, stars, forks, commits))
    
    conn.commit()
    conn.close()
    return True

def get_total_stats():
    """Get summary statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT 
        COUNT(*) as total_projects,
        SUM(stars) as total_stars,
        SUM(forks) as total_forks,
        SUM(commits) as total_commits
    FROM projects
    ''')
    stats = cursor.fetchone()
    conn.close()
    
    return {
        'total_projects': stats[0] or 0,
        'total_stars': stats[1] or 0,
        'total_forks': stats[2] or 0,
        'total_commits': stats[3] or 0
    }

def get_language_breakdown():
    """Get project count by language"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT language, COUNT(*) as count, SUM(stars) as stars
    FROM projects
    GROUP BY language
    ORDER BY count DESC
    ''')
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_project_history(project_id):
    """Get historical data for a specific project"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT recorded_date, stars, forks, commits
    FROM project_history
    WHERE project_id = ?
    ORDER BY recorded_date ASC
    ''', (project_id,))
    
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_top_projects(limit=5):
    """Get top projects by stars"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT name, stars, forks, commits, language
    FROM projects
    ORDER BY stars DESC
    LIMIT ?
    ''', (limit,))
    
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_average_metrics_by_language():
    """Get average stats per project by language"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT language, 
           AVG(stars) as avg_stars,
           AVG(forks) as avg_forks,
           AVG(commits) as avg_commits,
           COUNT(*) as project_count
    FROM projects
    GROUP BY language
    ORDER BY project_count DESC
    ''')
    
    result = cursor.fetchall()
    conn.close()
    
    return result

def get_portfolio_growth():
    """Get total stats over time"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT recorded_date, 
           SUM(stars) as total_stars,
           SUM(forks) as total_forks,
           SUM(commits) as total_commits,
           COUNT(DISTINCT project_id) as project_count
    FROM project_history
    GROUP BY recorded_date
    ORDER BY recorded_date ASC
    ''')
    
    result = cursor.fetchall()
    conn.close()
    
    return result