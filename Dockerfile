FROM node:slim

WORKDIR /usr/app/babysleepcoach
EXPOSE 80

# Install required system packages
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y cron python3-pip libgl1 libglib2.0-0

# Python dependencies
COPY ./requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy all files into the image
COPY . .

# Cron configuration
RUN echo '0 0 * * * root /usr/bin/python3 /usr/app/babysleepcoach/analyze_sleep.py >> /sleep_analysis.log' > /etc/cron.d/sleep_analysis
RUN chmod 0644 /etc/cron.d/sleep_analysis && \
    touch /var/log/cron.log

# Cron configuration
RUN echo '0 0 * * * root /usr/bin/python3 /usr/app/babysleepcoach/sleep_heatmap.py >> /sleep_heatmap.log' > /etc/cron.d/sleep_heatmap
RUN chmod 0644 /etc/cron.d/sleep_heatmap && \
    touch /var/log/cron.log

# Install React app dependencies
RUN cd webapp && yarn install && cd ..

# Make entrypoint executable
RUN chmod +x start_docker.sh

ENTRYPOINT ["./start_docker.sh"]
