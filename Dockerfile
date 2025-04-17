FROM node:slim

WORKDIR /usr/app/babysleepcoach
EXPOSE 80

#Copy the pip build files in first
COPY ./requirements.txt .

ENV DEBIAN_FRONTEND=noninteractive
# Install required packages
ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN apt-get update && apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y python3-pip libgl1 libglib2.0-0



RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy in the rest of the files
COPY . .

RUN cd webapp && yarn install && cd ..

WORKDIR /usr/app/babysleepcoach

ENTRYPOINT ["bash", "start_docker.sh"]
