export LAMIN_SKIP_MIGRATION=true
export LAMIN_DEV="true"
export email="frederic.enard@gmail.com"
export password="D9lPqiw16FYELrrRnRvsKMv12V1F9DsP8JPqFiUR"
export storage="instance-test-1-storage"
export schema="bionty,wetlab,bfx"
export db="postgresql://postgres:lamin-data-admin-0@lamindata.ciwirckhwtkd.eu-central-1.rds.amazonaws.com:5432/lamindata"

lndb login $email --password $password
lndb init --storage $storage --schema $schema --db $db

python3 ./lndb_rest_instance/main.py
