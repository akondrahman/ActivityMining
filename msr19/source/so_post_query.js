const BigQuery = require('@google-cloud/bigquery');
var fs = require('fs');

const projectId = "githubsolidityquery";
const sqlQuery = 'SELECT * FROM `LOL.SO_GH_PYTHON_POST_ID_TITLE_BODY`' ; 

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
var out_fil  = 'OUT_ SO_GH_PYTHON_POST_ID_TITLE_BODY_DAT.txt'

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
      postID      = row_as_json['Id'];
      postTitle   = row_as_json['Title'];
      postBody    = row_as_json['Body'];

      postTitle   = postTitle.replace(/;/g, ' ') 
      postTitle   = postTitle.replace(/,/g, ' ') 

      postBody    = postBody.replace(/,/g, ' ')
      postBody    = postBody.replace(/#/g, ' ')      
      postBody    = postBody.replace(/&/g, ' ')      
      postBody    = postBody.replace(/\t/g, ' ')      
      postBody    = postBody.replace(/\n/g, ' ')            
      postBody    = postBody.replace(/=/g, ' ')      
      
      data   = postID.toString() + ',' + postTitle + ',' + postBody +  '\n' ;
      fullData = fullData + data ; 
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