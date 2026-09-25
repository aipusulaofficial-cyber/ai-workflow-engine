FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from workflow_engine import Workflow; print('workflow engine ready')"]
