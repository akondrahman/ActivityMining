const BigQuery = require('@google-cloud/bigquery');
var fs = require('fs');

const projectId = "githubsolidityquery";
const sqlQuery = 'SELECT * FROM `LOL.SO_GH_IDS`' ; 

const bigquery = new BigQuery({
  projectId: projectId,
  keyFilename: '', 
  location: 'US'

});

// Query options list: https://cloud.google.com/bigquery/docs/reference/v2/jobs/query
const options = {
  query: sqlQuery,
  useLegacySql: false, 
};

let job;
var fullData = '' ;
var out_fil  = 'OUT_FIL_GH_DAT.csv'

bigquery
  .createQueryJob(options)
  .then(results => {
    job = results[0];
    console.log(`Job ${job.id} started.`);
    return job.promise();
  })
  .then(() => {
    // Get the job's status
    return job.getMetadata();
  })
  .then(metadata => {
    // Check the job's status for errors
    const errors = metadata[0].status.errors;
    if (errors && errors.length > 0) {
      throw errors;
    }
  })
  .then(() => {
    console.log(`Job ${job.id} completed.`);
    return job.getQueryResults();
  })
  .then(results => {
    const rows = results[0];
    index = 0 ; 
    rows.forEach(function(row_as_json){
      //console.log(row_as_json);
      fileID = row_as_json['FileId'];
      repo   = row_as_json['RepoName'];
      branch = row_as_json['Branch'];
      postID = row_as_json['PostId'] ; 
      ghURL  = row_as_json['GHUrl'] ;
      
      data   = index.toString() + ',' + repo + ',' + branch + ',' + postID.toString() + ',' + ghURL + '\n' ;
      fullData = fullData + data ; 
      //console.log(fullData) ;
      index  += 1 ;
    });

    fs.writeFile(out_fil, fullData, function(err) {
    if(err) {
        return console.log(err);
    }
        console.log("File dumped succesfully ... ");
    }); 

  })
  .catch(err => {
    console.error('ERROR:', err);
  });