find ./dal/product/migrations/* ! -name "__init__.py" -delete
find ./dal/ranking/migrations/* ! -name "__init__.py" -delete
find ./dal/survey/migrations/* ! -name "__init__.py" -delete
find ./dal/user/migrations/* ! -name "__init__.py" -delete
find ./dal/board/migrations/* ! -name "__init__.py" -delete
rm ./dal/db.sqlite3
python3 ./dal/manage.py makemigrations
python3 ./dal/manage.py migrate
python3 ./dal/manage.py createsuperuser
