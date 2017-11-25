# gitwatch v0.9

## Authenitcation

To use the api, a User-Agent header is required.  It is recommend to also generate an [personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/), as unauthenticated requests are limited to 60/hour.

For security, we keep the header info in a file called token.txt.  Create this file in the main directory, with a single line formatted as:
`{"User-Agent": "<username>", "Authorization": "token <token>"}`
