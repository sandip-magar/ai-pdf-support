#Start with a lightweight, official Python image
FROM python:3.11-slim

#Set the working directory inside the container to /app
WORKDIR /app

#Copy ONLY the requirements file first.
#(Docker caches this step! if requirements don't change, it skips reinstalling everything)
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy the rest of the application.
COPY . .

#Expose port -8000
EXPOSE 8000

#Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]