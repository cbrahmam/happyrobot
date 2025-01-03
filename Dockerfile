FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo '#!/bin/bash\n\
echo "Starting uvicorn..."\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 80' > /startup.sh

RUN chmod +x /startup.sh
CMD ["/startup.sh"]