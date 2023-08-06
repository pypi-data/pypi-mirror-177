rm -rf .gitlab-ci.yml test setup.cfg setup.py docs linksaas_local_api git_push.sh README.md test-requirements.txt tox.ini src
npx @openapitools/openapi-generator-cli generate -c config.json -i proto/index_0.1.3.yml -g python-prior -o .
rm -rf .gitlab-ci.yml test setup.cfg setup.py docs git_push.sh README.md test-requirements.txt tox.ini
mkdir src
mv linksaas_local_api src/
cp API_README.md README.md