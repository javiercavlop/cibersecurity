bazel-bin/private_join_and_compute/generate_dummy_data \
--server_data_file=../data/dummy_server_data.csv \
--client_data_file=../data/dummy_client_data.csv --server_data_size=1000 \
--client_data_size=1000 --intersection_size=200 --max_associated_value=100


bazel-bin/private_join_and_compute/server --server_data_file=../data/dummy_server_data.csv

bazel-bin/private_join_and_compute/client --client_data_file=../data/dummy_client_data.csv


bazel-bin/private_join_and_compute/generate_dummy_data \
--server_data_file=../data/dummy_server_data.csv \
--client_data_file=../data/dummy_client_data.csv --server_data_size=81000 \
--client_data_size=1000 --intersection_size=1 --max_associated_value=100


bazel-bin/private_join_and_compute/server --server_data_file=../data/dummy_server_data.csv

bazel-bin/private_join_and_compute/client --client_data_file=../data/dummy_client_data.csv