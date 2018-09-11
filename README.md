# HtmlToPdfPythonLambda
Inspired from https://github.com/21Buttons/pychromeless

## How to 
### On Dev
#### Installation
You must have docker and Docker compose installed. 
Virtualenv your project if you want to (`virtualenv . -p /usr/local/bin/python3`, `source bin/activate`)
run `make fetch-dependencies`.

#### Run 
`make fetch-dependencies`
`make docker-run`

### On Production
#### Creating the zip deployment package
run `make build-lambda-package`     

#### Creating a AWS lambda instance
Following those steps:
- go to the create function insterface, and select the author form scratch option.
- set a name and the runtime to Python 3
- create a new role with admin access, and just select the default options that are proposed to you
- You are then re-directed to editor interface of your function
    - in the function code part:
        - under the "Code entry type"
        - select "Upload .zip file"
        - upload the zip that you've created with the makefile function. (if it's too big, upload it to s3)
        - in the handler set the path to your function like: module.file_name.method_name
    - in the environnement variable
        - `PYTHONPATH=/var/task/src:/var/task/lib`
        - `PATH=/var/task/bin`
    - in the basic setting section
        - Timeout: +10 seconds
        - Memory: + 250MB
    - in the editor part
        - Add a API Gateaway. In the configure triggers section that just appears:
            - select the "create new API" option
            - select whatever security option you want
    - click save and wait for the Lambda and API Gateaway to be created.
        - (Optional) Go to the API Gateaway editor and you can there create a new method endpoint
            - select the GET type
            - select the "Lambda Function" integration type
            - Tick the "Use Lambda Proxy integration" checkbox
            - select your lambda function that you've just created
            
#### Use
Now that you have an open API gateaway, you just have to use it's url and do a GET method on it with a GET param named `url`.

## Explanation
### Running a python lambda function on AWS Lambda
> To create a Lambda function, you first package your code and dependencies in a deployment package. Then, you upload the deployment package to AWS Lambda to create your Lambda function.
> https://docs.aws.amazon.com/lambda/latest/dg/lambda-app.html

So basically, AWS can run any python code with any dependancies if you install them in a directory and zip it. For automation, this step is done in a Makefile, the `build-lambda-package`.

### Generation of PDF
It's base on the [pdfkit](https://github.com/JazzCore/python-pdfkit) package, which rely on [wkhtmltopdf](https://wkhtmltopdf.org/).

## TODO
- make it work with pdfkit
- reduce package size
- make docker test works with the event part

## Testing with docker-lambda
https://github.com/lambci/docker-lambda

Just run `make docker-run`
