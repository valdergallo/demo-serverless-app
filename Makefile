build:
	sam build --use-container

docker_setup_network:
	docker network create lambda-local

run_database:
	docker run -p 8000:8000 -d --rm --network lambda-local --name dynamodb -v $(CURDIR)/local/dynamodb:/data/ amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb -dbPath /data

stop_database:
	docker stop dynamodb

server:
	sam local start-api --debug --docker-network lambda-local --parameter-overrides Table=Activities Region=us-east-1 AWSEnv=AWS_SAM_LOCAL

load_data:
	aws dynamodb put-item --table-name Activities --item file://$(CURDIR)/data_model/DataModel.json --endpoint-url http://localhost:8000 --return-consumed-capacity TOTAL

save_schema:
	aws dynamodb describe-table --endpoint-url http://localhost:8000 --table-name Activities > data_model/Activities.json

list_table:
	aws dynamodb list-tables --endpoint-url http://localhost:8000

setup_dynamo_admin:
	npm install -G dynamodb-admin

run_dynamo_admin:
	DYNAMO_ENDPOINT=http://localhost:8000 dynamodb-admin --host localhost --port 8080
