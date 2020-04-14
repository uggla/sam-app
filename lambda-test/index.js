const AWS = require('aws-sdk');
const env = require(`./environments/environment.${process.env.ENVIRONMENT.toLowerCase()}`);

const s3 = new AWS.S3({
  apiVersion: '2006-03-01',
  endpoint: env.s3_endpoint,
  sslEnabled: env.s3_ssl_enabled,
  s3ForcePathStyle: env.s3ForcePathStyle
});

/**
 * Handle SQS event
 * Consomme le flux adresse pour mettre à jour les sites dans Tempo
 */
exports.handler = async sqsMessage => {
  console.log(`input : ${JSON.stringify(sqsMessage)}`);

  const sqsBody = JSON.parse(sqsMessage.Records[0].body);
  const bucketEvent = sqsBody.Records[0];

  const bucketParams = {
    Bucket: env.bucket,
    Key: "ressources/exemple_ressource_1_S3.json",
    ResponseContentType: 'application/json'
  };

  try {
    const bucketFile = await s3.getObject(bucketParams).promise();
    const fileContent = JSON.parse(bucketFile.Body.toString());
    console.debug('Contenu du Fichier Bucket : ' + JSON.stringify(fileContent));
  } catch (err) {
    console.log(err, err.stack);
  }
};
