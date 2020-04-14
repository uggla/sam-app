module.exports = {
  region: process.env.REGION,
  s3_endpoint: `${process.env.S3_ENDPOINT}:4572`,
  s3_ssl_enabled: `${process.env.S3_SSL_ENABLED}`.toLowerCase() === 'true',
  bucket: process.env.ECHANGE_PFE_BUCKET,
  s3ForcePathStyle: true,
};
