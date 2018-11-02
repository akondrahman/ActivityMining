const BigQuery = require('@google-cloud/bigquery');
var fs = require('fs');

const projectId = "githubsolidityquery";
const sqlQuery = 'SELECT * FROM `LOL.SO_SONAR_QUES_DETAILS`' ; 

var out_fil = 'SO_SONAR_QUES_DETAILS.txt'

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
      postID      = row_as_json['Id'];
      postTitle   = row_as_json['Title'];
      postBody    = row_as_json['Body'];
      postScore   = row_as_json['Score'];
      postViews   = row_as_json['ViewCount'];
      postAnswers = row_as_json['AnswerCount'];
      postComments= row_as_json['CommentCount'];
      postFavs    = row_as_json['FavoriteCount'];   
      postDate    = row_as_json['CreateDate'];
      postAccID   = row_as_json['AcceptedAnswerId'] ;
      
      if (postViews == null)
      {
        postViews = 0  // 0 means no favorites 
      }
      if (postAnswers == null)
      {
        postAnswers = 0 // 0 means no accepted answer ID 
      }      
      if (postFavs == null)
      {
        postFavs = 0  // 0 means no favorites 
      }
      if (postAccID == null)
      {
          postAccID = 0 // 0 means no accepted answer ID 
      }


      postTitle   = postTitle.replace(/;/g, ' ') 
      postTitle   = postTitle.replace(/,/g, ' ') 
      
      postBody    = postBody.replace(/,/g, ' ')
      postBody    = postBody.replace(/#/g, ' ')      
      postBody    = postBody.replace(/&/g, ' ')      
      postBody    = postBody.replace(/\t/g, ' ')      
      postBody    = postBody.replace(/\n/g, ' ')            
      postBody    = postBody.replace(/=/g, ' ')      
      
      data   = postID.toString() + ',' + postTitle + ',' + postDate + ',' + postBody  + ',' + postScore.toString() + ',' + postViews.toString() + ',' + postAnswers.toString() + ',' + postComments.toString() + ',' + postFavs.toString() + ',' + postAccID.toString() + '\n' ;
      fullData = fullData + data ; 
    });

    fs.writeFile(out_fil, fullData, function(err) {
    if(err) {
        return console.log(err);
    }
        console.log("SO+SONARQUBE+QUES data dumped succesfully ... ");
    }); 

  })
  .catch(err => {
    console.error('ERROR:', err);
  });