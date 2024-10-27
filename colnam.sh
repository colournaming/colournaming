#!/usr/bin/env bash

set -eu -o pipefail

Help()
{
	# Display help
	echo "-u: Bring up test setup"
	echo "-r: Reinitialize the database"
	echo "-d: Tear down test setup"
	echo "-h: Print help message"
}

ImportTargets()
{
	docker compose run --rm web import-centroids docs/dataset_en.csv English en
	docker compose run --rm web import-col-targets targets.csv
	docker compose run --rm web import-colbg-targets colbg_targets.csv
	docker compose run --rm web import-colbg-backgrounds colbg_targets.csv
}


Up()
{
	# Bring up test setup
    	docker compose build
	docker compose up -d postgres
	docker compose run --rm web initdb
	ImportTargets
	docker compose up -d web
}

Reinit()
{
	# Reinitialize the database
	docker compose run --rm web dropdb
    	docker compose run --rm web initdb
	ImportTargets
}

Down()
{
	# Tear down test setup
   	docker compose down
}

if [[ $# != 1 ]]; then
      Help
      exit 1
fi

while getopts ":hurd:" option; do
      case $option in
      	   h) # display help
	      Help
	      exit;;
	   u) # bring up test setup
	      Up
	      exit;;
	   r) # reinitialize databse
	      Reinit
	      exit;;
	   d) # tear down test setup
	      Down
	      exit;;
	   \?) # Invalid option
	      echo "Error: Invalid argument"
	      exit 1;;
      esac
done 