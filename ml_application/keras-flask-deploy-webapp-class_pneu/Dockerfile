FROM tensorflow/tensorflow:2.11.0

COPY ./req_info.txt /
RUN python3 -m pip install -r req_info.txt

COPY . /app
WORKDIR /app

EXPOSE 5000
CMD [ "python" , "app_pneu.py"]
