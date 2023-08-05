## download artifacts backend for auda-data-center

### local
```
python3 src/hc_upgrade_tools/skeleton.py dl-pkg \
--host=10.0.1.245 \
--port=7070 \
--project-system-id=auda-data-center \
--target-sub-folder-in-artifact=archive \
--project-dir=/Users/shixukai/Downloads/S004/data_center \
--token="FD0276C6-7B5D-4424-8B7D-F8CF7D7AC81C" \
--extra-symbolics "current/dock-compose.yml:shared/dock-compose.yml" \
"current/backend/config.js:shared/config.js" \
"current/backend/public:shared/public/" \
"current/.env:shared/.env"

```

### remote
```
hc_upgrade_tools dl-pkg \
--host=10.0.1.245 \
--port=7070 \
--project-system-id=auda-data-center \
--target-sub-folder-in-artifact=archive \
--project-dir=/home/deployer/Projects/data_center \
--token="FD0276C6-7B5D-4424-8B7D-F8CF7D7AC81C" \
--extra-symbolics "current/docker-compose.yml:shared/docker-compose.yml" \
"current/backend/config.js:shared/config.js" \
"current/backend/public:shared/public/" \
"current/.env:shared/.env" \
--restart-docker

```

## download artifacts backend for sort backend
```
hc_upgrade_tools dl-pkg \
--host=10.0.1.245 \
--port=7070 \
--project-system-id=hc_sort_upgrade_test \
--target-sub-folder-in-artifact=archive \
--project-dir=/home/deployer/Projects/hc_sort \
--token="FD0276C6-7B5D-4424-8B7D-F8CF7D7AC81C" \
--extra-symbolics "current/docker-compose.yml:shared/docker-compose.yml" \
"current/config:shared/config/" \
"current/public:shared/public/" \
"current/.env:shared/.env" \
--restart-docker
```