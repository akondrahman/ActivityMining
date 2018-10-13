// To download all post to GH mappings for all languages 

const BigQuery = require('@google-cloud/bigquery');
var fs = require('fs');

const projectId = "githubsolidityquery";
const sqlQuery = 'SELECT * FROM `LOL.SO_GH_DATA_FILTERED`' ; 

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
var out_fil  = 'OUT_SO_GH_DATA_FILTERED.csv'

bigquery
  .createQueryJob(options)
  .then(results => {
    job = results[0];
    console.log(`Job ${job.id} started.`);
    return job.promise();
  })
  .then(() => {
    return job.getMetadata();
  })
  .then(metadata => {
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
    rows.forEach(function(row_as_json){
      //console.log(row_as_json);
      postID      = row_as_json['PostId'];
      repoName    = row_as_json['RepoName'];


      
      data   = postID.toString() + ',' + repoName  +  '\n' ;
      fullData = fullData + data ; 
    });

    fs.writeFile(out_fil, fullData, function(err) {
    if(err) {
        return console.log(err);
    }
        console.log("SO+GH data dumped succesfully ... ");
    }); 

  })
  .catch(err => {
    console.error('ERROR:', err);
  });