import os
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI (optional - graceful fallback if not available)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def generate_bio_with_openai(prompt):
    """
    Generate developer bio using OpenAI API
    Falls back to template if API key not available
    """
    
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return None
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional technical writer who creates concise developer bios."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        bio = response.choices[0].message.content.strip()
        return bio
    
    except Exception as e:
        print(f"Error generating bio with OpenAI: {e}")
        return None

def generate_bio_template(insights):
    """
    Generate a template bio if AI is not available
    """
    
    top_langs = ', '.join(list(insights['top_languages'].keys()))
    
    bio = f"A {insights['primary_language']} developer with {insights['total_projects']} projects and {insights['total_stars']} total stars. " \
          f"Specializes in {top_langs}. Most successful project: {insights['most_successful_repo']} with {insights['most_successful_repo_stars']} stars."
    
    return bio

def get_developer_bio(insights):
    """
    Get developer bio from OpenAI or fallback to template
    """
    from analytics import generate_bio_prompt
    
    # Try OpenAI first
    prompt = generate_bio_prompt(insights)
    bio = generate_bio_with_openai(prompt)
    
    # Fallback to template
    if not bio:
        bio = generate_bio_template(insights)
    
    return bio