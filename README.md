# Unserve
Run python serverless locally


Instructions

    pip install git+https://github.com/kryptn/unserve.git 
    npm install -g serverless
    
    sls create --template aws-python --path service
    touch service/__init__.py
    python -m unserve service


