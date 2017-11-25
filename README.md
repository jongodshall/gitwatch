# gitwatch v1.0

## Use

Expects a single command line parameter to specify the organization name:

`python gitwatch.py <orgname>`

Currently, the program will find all public repos for the organization, gather all pull requests for each repo, print the count of pull requests to the console, and finally print the high level details of individual pulls to a file in the tmp directory.  Each repo gets its own file.


## Authenitcation

To use the api, a User-Agent header is required.  It is recommend to also generate an [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/), as unauthenticated requests are limited to 60/hour.

For security, we keep the header info in a file called token.txt.  Create this file in the main directory, with a single line formatted as:
`{"User-Agent": "<username>", "Authorization": "token <token>"}`
