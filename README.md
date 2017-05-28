# Unserve
Run python serverless locally


Instructions

    virtualenv venv
    source venv/bin/activate

    pip install git+https://github.com/kryptn/unserve.git 
    npm install -g serverless
    
    sls create --template aws-python --path service
    touch service/__init__.py
    unserve service

    curl http://localhost:5000/


