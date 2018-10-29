const BigQuery = require('@google-cloud/bigquery');
var fs = require('fs');

const projectId = "githubsolidityquery";
// const sqlQuery = 'SELECT * FROM `LOL.SO_PYTHON_CODE_HISTORY`' ; 
const sqlQuery = 'SELECT * FROM `LOL.SO_PY_ANS_HISTORY`' ; 


// var out_fil = 'SO_PYTHON_CODE_HISTORY.csv'
var out_fil = 'SO_PY_ANS_HISTORY.csv'

const bigquery = new BigQuery({
  projectId: projectId,
  keyFilename: '', 
  location: 'US'
});

const options = {
  query: sqlQuery,
  useLegacySql: false, 
};

let job;
var fullData = '' ;


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
      //ID      = row_as_json['Id'];
      postID  = row_as_json['PostId'];
      //postHistoryID = row_as_json['PostHistoryId'];
      //postBody      = row_as_json['Content'];
      //postBody     = row_as_json['Comment'];
      //createDate  = row_as_json['CreationDate'];
      postBody  = row_as_json['Content'] 
      lineCount = row_as_json['LineCount'] 

      postBody    = postBody.replace(/,/g, ' ')
      postBody    = postBody.replace(/#/g, ' ')      
      postBody    = postBody.replace(/&/g, ' ')      
      postBody    = postBody.replace(/\t/g, ' ')      
      postBody    = postBody.replace(/\n/g, ' ')            
      postBody    = postBody.replace(/=/g, ' ')      

      

      //data   = ID.toString() + ',' + postID.toString() + ',' + postHistoryID.toString()+ ',' + postBody  + '\n' ;
      // data     = ID.toString() + ',' + postID.toString() + ',' + createDate + ',' + postBody  + '\n' ;
      data     =  postID.toString() + ',' + lineCount.toString() + ',' + postBody  + '\n' ;
      fullData = fullData + data ; 
    });
    
    fs.writeFile(out_fil, fullData, function(err) {
    if(err) {
        return console.log(err);
    }
        console.log("SO+CodeVersion data dumped succesfully ... ");
    }); 

  })
  .catch(err => {
    console.error('ERROR:', err);
  });