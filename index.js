/* The MIT License

Copyright (c) 2021 Sanay Bordia

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE. */

const express = require('express')
const app = express()
const csv = require('node-csv').createParser()
const _ = require('underscore')

// This is the webserver port
const port = 3000

/////////////////////////////////////////////////////////////////////////////////////////////////////
// Data
/////////////////////////////////////////////////////////////////////////////////////////////////////

// Parse the majors file
var majors = null;
csv.parseFile('./data/majors.csv', function(err, data) {
    if (err) {
        console.log("Unable to get majors data");
    } else {
        majors = data;
        majors.shift(); // remove the header
    }
});

// Parse the all file
var all = null;
csv.parseFile('./data/all.csv', function(err, data) {
    if (err) {
        console.log("Unable to get specific data");
    } else {
        all = data;
        all.shift(); // remove the header
    }
});

/////////////////////////////////////////////////////////////////////////////////////////////////////
// API's
/////////////////////////////////////////////////////////////////////////////////////////////////////

// Get a list of all majors
app.get('/majors', (req, res) => {
    if (majors != null) {
        var listMajors = [];

        // Get the list of majors (which is the 2nd element in each sub-object)
         _.each(majors, function(value) {
            return listMajors.push(value[1]);
          });        

        res.status(200).json({Message: listMajors})
    }
    else
        res.status(404).json({Message: "List of majors is not available"})   
})

// Get economic data for each major
app.get('/major', (req, res) => {
    if (all != null) {
        if (req.query != null) {
            var major = Object.keys(req.query)[0];
            var data = {};
             _.each(all, function(value) {
                if (major.toUpperCase() == value[1].toUpperCase()) {
                    data = {"Median Income": value[8], "25th Percentile": value[9], "75th Percentile": value[10], "Top 5 Colleges": value[11]};
                    res.status(200).json({Message: data});
                }
              });        

            res.status(404).json({Message: "Data not found"})
        }
        else
            res.status(404).json({Message: "Incorrect query specified"})   
    }    
    else
        res.status(404).json({Message: "Majors data is not available"})   
})

/////////////////////////////////////////////////////////////////////////////////////////////////////
// Listener
/////////////////////////////////////////////////////////////////////////////////////////////////////

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

