ENV_FILE := .env

# Read the .env file and create variables
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

duckdb:
	export DUCKDB_ENABLED=true && \
		export SNOWFLAKE_ENABLED=false && \
		export DEFAULT_DIALECT=duckdb && \
		sqlmesh --gateway duckdb $(cmd)

snowflake:
	export DUCKDB_ENABLED=false && \
		export SNOWFLAKE_ENABLED=true && \
		export DEFAULT_DIALECT=snowflake && \
		sqlmesh --gateway snowflake $(cmd)