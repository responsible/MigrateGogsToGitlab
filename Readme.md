# Migrate Gogs to Gitlab

## Prerequisites
+ Gogs repo excluded backup

  > On gogs server, run:
  ```shell
  gogs run backup --exclude-repo
  ```
  then unzip backup file, copy **gogs-backup** folder to current migration script folder.

+ Make sure the user in gogs you use to export repo have the access to pull all projects.

+ You have set up gitlab server and have generate **private token**

+ Update following variable in **variables.py**:

  **GOGS_DB_FOLDER** (The gogs backup file folder)
  
  **PRIVATE_TOKEN** (Gitlab root user private token)
  
  **BASE_URL** (Gitlab server url, just replace domain, don't delete 'api/v4...')
  
  **GOGS_REPO_URL** (Gogs server url with gogs username and password)
  
  **USER_PASSWD** (Gitlab imported user's new password)

## Run

```shell
python3 run_import.py
```

## Tips

For mirror repository, you can export config by running **list_all_mirror_repo.sh** on your gogs server, and update them by running **update_mirror.sh** on gitlab server.
