#!/usr/bin/env python3

"""
NAME
    fastdetect - run a lightweight language detection server
    
SYNOPSIS
    fastdetect bind_addr port model_path [--workers] [--cors]
    
DESCRIPTION
    FastDetect is a lightweight language detection server that is capable of 
    recognizing 175 languages using a data model trained on source text from 
    Wikipedia, Tatoeba, and SETimes. It is powered by the Facebook developed 
    `fastText` library, a uses `Bottle` and `gunicorn` to provide a REST-style 
    interface in which to interact with the model.

    Please see https://fasttext.cc/ for more information.
    
OPTIONS
    bind_addr
        The IP address or hostname that this server process will bind to.
    port
        The port used by this server process to listen for incoming requests.
    model_path
        The path to the model file. This file can be found at 
        https://fasttext.cc/docs/en/language-identification.html
    --workers=COUNT
        The number of worker processes that will be used to serve responses. The
        default value if omitted is 1.
    --cors=DOMAIN
        If given, CORS requests will be accepted from the given domain. An 
        'Access-Control-Allow-Origin' header with the given domain will be 
        included in all responses, unconditionally. Supports the wildcard 
        character ('*'). Note that if this is omitted, CORS will not be
        supported, and all preflight requests will receive a 400 error.
        
ENDPOINTS
    XYZ /
        Unconditionally serves 200 with an empty response body. Used primarily 
        for performing health checks on the server. 'XYZ' may be any canonical 
        HTTP request method.
    OPTIONS /detectOne
        Preflighting for 'POST /detectOne' endpoint.
    POST /detectOne
        Detect the language of a single utterance. The request body should
        comport with the 'application/json' content-type, and should contain
        a JSON object with a MANDATORY top-level 'data' property containing the
        utterance to be detected. An optional 'predictions' property containing
        an integer value may be given to alter the number of predictions that
        are returned (the default value is 1).
    OPTIONS /detectMany
        Preflighting for 'POST /detectMany' endpoint.
    POST /detectMany
        Detect the language of an array of utterances. The request body should
        comport with the 'application/json' content-type, and should contain
        a JSON object with a MANDATORY top-level 'data' property containing the
        array of utterances to be detected. An optional 'predictions' property
        containing an integer value may be given to alter the number of
        predictions that are returned (the default value is 1).
        
OUTPUT
    200
        Successful responses are of the content-type 'application/json', and
        contain a JSON object containing a top-level property named 'data'. This
        property either contains an object with a string property
        'utterance' containing the original utterance and an object property
        containing the 'detectedLanguage' and 'confidence' for each prediction,
        or an array of said objects.
    400
        Malformed requests are given responses of the content-type 
        'application/json' which contain two properties: 'errorCode', which
        provides a code for the given error, and 'errorDescritpion', which is
        a detailed explaination of the error. Note that unsupported CORS
        requests fall under this category.
        
EXIT CODES
    0
        This exit code is used if no errors ocurred during execution.
    1
        This exit code is used if the given data model file cannot be found.
        Also raised if any unexpected runtime exceptions are raised.
    2
        This exit code is used if the given argument vector was malformed.
        
AUTHOR
    Written by Kristoffer A. Wright (kris.al.wright@gmail.com)
    
COPYRIGHT
    Copyright (C) 2022 Kristoffer A. Wright
    This software is protected under the MIT license.
    Please see the LICENSE file for more information.
"""

################################################################################
# Imports ######################################################################
################################################################################

# Standard library:
import argparse
import datetime
import os
import sys
from typing import List

# Third party:
import bottle
import fasttext
import gunicorn.app.base

################################################################################
# Globals ######################################################################
################################################################################

MODEL = None
CORS_DOMAIN = None

def initialize_model(model_path: str) -> None:
    """Initialize the global MODEL variable. This can only be done once."""
    
    global MODEL
    
    # Only initialize once!
    if MODEL is not None:
        return
    
    try:
        MODEL = fasttext.load_model(model_path)
    except Exception:
        print("Could not load model.", file=sys.stderr)
        sys.exit(1)

def initialize_cors_domain(domain: str) -> None:
    """
    Initialize the global CORS_DOMAIN variable. This can only be done once.
    """
    
    global CORS_DOMAIN
    
    # Only initialize once!
    if CORS_DOMAIN is not None:
        return
    
    CORS_DOMAIN = domain
    

################################################################################
# Argument parsing #############################################################
################################################################################

def parse_argv() -> argparse.Namespace:
    """
    Parse the argument vector and return the `argparse.Namespace` yielded from
    this operation.
    """
    
    # Create the parser and define the arguments to parse:
    parser = argparse.ArgumentParser()
    parser.add_argument("bind", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("model", type=str)
    parser.add_argument("--workers", type=int, required=False, default=1)
    parser.add_argument("--cors", type=str, required=False, default=None)
    namespace = parser.parse_args()
    return namespace

################################################################################
# Language detection ###########################################################
################################################################################

def detect(utterance: str, 
            predictions: int) -> List[dict]:
    """
    Detect the language of a given utterance and return the given number of
    top predictions.
    
    The return data consists of a list of predictions, sorted in descending
    order by confidence score, where each prediction is a dict containing
    the detected language code, and the confidence score.
    """
    prediction = MODEL.predict(utterance, k=predictions)
    ret = {
        "utterance": utterance,
        "results": []
    }
    log = "[{}] [{}] [DETECTION] {}".format(
        str(datetime.datetime.now()),
        os.getpid(),
        utterance)
    for i in range(len(prediction[0])):
        ret["results"].append(
            {
                "detectedLanguage": prediction[0][i][9:], 
                "confidence": prediction[1][i]
            }
        )
        log += " ({}/{})".format(prediction[0][i][9:], prediction[1][i])
    print(log)
    return ret

################################################################################
# WSGI application #############################################################
################################################################################

def health_check_route() -> dict:
    """
    Route callback for the `XYZ /` endpoint where `XYZ` is one of "GET", "POST",
    "OPTIONS", "HEAD", "PUT", "PATCH", "DELETE", "CONNECT", or "TRACE".
    Unconditionally serves 200, and is primarily used for health checks. Also
    serve
    """
    return

def detect_one_route() -> dict:
    """
    Route callback for the `POST /detectOne` endpoint. Detects the language of
    a single utterance.
    """
    
    # Validate input:
    try:
        utterance = str(bottle.request.json["data"]) \
            .replace("\n", "") \
            .replace("\t", "") \
            .replace("\r", "") 
        predictions = int(bottle.request.json["predictions"]) \
            if ("predictions" in bottle.request.json) else 1   
    except Exception:
        bottle.response.status = 400
        return {
            "errorCode": "MALFORMED_REQUEST",
            "errorDescription": "Could not parse the request body. Please try "
                + "again."
        }
        
    if CORS_DOMAIN is not None:
        bottle.response.add_header("Access-Control-Allow-Origin", CORS_DOMAIN)
        
    return {"data": detect(utterance, predictions)}

def detect_many_route() -> dict:
    """
    Route callback for the `POST /detectMany` endpoint. Detects the language of
    an array of utterances.
    """
    
    # Validate input:
    try:
        utterances = bottle.request.json["data"]
        if not isinstance(utterances, list):
            raise Exception
        predictions = int(bottle.request.json["predictions"]) \
            if ("predictions" in bottle.request.json) else 1
    except Exception:
        bottle.response.status = 400
        return {
            "errorCode": "MALFORMED_REQUEST",
            "errorDescription": "Could not parse the request body. Please try "
                + "again."
        }
        
    ret = []
    for utterance in utterances:
        clean_utterance = utterance \
            .replace("\n", "") \
            .replace("\t", "") \
            .replace("\r", "") 
        ret.append(detect(clean_utterance, predictions))
        
    if CORS_DOMAIN is not None:
        bottle.response.add_header("Access-Control-Allow-Origin", CORS_DOMAIN)
        
    return {"data": ret}

def preflight_route() -> dict:
    
    # If CORS is not enabled, serve a 400 error:
    if CORS_DOMAIN is None:
        bottle.response.status = 400
        return {
            "errorCode": "CORS_REQUEST_REJECTED",
            "errorDescription": "CORS requests are not supported by this server"
        }
    
    # Get request headers
    origin_request_header = bottle.request.get_header("Origin", None)
    access_control_method_request_header = \
        bottle.request.get_header("Access-Control-Request-Method", None)
        
    if origin_request_header is None:
        bottle.response.status = 400
        return {
            "errorCode": "CORS_REQUEST_REJECTED",
            "errorDescription": "Missing required header 'Origin'"
        }
    if access_control_method_request_header is None:
        bottle.response.status = 400
        return {
            "errorCode": "CORS_REQUEST_REJECTED",
            "errorDescription": "Missing required header 'Access-Control-"
                + "Request-Method'"
        }
        
    # Ensure the given headers match:
    if (CORS_DOMAIN != "*") and (origin_request_header != CORS_DOMAIN):
        bottle.response.status = 400
        return {
            "errorCode": "CORS_REQUEST_REJECTED",
            "errorDescription": "CORS requests not accepted from this domain"
        }
    if access_control_method_request_header.lower() != "post":
        bottle.response.status = 400
        return  {
            "errorCode": "CORS_REQUEST_REJECTED",
            "errorDescription": "Unsupported request method preflighted"
        }
        
    # Add response headers:
    bottle.response.add_header("Access-Control-Allow-Origin", CORS_DOMAIN)
    bottle.response.add_header("Access-Control-Allow-Methods", "POST")
    
    return

def get_wsgi_app() -> bottle.Bottle:
    """
    Return the root WSGI application to be served by the `gunicorn` server.
    """
    application = bottle.Bottle()
    
    # Configure routes:
    application.route("/", "GET", health_check_route)
    application.route("/", "POST", health_check_route)
    application.route("/", "PUT", health_check_route)
    application.route("/", "PATCH", health_check_route)
    application.route("/", "DELETE", health_check_route)
    application.route("/", "TRACE", health_check_route)
    application.route("/", "OPTIONS", health_check_route)
    application.route("/", "HEAD", health_check_route)
    application.route("/detectOne", "OPTIONS", preflight_route)
    application.route("/detectOne", "POST", detect_one_route)
    application.route("/detectMany", "OPTIONS", preflight_route)
    application.route("/detectMany", "POST", detect_many_route)
    
    return application

################################################################################
# WSGI server ##################################################################
################################################################################

class FastDetectServer(gunicorn.app.base.BaseApplication):
    
    def __init__(self,
            app: bottle.Bottle,
            options: dict = {}) -> None:
        """Create a new instance of this class."""
        
        self.options = options
        self.application = app
        super().__init__()
        
    # OVERRIDE:
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    # OVERRIDE:
    def load(self):
        return self.application

################################################################################
# Main function ################################################################
################################################################################

def main() -> int:
    """The entry point for this application."""
    
    # Parse the argument vector:
    argv_arguments = parse_argv()
    bind_address = argv_arguments.bind
    listening_port = argv_arguments.port
    model_path = argv_arguments.model
    worker_count = argv_arguments.workers
    cors_domain = argv_arguments.cors
    
    # Initialize globals:
    initialize_model(model_path)
    initialize_cors_domain(cors_domain)
    
    # Initialize the server:
    server_options = {
        "bind": "{}:{}".format(bind_address, listening_port),
        "workers": worker_count,
        "accesslog": "-"
    }
    FastDetectServer(get_wsgi_app(), server_options).run()
    
    return 0

################################################################################
# Driver code ##################################################################
################################################################################

if __name__ == "__main__":
    sys.exit(main())