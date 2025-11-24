# Step-by-Step: Creating GitHub Repository

## Step 1: Go to GitHub

1. Open your web browser
2. Go to: **https://github.com**
3. **Sign in** to your account (username: Anant-Madhok231)

## Step 2: Create New Repository

1. Click the **"+" icon** in the top right corner (next to your profile picture)
2. Select **"New repository"** from the dropdown menu

   OR

   Go directly to: **https://github.com/new**

## Step 3: Fill in Repository Details

Fill in the form with these exact settings:

### Repository name:
```
insider-trade-platform
```
*(You can use any name you want, but this is recommended)*

### Description (Optional):
```
Stock Market Analytics Platform with Insider Trade Ratio (ITR) calculation
```

### Visibility Options:
**Choose: Public** ✅
- This makes your code visible to everyone
- Required for free hosting on Render
- Your code will be publicly accessible

**OR choose: Private** (if you want to keep it private)
- Only you can see it
- You can still deploy to Render with private repos

### ⚠️ IMPORTANT: DO NOT CHECK THESE BOXES:
- ❌ **DO NOT** check "Add a README file" (we already have one)
- ❌ **DO NOT** check "Add .gitignore" (we already have one)
- ❌ **DO NOT** check "Choose a license" (optional, but skip for now)

**Leave all checkboxes UNCHECKED!**

### Final Settings Should Look Like:
```
Repository name: insider-trade-platform
Description: (optional - can leave blank)
Public ○  Private ●  (choose Public)
☐ Add a README file
☐ Add .gitignore
☐ Choose a license
```

## Step 4: Create Repository

1. Click the green **"Create repository"** button at the bottom

## Step 5: Copy the Repository URL

After creating, GitHub will show you a page with setup instructions.

**Copy this URL** (you'll see it on the page):
```
https://github.com/Anant-Madhok231/insider-trade-platform.git
```

## Step 6: Push Your Code

Now go back to your terminal and run these commands:

```bash
cd "/Users/anantmadhok/Desktop/insider 2 copy 2"

# Add the remote repository
git remote add origin https://github.com/Anant-Madhok231/insider-trade-platform.git

# Make sure you're on main branch
git branch -M main

# Push your code to GitHub
git push -u origin main
```

You'll be asked to enter your GitHub username and password/token:
- **Username**: Anant-Madhok231
- **Password**: Use a Personal Access Token (not your regular password)

### If you need to create a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "insider-trade-platform"
4. Select scopes: Check **"repo"** (this gives full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

## Step 7: Verify

After pushing, refresh your GitHub repository page. You should see all your files there!

## Visual Guide Summary

```
GitHub.com → Click "+" → New repository
↓
Repository name: insider-trade-platform
Visibility: Public ✅
Checkboxes: ALL UNCHECKED ❌
↓
Click "Create repository"
↓
Copy the repository URL
↓
Run git commands in terminal
↓
Done! 🎉
```

## Troubleshooting

**If you get "repository already exists" error:**
- Choose a different repository name
- Or delete the existing repository first

**If you get authentication error:**
- Make sure you're using a Personal Access Token, not your password
- Check that the token has "repo" permissions

**If files don't appear:**
- Make sure you ran `git add .` and `git commit` (already done!)
- Check that you're pushing to the correct remote URL

