# unserve
Run python serverless locally



Untested instructions

    pip install -git+git://github.com/kryptn/unserve.git#egg=unserve 
    npm install -g serverless
    
    sls create --template aws-python --path service
    touch service/__init__.py
    python -m unserve service


