FROM python:3.5

# Copy the application folder inside the container
ADD . /my_application

# Install required python packages
RUN pip install -r /my_application/requirements.txt

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /my_application

# Set the default command to execute
# when creating a new container
CMD python run.py host=0.0.0.0
