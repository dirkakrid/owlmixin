FROM python:3-onbuild

RUN pip install -U setuptools pip
RUN pip install wheel twine

CMD [ "./release.sh", ${VERSION}, ${PASSWORD} ]
