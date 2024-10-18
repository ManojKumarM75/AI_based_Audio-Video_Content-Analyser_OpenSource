@echo off
echo Git Add, Commit, and Push Script

:: Add all changes
git add .

:: Prompt for commit message
set /p commit_message=Enter commit message: 

:: Commit changes
git commit -m "%commit_message%"

:: Push to remote repository
git push origin main

echo Push completed.
pause
