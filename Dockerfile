# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:2.7

# Copy local code to the container image.
# ENV APP_HOME /techtrends/app
# WORKDIR $APP_HOME
COPY . /
WORKDIR /techtrends/app



# Install production dependencies.
# RUN apt-get update && \
#     pip install --upgrade pip && \
RUN pip install -r /techtrends/requirements.txt

# EXPOSE 3111
CMD sh /techtrends/startup.sh