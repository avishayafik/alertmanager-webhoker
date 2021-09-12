FROM python:3.7-slim
WORKDIR /opt/
ADD requirements.txt $WORKDIR
RUN pip install -r requirements.txt
COPY ./ /opt/
#COPY templates/ /opt
### sanity test
#RUN export awx_username=test && export awx_password=test &&  python3 web-hooker.py &
ENTRYPOINT ["python","web-hooker.py"] 


