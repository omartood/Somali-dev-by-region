#!/usr/bin/env python3
"""
Somali GitHub Developers by City Ranking System
Fetches and ranks Somali developers from GitHub by their city location
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import os

class SomaliDevRanker:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv('GH_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Somali-Dev-Ranker'
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
        
        # Somali cities to search
        self.cities = [
            "Mogadishu", "Hargeisa", "Garowe", "Kismayo", 
            "Baidoa", "Bosaso", "Beledweyne"
        ]
    
    def search_developers_by_city(self, city: str, max_users: int = 100) -> List[Dict]:
        """Search for developers in a specific Somali city"""
        developers = []
        page = 1
        per_page = 30  # GitHub API limit
        
        print(f"🔍 Searching developers in {city}...")
        
        while len(developers) < max_users:
            try:
                url = f"{self.base_url}/search/users"
                params = {
                    'q': f'location:"{city}" type:user',
                    'sort': 'followers',
                    'order': 'desc',
                    'page': page,
                    'per_page': per_page
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 403:
                    print("⚠️ Rate limit hit, waiting...")
                    time.sleep(60)
                    continue
                
                if response.status_code != 200:
                    print(f"❌ Error fetching data for {city}: {response.status_code}")
                    break
                
                data = response.json()
                users = data.get('items', [])
                
                if not users:
                    break
                
                for user in users:
                    if len(developers) >= max_users:
                        break
                    
                    # Get detailed user info
                    user_details = self.get_user_details(user['login'])
                    if user_details:
                        developers.append(user_details)
                
                page += 1
                time.sleep(1)  # Be nice to GitHub API
                
            except Exception as e:
                print(f"❌ Error searching {city}: {str(e)}")
                break
        
        print(f"✅ Found {len(developers)} developers in {city}")
        return developers
    
    def get_user_details(self, username: str) -> Optional[Dict]:
        """Get detailed information for a specific user"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                return None
            
            user_data = response.json()
            
            return {
                'username': user_data['login'],
                'followers': user_data['followers_count'] or 0,
                'following': user_data['following_count'] or 0,
                'public_repos': user_data['public_repos'] or 0,
                'bio': user_data.get('bio', ''),
                'location': user_data.get('location', ''),
                'github_url': user_data['html_url'],
                'avatar_url': user_data['avatar_url'],
                'created_at': user_data['created_at']
            }
        except Exception as e:
            print(f"❌ Error fetching user {username}: {str(e)}")
            return None
    
    def generate_readme(self, city_developers: Dict[str, List[Dict]]) -> str:
        """Generate the README.md content"""
        total_devs = sum(len(devs) for devs in city_developers.values())
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        readme_content = f"""# 🇸🇴 Somali GitHub Developers by City

> Ranking the most-followed Somali developers on GitHub by their city location

## 👥 Total Developers Tracked: {total_devs}

_Last updated: {current_date}_

---

"""
        
        for city in self.cities:
            developers = city_developers.get(city, [])
            if not developers:
                continue
            
            # Sort by followers (highest first)
            developers.sort(key=lambda x: x['followers'], reverse=True)
            
            readme_content += f"## 📍 {city} 🇸🇴\n\n"
            readme_content += f"**{len(developers)} developers found**\n\n"
            readme_content += "| Rank | Developer | Followers | Repos | GitHub Profile |\n"
            readme_content += "|------|-----------|-----------|-------|----------------|\n"
            
            for i, dev in enumerate(developers[:20], 1):  # Top 20 per city
                rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}"
                username = dev['username']
                followers = dev['followers']
                repos = dev['public_repos']
                github_url = dev['github_url']
                
                readme_content += f"| {rank_emoji} | **{username}** | {followers} | {repos} | [Profile]({github_url}) |\n"
            
            readme_content += "\n---\n\n"
        
        # Add footer
        readme_content += """## 📊 About This Project

This repository automatically tracks and ranks Somali GitHub developers by their city location. The data is updated daily using GitHub's REST API.

### 🏙️ Cities Tracked
- 📍 Mogadishu 🇸🇴
- 📍 Hargeisa 🇸🇴  
- 📍 Garowe 🇸🇴
- 📍 Kismayo 🇸🇴
- 📍 Baidoa 🇸🇴
- 📍 Bosaso 🇸🇴
- 📍 Beledweyne 🇸🇴

### 🤝 Contributing
Found a bug or want to add a new city? Feel free to open an issue or submit a pull request!

### 📝 License
This project is open source and available under the MIT License.

---

**Made with ❤️ for the Somali developer community**
"""
        
        return readme_content
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting Somali Developer City Ranking...")
        
        city_developers = {}
        
        for city in self.cities:
            developers = self.search_developers_by_city(city)
            if developers:
                city_developers[city] = developers
        
        # Generate README
        readme_content = self.generate_readme(city_developers)
        
        # Write to file
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README.md generated successfully!")
        print(f"📊 Total developers found: {sum(len(devs) for devs in city_developers.values())}")

if __name__ == "__main__":
    ranker = SomaliDevRanker()
    ranker.run()