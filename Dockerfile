FROM python:3.9.2-buster
WORKDIR /rolelive
ADD requirements.txt .
RUN python -m pip install -r requirements.txt
ADD src .
CMD ["python", "main.py"]
