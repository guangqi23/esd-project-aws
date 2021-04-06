FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./optimisation.py ./invokes.py ./
CMD [ "python", "./optimisation.py" ]