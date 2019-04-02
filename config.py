# Update the config for your instance and table you want to query.

username='user'
password='pass' 
table='ast_contract'
query='active=true' #your encoded query string
URI='https://SOURCE.service-now.com'
URI_Attachments='https://SOURCE.service-now.com/DownloadAttachment.do?'
OUTPUT_FILE_PATH='FULLPATH/attachment-runner/output.xlsx' 
ATTACHMENT_EXTRACTION_PATH="FULLPATH/attachment-runner/attachments/"
FAILED_ATTACHMENT_PATH='FULLPATH/attachment-runner/failed_attachments/'
ATTACHMENT_LOG_PATH="FULLPATH/attachment-runner/download-log.xlsx"
CORRELATION_FIELD_NAME="u_correlation_id"
ATTACHMENT_RESOURCE="/api/acusa/attachmentrunner" #CHANGE ME
TARGET_INSTANCE="https://TARGET.service-now.com"

