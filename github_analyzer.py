import pandas as pd
import requests as rq

def fetch_all_repos(username):
    """Fetches all public repositories for a given GitHub username."""
    print(f"Fetching repositories for {username}...")
    
    # The starting point for the GitHub API
    api_url = f"https://api.github.com/users/{username}/repos"
    
    # It's good practice to send a User-Agent header
    headers = {'User-Agent': 'GitHub Repo Analyzer'}
    
    all_repos = []
    page = 1
    
    while True:
        # We'll add a 'per_page' parameter to get the max amount (100)
        enter = {'per_page': 100, 'page': page}
        
        try:
            response = rq.get(api_url,  params=enter,headers=headers)
            response.raise_for_status() # Check for errors
            
            data = response.json()
            
            # If the page has no data, we've reached the end
            if not data:
                break
            
            all_repos.extend(data)
            page += 1
            
        except rq.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
            
    return all_repos

def analyze_repos(repos_data):
    """Processes the raw repo data and prints a summary using pandas."""
    if not repos_data:
        print("No repositories found or an error occurred.")
        return

    # Extract only the information we care about
    processed_repos = []
    for repo in repos_data:
        processed_repos.append({
            'name': repo['name'],
            'language': repo['language'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count']
        })
        
    # Create a pandas DataFrame from our list of dictionaries
    df = pd.DataFrame(processed_repos)
    
    print(f"\n--- Analysis for {len(df)} repositories ---")
    
    # 1. Show the top 5 most starred repositories
    print("\nTop 5 Most Starred Repositories:")
    top_starred = df.sort_values(by='stars', ascending=False).head(5)
    print(top_starred[['name', 'stars', 'language']])
    
    # 2. Show a summary of languages used
    print("\nPrimary Languages Used:")
    language_counts = df['language'].value_counts().dropna() # dropna removes 'None' languages
    print(language_counts)

# --- Main part of the script ---
if __name__ == "__main__":
    github_username = input("Enter the GitHub username to analyze: ")
    
    # Step 1: Fetch all the repository data
    all_repos_data = fetch_all_repos(github_username)
    
    # Step 2: Process and analyze the data
    if all_repos_data:
        analyze_repos(all_repos_data)