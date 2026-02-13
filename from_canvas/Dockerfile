FROM python:3.12-slim

WORKDIR /app

COPY . /app

# RUN apt-get update && \
  #  apt-get install -y --no-install-recommends \
   #     build-essential \
    #    libssl-dev \
     #   libffi-dev \
      #  python3-dev \
       # curl \
  #  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["python", "retrieve.py"]

