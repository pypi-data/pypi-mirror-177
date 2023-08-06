# `aws_feature_store`

The `aws_feature_store` is a simplified approach from SageMaker Feature Store.

# Initialize feature group

bucket_name = '{bucket_for_feature_store}'
s3_folder = '{folder_for_feature_store}'
featuregroup_name = '{my_repo}_{commit_id}'

feature_group = FeatureGroup(
    name=featuregroup_name,
    boto3_session = boto3.Session(**credentials),
    s3_uri=f"s3://{bucket_name}/{s3_folder}"
    )

# Create feature group

description="What is my feature group about"
feature_script_repo="{repo_link_to_script}"
data_source="{what data are used}"

record_identifier_feature_name = "column name to store id" 
event_time_feature_name = "{column name to store timestamp}"

feature_definitions=[
        FeatureDefinition(feature_name="column_name1", feature_type=FeatureTypeEnum.INTEGRAL),
        FeatureDefinition(feature_name="column_name2", feature_type=FeatureTypeEnum.STRING),
        ]


feature_group.create(
    record_identifier_name=record_identifier_feature_name,
    event_time_feature_name=event_time_feature_name,
    feature_script_repo=feature_script_repo,
    data_source=data_source,
    description=description,
    feature_definitions=feature_definitions
)

# Ingest data
import pandas as pd
data = pd.read_json('data.json')
feature_group.ingest(data,'{batch_id_or_filename}')
