build:
	sam build --use-container

docker_setup_network:
	docker network create lambda-local

run_database:
	docker run -p 8000:8000 -d --rm --network lambda-local --name dynamodb -v $(CURDIR)/local/dynamodb:/data/ amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb -dbPath /data

stop_database:
	docker stop dynamodb

server:
	# sam local start-api --debug --docker-network lambda-local --parameter-overrides Table=Activities Region=us-east-1 AWSEnv=AWS_SAM_LOCAL
	sam local start-api --debug --docker-network lambda-local --parameter-overrides AWSEnv=AWS_SAM_LOCAL

load_data:
	aws dynamodb put-item --table-name Activities --item file://$(CURDIR)/data_model/DataModel.json --endpoint-url http://localhost:8000 --return-consumed-capacity TOTAL

list_table:
	aws dynamodb list-tables --endpoint-url http://localhost:8000

run_dynamo_admin:
	dynamodb-admin
