FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . /src
WORKDIR /src
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
ENV PYTHONPATH=/src
CMD alembic upgrade head && uvicorn main:app --debug --reload --host 0.0.0.0 --port 8001
EXPOSE 8001
