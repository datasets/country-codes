const fs = require('fs')
const request = require('request')
const Papa = require('papaparse')


const urlToCsv = 'https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv'

let data = ''

request
  .get(urlToCsv)
  .on('response', (response) => {
    console.log(response.statusCode)
  })
  .on('data', (chunk) => {
    if (chunk) {
      data += chunk.toString('utf8')
    }
  })
  .on('end', () => {
    const parsed = Papa.parse(data, {
      header: true,
      skipEmptyLines: true
    })
    const myJson = JSON.stringify(parsed.data, null, 2)
    fs.writeFileSync('data.json', myJson)
  })
