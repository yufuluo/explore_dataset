## Programming Exercise
The application in this repository allows users to interactively explore a [dataset](../db/data.csv).\
Please follow this [instruction](../README.md) to run the app locally.\

It supports users to:
- group data by genre or network
- filter the data by a set of cities
- get the sum or average viewers of the dataset\

Some design considerations:
- As actual dataset being explored is larger than can fit in memory, the result return from the database is divided into multiple chunks, each with a reasonable size.
- The API is designed to be generic for supporting different filters and groups.
Please check the [API doc](api.md) for more details.
- If the underlying data model changed, I'll update the functions in the [util library](../lib/util.py) for supporting more complex db queries, for example JOIN among multiple tables.
- If other teams would like to integrate the same analytics your application produces into their own applications, they can use our [REST APIs](api.md).


## Perform a Code Review
The review can be found in a [PR of the tic-tac-toe repo](https://github.com/yufuluo/tic-tac-toe/pull/1).

## Recommend a Technology
If we need to support a fair amount of user load, we can:
- Pack the app server into a container and deploy to Kubernetes.\
Kubernetes can automatically scale the number of pods up and down based on the server load. Pods run by Kubernetes are stateless by default, if any of the server pods is down, the end user won’t notice it on their side as their request will be immediately processed by another pod.
- Use relational database (e.g. PostgreSQL or MySQL) as centralized database for supporting complex query for analysis.\
Create replicas for the main db instance, so that the load can be route to replicas if the main db instance is down.
- Cache recent or popular analytical results to distributed NoSQL database (e.g. Memcached or Redis).\
Not every user request queries unique data, lots of the data that users search may be similar. Therefore, we can store the most recent or known popular analytical results to a distributed NoSQL database cluster. When user submit a request, server first connect to the NoSQL database. If it cannot find the result there, then server query the centralized relational database, process the data, return result to user, and also write the new result to cache.\
NoSQL databases can usually handle way more query per second (QPS) then relational databases, so reading form it will be a lot faster. And it's also easier to scale the NoSQL database up or down according to the user load.
- Control user request frequency.\
To prevent the server from being overwhelmed, we should avoid user from sending multiple requests at a time. We can enforce a limit on the number of requests for the API calls. On the web UI, we can also add CAPTCHA, or make the submit button not clickable in a few seconds after the previous submit.\
Other improvements:
- Add monitoring and alerting for the server and databases. Prometheus + Grafana + Alertmanager.
- Build a pipeline for CI/CD using Jenkins or GitlabCI. For example trigger testing on PR, trigger build and deploy automatically when changes merged to the main branch.

## Recommend a Process
Stories for a sprint are usually planned base on the roadmap of a quarter. If a team cannot finish the stories within the planned sprint and have to roll over to next one too often, it will affect other projects on the plate, and can cause a delay of product delivery.\
If this happens, we need to look into the cases to figure out the cause, and then make relative changes. For example:
- If the stories are incomplete due to some external dependancies (for example, waiting for the security team to approve an exception, or waiting for the ops team to build some infrastructure), we need to figure out all the dependencies when kicking off a project, and plan ahead to avoid this in the future.
- If the stories are incomplete because its complexity is underestimated, or it's too big, we need to split the story, break it down into smaller pieces that can be finished in a sprint.
