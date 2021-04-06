FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
RUN mkdir -p ./templates
COPY ./map_opt.py ./invokes.py ./
CMD [ "python", "./map_opt.py" ]