# Do this once, if you haven't ever done this before:

git config --global core.editor nano

# Our current workflow:

git fetch
git checkout development
git pull
git checkout -b new_branch_name # (example: tvdev)
git push origin new_branch_name

# Do what you need to do here, commits, etc.
# git commit -m "COMMIT MESSAGE HERE"

git push origin new_branch_name
git checkout development
git merge origin/new_branch_name
git push origin development

# If you get an error here, then do a 'git pull'; it will throw you into a
# text editor to enter a commit message; do this then run
# 'git push origin development' again.

git push origin :new_branch_name
git branch -D new_branch_name

git pull
git commit -m "COMMIT MESSAGE"
# might need to do git add . , if you delete files, git rm FILENAME, then git commit -m "****"
git push -u origin master

#Making code changes
Install the Git client for your operating system, and from your command line run

git clone ssh://52916382e0b8cd6b2300001c@wordpresstest-gsumm.rhcloud.com/~/git/wordpresstest.git/
cd wordpresstest/
This will create a folder with the source code of your application. After making a change, add, commit, and push your changes.

git add .
git commit -m 'My changes'
git push
When you push changes the OpenShift server will report back its status on deploying your code. The server will run any of your configured deploy hooks and then restart the application.