#!/bin/bash

echo "Running tests"

# luodaan tietokanta
poetry run python src/db_helper.py

echo "DB setup done"

# käynnistetään Flask-palvelin taustalle
poetry run python3 src/index.py &

echo "started Flask server"

# odetetaan, että palvelin on valmiina ottamaan vastaan pyyntöjä
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5001)" != "200" ]];
  do sleep 1;
done

echo "Flask server is ready"

# tarkistetaan, onko testitiedostoja olemassa
# resource.robot ignorataan, katsotaan, onko .robot-tiedostoja *** Test Cases *** -osiolla
test_files=$(find src/story_tests -type f -name "*.robot" -exec grep -l "*** Test Cases ***" {} +)

if [[ -n "$test_files" ]]; then
  echo "Found Robot Framework test files. Running tests..."
  # suoritetaan testit
  poetry run robot --variable HEADLESS:true src/story_tests
  status=$?
else
  echo "No Robot Framework test cases found. Skipping tests."
  status=0
fi

# pysäytetään Flask-palvelin portissa 5001
kill $(lsof -t -i:5001)

exit $status
