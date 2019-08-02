#!/bin/bash
pip install -r /component_repository/sh/pre_config/requirements.txt
python /component_repository/sh/pre_config/main.py --site_config /component_repository/augmented_site_level_config_file.yaml --execution_id $EXECUTION_ID --output_dir /component_repository/sh/config
