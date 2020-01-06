FROM python:3
COPY . graphqlGenerator
WORKDIR graphqlGenerator
RUN pip install -r requirements.txt
RUN python setup.py install
CMD ["python","connections/app.py"]