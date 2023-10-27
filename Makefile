DC = docker compose
PRUNE = docker system prune
STORAGE_FILE = docker/storage.yaml
PGADMIN_FILE = docker/pgadmin.yaml


.PHONY: all
all:
	${DC} -f ${STORAGE_FILE} -f ${PGADMIN_FILE} up --build -d

.PHONY: drop-all
drop-all:
	${DC} -f ${STORAGE_FILE} -f ${PGADMIN_FILE} down

.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} up --build -d

.PHONY: drop-storage
drop-storage:
	${DC} -f ${STORAGE_FILE} down

.PHONY: pgadmin4
pgadmin4:
	${DC} -f ${PGADMIN_FILE} up --build -d

.PHONY: drop-pgadmin4
drop-pgadmin4:
	${DC} -f ${PGADMIN_FILE} down

.PHONY: logs-all
logs-all:
	${DC} -f ${STORAGE_FILE} -f ${PGADMIN_FILE} logs -f

.PHONY: logs-pgadmin4
logs-pgadmin4:
	${DC} -f ${PGADMIN_FILE} logs -f

.PHONY: logs-storage
logs-storage:
	${DC} -f ${STORAGE_FILE} logs -f

.PHONY: prune
prune:
	${PRUNE} -a