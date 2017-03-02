Release checklist
=================

Creating the release
--------------------
1. Grab the release name and number from [here](https://github.com/uktrade/data-hub/blob/master/releases-codenames.md)
1. Release branch created off develop at a given commit
2. Confirm CI is green on release branch
3. Confirm users have been made aware of scheduled downtime
4. Open PR release branch -> master on this repository (also update the release codenames table)
5. Merge release branch into master and tag it

Deploying the release
---------------------
6. Make sure someone is with you
7. Stop the celery workers
8. Trigger Jenkins job to release
9. Apply migrations manually (if needed)
10. Restart the celery workers
11. If release is successful, delete release branch
