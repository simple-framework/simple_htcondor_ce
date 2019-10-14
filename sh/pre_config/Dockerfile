FROM python:3.5
RUN mkdir /component_repository
VOLUME /component_repository
ENV PYTHONPATH=$PYTHONPATH:/component_repository/sh/pre_config:/component_repository/sh/pre_config/files:/component_repository/sh/pre_config/helpers:/component_repository/sh/pre_config/models
ENTRYPOINT /component_repository/sh/pre_config/init.sh