1. Starting commands:
	- `dev init`
	- `dev start` 
---
2. After installing astro `brew install astro`
	- `astro dev init`
		- Makes a project with Dockerfile, test, requirements, packages, etc
	- `astro dev start`
		- Builds your deployment (I think)
---
3. Commands to get started
	- `astro dev start`
	- `astro dev start --no-browser`
	- `astro dev stop`
	- `astro dev pytest`
	- `astro help`
	- `astro dev ps`
	- `astro dev logs`
	- `astro wo create --name "AstronomerGirls"`
	- `astro deployment create -n "dev" -d "dev environment"`
	- `astro deployment list`
	- `astro deployment delete`
	- `astro deploy`
	- `docker container prune`
	- `docker ps`
	- `docker images`
	- `airflow scheudler`
---
4. To specify a custom `docker-compose.yml` file, use the `--compose-file` method
	- `astro dev start --compose-file ./path/to/custom-docker-compose.yml --env ./path/to/.env --no-browser`