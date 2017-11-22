var https = require('https');
var querystring = require('querystring');


var options = {
  host: 'api.github.com',
  //host: 'www.google.com',
  method: 'GET',
  headers: {
    'User-Agent': 'jongodshall'
  }
}

var request = https.request(options, (response) => {
  console.log('Status: ' + response.StatusCode);
  console.log('Headers: ' + JSON.stringify(response.headers));
  response.setEncoding('utf8');
  response.on('data', (body) => {
    console.log('Body: ' + body);
  });
  response.on('end', () => {
    console.log('End of response.');
  })
});

request.on('error', (e) => {
  console.error('Something went wrong: ${e.message}');
})

request.end();
