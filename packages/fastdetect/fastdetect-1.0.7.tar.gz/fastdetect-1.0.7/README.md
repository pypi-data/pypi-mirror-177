# `fastdetect` Manual Page

## NAME
fastdetect - run a lightweight language detection server
    
## SYNOPSIS
fastdetect bind_addr port model_path [--workers] [--cors]
    
## DESCRIPTION
FastDetect is a lightweight language detection server that is capable of recognizing 175 languages using a data model trained on source text from Wikipedia, Tatoeba, and SETimes. It is powered by the Facebook developed `fastText` library, and uses `Bottle` with `gunicorn` to provide a REST-style interface in which to interact with the model.

Please see https://fasttext.cc/ for more information.

## OPTIONS

### `bind_addr`
The IP address or hostname that this server process will bind to.

### `port`
The port used by this server process to listen for incoming requests.

### `model_path`
The path to the model file. This file can be found at https://fasttext.cc/docs/en/language-identification.html

### `--workers=COUNT`
The number of worker processes that will be used to serve responses. The
default value if omitted is 1.


### `--cors=DOMAIN`
If given, CORS requests will be accepted from the given domain. An 
`Access-Control-Allow-Origin` header with the given domain will be 
included in all responses, unconditionally. Supports the wildcard 
character ('*'). Note that if this is omitted, CORS will not be
supported, and all preflight requests will receive a 400 error.
        
## ENDPOINTS

### `XYZ /`
Unconditionally serves 200 with an empty response body. Used primarily for
performing health checks on the server. `XYZ` may be any canonical HTTP request
method.

### `OPTIONS /detectOne`
Preflighting for `POST /detectOne` endpoint.

### `POST /detectOne`
Detect the language of a single utterance. The request body should
comport with the `application/json` content-type, and should contain
a JSON object with a MANDATORY top-level `data` property containing the
utterance to be detected. An optional `predictions` property containing
an integer value may be given to alter the number of predictions that
are returned (the default value is 1).

### `OPTIONS /detectMany`
Preflighting for 'POST /detectMany' endpoint.

### `POST /detectMany`
Detect the language of an array of utterances. The request body should
comport with the `application/json` content-type, and should contain
a JSON object with a MANDATORY top-level `data` property containing the
array of utterances to be detected. An optional `predictions` property
containing an integer value may be given to alter the number of
predictions that are returned (the default value is 1).
        
## OUTPUT

### `200`
Successful responses are of the content-type `application/json`, and
contain a JSON object containing a top-level property named `data`. This
property either contains an object with a string property
`utterance` containing the original utterance and an object property
containing the `detectedLanguage` and `confidence` for each prediction,
or an array of said objects.

### `400`
Malformed requests are given responses of the content-type 
`application/json` which contain two properties: `errorCode`, which
provides a code for the given error, and `errorDescritpion`, which is
a detailed explaination of the error. Note that unsupported CORS
requests fall under this category.
        
## EXIT CODES

### `0`
This exit code is used if no errors ocurred during execution.

### `1`
This exit code is used if the given data model file cannot be found.
Also raised if any unexpected runtime exceptions are raised.

### `2`
This exit code is used if the given argument vector was malformed.
        
## AUTHOR
Written by Kristoffer A. Wright (kris.al.wright@gmail.com)
    
## COPYRIGHT
Copyright (C) 2022 Kristoffer A. Wright
    
This software is protected under the MIT license.
Please see the LICENSE file for more information.

---

# Sample JSON Requests and Responses

## Sample `POST /detectOne` Request Body

```json
{
    "data": "The man in black fled across the desert, and the gunslinger followed."
}
```

## Sample `POST /detectOne` Response Body

```json
{
    "data": {
        "utterance": "The man in black fled across the desert, and the gunslinger followed.",
        "results": [
            {
                "detectedLanguage": "en",
                "confidence": 0.9147520065307617
            },
            {
                "detectedLanguage": "it",
                "confidence": 0.01209554634988308
            },
            {
                "detectedLanguage": "pt",
                "confidence": 0.009296770207583904
            }
        ]
    }
}
```

## Sample `POST /detectMany` Request Body

```json
{
    "data": [
        "The man in black fled across the desert, and the gunslinger followed.",
        "Hola. Como estas?",
        "Muž v černém uprchl přes poušť a pistolník ho následoval.",
        "검은 옷을 입은 남자는 사막을 가로질러 도망쳤고 총잡이는 그 뒤를 따랐다."
    ]
}
```

## Sample `POST /detectMany` Response Body

```json
{
    "data": [
        {
            "utterance": "The man in black fled across the desert, and the gunslinger followed.",
            "results": [
                {
                    "detectedLanguage": "en",
                    "confidence": 0.9147520065307617
                },
                {
                    "detectedLanguage": "it",
                    "confidence": 0.01209554634988308
                },
                {
                    "detectedLanguage": "pt",
                    "confidence": 0.009296770207583904
                }
            ]
        },
        {
            "utterance": "Hola. Como estas?",
            "results": [
                {
                    "detectedLanguage": "es",
                    "confidence": 0.7752323746681213
                },
                {
                    "detectedLanguage": "pt",
                    "confidence": 0.20101742446422577
                },
                {
                    "detectedLanguage": "gl",
                    "confidence": 0.015422248281538486
                }
            ]
        },
        {
            "utterance": "Muž v černém uprchl přes poušť a pistolník ho následoval.",
            "results": [
                {
                    "detectedLanguage": "cs",
                    "confidence": 0.9968787431716919
                },
                {
                    "detectedLanguage": "en",
                    "confidence": 0.0011031883768737316
                },
                {
                    "detectedLanguage": "ro",
                    "confidence": 0.0007685713935643435
                }
            ]
        },
        {
            "utterance": "검은 옷을 입은 남자는 사막을 가로질러 도망쳤고 총잡이는 그 뒤를 따랐다.",
            "results": [
                {
                    "detectedLanguage": "ko",
                    "confidence": 1.0000699758529663
                },
                {
                    "detectedLanguage": "tr",
                    "confidence": 1.0000403563026339e-05
                },
                {
                    "detectedLanguage": "en",
                    "confidence": 1.0000098882301245e-05
                }
            ]
        }
    ]
}

```

