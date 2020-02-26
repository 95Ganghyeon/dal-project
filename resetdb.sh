find ./dal/product/migrations/* ! -name "__init__.py" -delete
find ./dal/ranking/migrations/* ! -name "__init__.py" -delete
find ./dal/survey/migrations/* ! -name "__init__.py" -delete
find ./dal/user/migrations/* ! -name "__init__.py" -delete
echo "makemigrations, migrate은 직접 해주세용~~"
