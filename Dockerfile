FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all code
COPY . .

# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Start both FastAPI and Streamlit using Honcho (Procfile runner)
RUN pip install honcho

CMD ["honcho", "start"]