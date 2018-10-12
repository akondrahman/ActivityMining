const BigQuery = require('@google-cloud/bigquery');


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
    console.log('Rows:');
    rows.forEach(row => console.log(row['Path']));
  })
  .catch(err => {
    console.error('ERROR:', err);
  });