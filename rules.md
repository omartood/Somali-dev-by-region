# 🤖 Cursor AI Prompt for Somali Developers by Region (City-Level Ranking)

## 🎯 Goal:
Automatically identify and rank **Somali GitHub developers** based on the cities in their profiles (e.g. "Mogadishu", "Hargeisa", "Kismayo"), and sort them by follower count. This will allow you to display:

- 📍 Somali developers by city
- 🏆 The most-followed GitHub users in each location
- 📊 Total developer count per region
- 🇸🇴 Somali flag and city badges in README

## 🧠 Cursor AI Role (Instructions)

```markdown
You are an AI agent generating regional GitHub developer insights. Please:

1. Use GitHub's REST API with query:
   - `location:Mogadishu`, `location:Hargeisa`, `location:Garowe`, etc.
   - Filter by `type:User` only (exclude bots/orgs)

2. For each city:
   - Collect up to 100 users
   - Retrieve:
     - Username
     - Followers count
     - GitHub profile link
     - Optional: bio, languages

3. Sort developers by follower count (highest → lowest)

4. Output to a single `README.md` with sections:
   ```markdown
   ## 📍 Mogadishu
   | Rank | Username | Followers | GitHub |
   |------|----------|-----------|--------|
   | 🥇 1 | @xuseen | 532 | https://github.com/xuseen |

   ## 📍 Hargeisa
   | Rank | Username | Followers | GitHub |
   ...
   ```

5. Add total dev count at the top:
   ```markdown
   ## 👥 Total Developers Tracked: 312
   ```

6. Cities to search:
   - Mogadishu
   - Hargeisa
   - Garowe
   - Kismayo
   - Baidoa
   - Bosaso
   - Beledweyne

7. Format city name with flag: `📍 Mogadishu 🇸🇴`

8. Update every 24 hours using GitHub Actions (cron job)

9. Use GitHub Token (GH_TOKEN) to avoid rate limits

10. Add last updated timestamp:
   ```markdown
   _Last updated: 2025-08-06_
   ```
```

---

## 🗂 Folder Structure

```bash
/somali-devs-by-region/
├── .github/workflows/city-rank.yml
├── generate_by_city.py
└── README.md
```

---

## 🔐 GitHub Secrets Required
- `GH_TOKEN`: GitHub Personal Access Token

---

## 💡 Bonus
- Optional: Include pie chart or bar graph by city
- Optional: Highlight newcomers (joined this year)
- Optional: Filter for active repos (pushed in last 30 days)

---

Let me know when you're ready to build the Python script or deploy the GitHub Action.
