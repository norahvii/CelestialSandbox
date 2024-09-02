1. Resources are handled by Kubernetes 
	- That means you will need to reference their documentation to learn more
2. Starting commands:
	- `dev init`
	- `dev start` 
![[Pasted image 20240820152217.png]]
---
3. After installing astro `brew install astro`
	- `astro dev init`
		- Makes a project with Dockerfile, test, requirements, packages, etc
	- `astro dev start`
		- Builds your deployment (I think)
---
4. Core components of Airflow
	1. Web Server
	2. Scheduler
	3. Metastore
		- Metadata related to users, jobs or data pipelines
	4. Triggerer
		- A thing that lets you deal with special tasks
	5. Executor
		- Defines how and on which system to execute your tasks
	6. Queue
		- Task execution order
	7. Worker
		- Executes tasks
---
5. Core concepts
	1. DAG: directed acyclic graph
		- To Airflow: a data pipeline
	2. Airflow is modular
		- You can add things to it, like Dbt, AWS, Snowflake,etc
	3. Task instance 
---
6. Views
	1. Landing Times View
		- Optimize your tasks
	2. Grid View
		- Historical states of DAG runs
	3. Ganett View
		- Identify bottlenecks in your DAG
	4. Calendar View
		- View to spot repetitive patterns over many DAG runs
	5. Recent Tasks column of Dag View Show
		- Current or latest DAG run for a given DAG
---
7. DAG runs
	1. state
		- Final DAG Run's state
	2. DAG id
		- DAG ID of DAG
	3. logical date
		- Data interval start
	4. start date
		- Start timestamp
	5. start interval
		- schedule DAGs
		- use `timedate object` for odd days, such as 3 days
---
8. Catchup
	- A parameter that has your DAG runs catch up 
		- Runs all the scheduled non-triggered DAG runs between now and the start date
		- When `catchup=False`, Airflow does not backfill missed runs. Instead, it only triggers the DAG for the most recent interval that has not been run. This means if your DAG was defined with a start date 30 days ago but has never run, only the latest interval (the current date) will be triggered [4](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html).

NOTE(s):
1. DAG runs are based on the **end of the data interval**
2. In Airflow, the `execution_date` (also known as `logical_date`) is indeed the same as the `data_interval_start`. This date represents the start of the interval for which the DAG run is processing data, not the actual time when the DAG run is executed [5](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html).
---
9. Templating
	- [Templates reference — Airflow Documentation (apache.org)](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)
	- Variables, macros and filters can be used in templates (see the [Jinja Templating](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#concepts-jinja-templating) section)
	- Also allows you to add SQL data requests, very cool.
---
10. XCOMs
	- Background: External systems are used for getting data from one system into another. Using XCOMs allow you not to rely on external systems. Instead, you would use an Airflow Meta Database.
	- Properties (value and timestamp do not define uniqueness of an XCOM):
		- `key`: XCOM identifier, its name
		- `value`: JSON serializable value
		- `task_id`: From which task the XCOM was created
		- `dag_id`: From which DAG the XCOM was created
		- `timestamp`: When the XCOM was created
		- `logical_date/execution_date`: DAG Run `data_interval_start`
	- Airflow GUI supports logging for XCOM activity
	- It is possible to pull an XCOM with a specific key, maybe with the `ti.xcom_push` method
		- `ti`: This is the task instance object
		- You can do XCOM push or XCOM pull etc. 
			- `xcom_pull`: allows you to pull multiple values at once 
	- Limitations:
		- Pushes and pulls go to and from the Airflow Database
		- SQLite: 2GB per XCOM
		- Postgres: 1GB per XCOM
		- MySQL: 64MB per XCOM
		- Data shared with XCOMs must be JSON serializable 
---
11. Logging into workspaces via the Astro CLI
	- Worked for me: `astro login -login-link`
		- Click the link to login
	- You'll need to create a workspace and an organization ID first on the website
	- Creating the organization on the website seems to work best
	- You may need to log in and out of Astro CLI for it to work the first time
---
12. Commands
	- `astro dev start`
	- `astro dev start -no-browser`
	- `astro dev stop`
	- `astro dev pytest
	- `astro help`
	- `astro dev ps`
	- `astro dev logs`
	- `astro wo create --name "AstronomerGirls"`
	- `astro deployment create -n "dev" -d "dev environment"`
	- `astro deployment list
	- `astro deployment delete`
	- `astro deploy`
	- `docker container prune`
	- `docker ps`
	- `docker images`
	- `airflow scheudler`
---
13. How to deploy Astro (with deployment API key)
	- Deployment > Add API key > New API key > name `cicd` > create 2 environment variables (context of Astro CLI: operating system level), (context of CI/CD pipeline: in CI/CD pipeline) > copy Key ID > go to code editor terminal 
	- > `export ASTRONOMER_KEY_ID={paste key ID}`
	- > `export ASTRONOMER_KEY_SECRET={paste secret ID}`
	- See your astronomer environment variables: `env | grep ASTRON`
	- `astro deploy {ID} --pytest`
---
14. See your deployment in browser
	- Deployments > Mouse hover over deployment > Click `Open Airflow`