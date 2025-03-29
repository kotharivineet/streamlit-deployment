FROM python:3.9-slim

# Set working directory
WORKDIR /streamlit-deployment

# Copy app files to the container
COPY . /streamlit-deployment/

# Install dependencies
RUN pip install streamlit

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
