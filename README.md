# Do this once, if you haven't ever done this before:

git config --global core.editor nano

##############################################################################

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

##############################################################################

git pull
git commit -m "COMMIT MESSAGE"
# might need to do git add . , if you delete files, git rm FILENAME, then git commit -m "****"
git push -u origin master

##############################################################################
Things everyone should know:

gsumm.phds@gmail.com
nothingabouteverything
http://wordpress-gsumm.rhcloud.com/
http://gsumm.com/

Amazon MT:
gsumm.phds@gmail.com
kayurpetmeow

##############################################################################
wordpress
##############################################################################
MySQL 5.1 database added. Please make note of these credentials:

	Root User: adminhJKfuuU
	Root Password: hEK8eaf2ksiZ
	Database Name: wordpress

Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/

You can manage your new MySQL database by also embedding phpmyadmin. The
phpmyadmin username and password will be the same as the MySQL credentials
above.

##############################################################################
wordpresstest information
##############################################################################
MySQL 5.1 database added.  Please make note of these credentials:

       Root User: adminiKZ9HWA
   Root Password: aXjka9g-gDy9
   Database Name: wordpresstest

Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/

You can manage your new MySQL database by also embedding phpmyadmin.
The phpmyadmin username and password will be the same as the MySQL credentials above.

Making code changes
Install the Git client for your operating system, and from your command line run

git clone ssh://52916382e0b8cd6b2300001c@wordpresstest-gsumm.rhcloud.com/~/git/wordpresstest.git/
cd wordpresstest/
This will create a folder with the source code of your application. After making a change, add, commit, and push your changes.

git add .
git commit -m 'My changes'
git push
When you push changes the OpenShift server will report back its status on deploying your code. The server will run any of your configured deploy hooks and then restart the application.

# Accessing wordpress-test using FileZilla
From FileZilla, select SFTP from Preferences window
Host: sftp://wordpresstest-gsumm.rhcloud.com
Username: 52916382e0b8cd6b2300001c
Password: NA
Port: 22

Please make note of these MySQL credentials again:
  Root User: adminiKZ9HWA
  Root Password: aXjka9g-gDy9
URL: https://wordpresstest-gsumm.rhcloud.com/phpmyadmin/

##############################################################################
wordpresstest - Jenkins
##############################################################################
Building your Application

Associated with job 'wordpresstest-build' in Jenkins server.

Jenkins created successfully.  Please make note of these credentials:

   User: admin
   Password: sb54mK3gYKIF

Note:  You can change your password at: https://jenkins-gsumm.rhcloud.com/me/configure

Your application is now building with Jenkins.
OpenShift is configured to build this application with Jenkins when you make changes through Git. You can track the progress of builds through the following Jenkins job:

https://jenkins-gsumm.rhcloud.com/job/wordpresstest-build/

If you no longer wish to run Jenkins builds, you can remove the Jenkins cartridge.