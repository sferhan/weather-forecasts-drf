/wait-for-postgres.sh
for db in ${POSTGRES12_DATABASE_NAMES}; do
	createuser -U postgres -s ${db}
	createdb -U postgres ${db} --owner=${db}
done