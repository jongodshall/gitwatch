# gitwatch v1.0

## Use

Expects a single command line parameter to specify the organization name:

`python gitwatch.py <orgname>`

Currently, the program will find all public repos for the organization, gather all pull requests for each repo, print the count of pull requests to the console, and finally print the high level details of individual pulls to a file in the tmp directory.  Each repo gets its own file.

The files are mostly a more convenient way to verify that the lists of pull requests are correct during development; the real value is the objects themselves.


## Authenitcation

To use the api, a User-Agent header is required.  It is recommend to also generate an [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/), as unauthenticated requests are limited to 60/hour.

For security, we keep the header info in a file called token.txt.  Create this file in the main directory, with a single line formatted as:
`{"User-Agent": "<username>", "Authorization": "token <token>"}`

## Improvements

The api is rate limited.  So long as the requests are authenticated per the previous section, we can make 5000 calls in an hour.  This is enough for normal use, but for a large repo where we require information only available on the details endpoint of an individual pull request, we can hit it fairly quickly.  Should we begin looking at details a caching mechanism will become necessary.

I believe I've handled the pagination as efficiently as possible.  It's not ideal to have to have web service calls inside a loop but I don't think it's avoidable at this time.
