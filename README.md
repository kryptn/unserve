# Unserve [![Build Status](https://travis-ci.org/kryptn/unserve.svg?branch=master)](https://travis-ci.org/kryptn/unserve) [![Coverage Status](https://coveralls.io/repos/github/kryptn/unserve/badge.svg?branch=master)](https://coveralls.io/github/kryptn/unserve?branch=master)
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


