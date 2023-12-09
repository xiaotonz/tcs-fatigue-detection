FROM --platform=linux/amd64 python:3.9-slim 


WORKDIR /app

COPY . /app

#tcsfatigueacr.azurecr.io/tcs_model_test

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgmp-dev \
        libmpfr-dev \
        gcc \
        python3-dev \
        libmpc-dev \
        libgl1-mesa-glx \
        libglib2.0-0  \
        && pip install --no-cache-dir -r requirements.txt

# Install gmpy2
RUN pip install gmpy2

# Clean up
RUN apt-get purge -y --auto-remove libgmp-dev libmpfr-dev gcc python3-dev libmpc-dev \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p videos/input_videos
RUN mkdir -p videos/output_videos
# Expose port 80
EXPOSE 8000
EXPOSE 8001


# Set an environment variable
ENV NAME Model
# ENV FLASK_APP=video_processing.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=80

# Run your Python script
# CMD ["flask", "run"]

# CMD ["python", "video_processing.py"]
CMD ["uvicorn", "video_processing:app", "--host", "0.0.0.0", "--port", "8000"]
