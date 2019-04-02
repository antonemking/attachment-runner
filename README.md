# Attachment Runner

Attachment Runner allows you to migrate records and attachments from an existing ServiceNow instance to a new one.
It also can be used to move attachments stored locally and move them to existing records in ServiceNow.

## Prerequisites

Attachment Runner requires python3 to be installed and the following imports:

1. requests
2. zipfile
3. pandas
4. pprint
5. openpyxl

os, json, io and mimetpyes should come with python3

## Setup

Update `config.py` for your usecase
```python
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
```

# Installation

### Create Processor

> In ServiceNow create a processor called DownloadAttachment with a path "DownloadAttachment" and add the follow code.

```javascript
/*
**
** Antone M King
** Add the processor to the target instance
** Name the processor and its path 'DownloadAttachment'
**
*/

var sysid = g_request.getParameter('sysparm_sys_id');
var table = g_request.getParameter('sysparm_table');

var theRecord = new GlideRecord(table);
theRecord.addQuery('sys_id', sysid);
theRecord.query();
theRecord.next();

var zipName = 'attachments.zip';

var StringUtil = GlideStringUtil;

var gr = new GlideRecord('sys_attachment');
gr.addQuery('table_sys_id', theRecord.sys_id);
gr.addQuery('table_name', theRecord.getTableName());
gr.query();

if (gr.hasNext()){
    g_response.setHeader('Pragma', 'public');
    g_response.addHeader('Cache-Control', 'max-age=0');
    g_response.setContentType('application/octet-stream');
    g_response.addHeader('Content-Disposition', 'attachment;filename=' + zipName);
    var out = new Packages.java.util.zip.ZipOutputStream(g_response.getOutputStream());
    var count=0;
    while (gr.next()){
        var sa = new GlideSysAttachment();
        var binData = sa.getBytes(gr);
        
        var file = gr.file_name;
        addBytesToZip(out, zipName, file, binData);
        count ++;
    }
    // Complete the ZIP file
    out.close();
}

function addBytesToZip (out, dir, file, stream){
    // Add ZIP entry to output stream.
    out.putNextEntry(new Packages.java.util.zip.ZipEntry(file));
    out.write(stream, 0, stream.length);
    out.closeEntry();
}
```

### Create Scripted REST API

> Create a new scripted REST API called Attachment Runner with an API ID "attachment_runner".
> Update the GET resource Relative path to `/table/{table}/correlationfield/{correfield}/correlationID/{correlationid}`.
> Add the below code to the script field

```javascript
/*
** Credit: ServiceNow Guru https://www.servicenowguru.com/scripting/download-attachments-zip-file/
** Antone M King
** API Definition: Attachment Runner
** Relative Path: /table/{table}/correlationfield/{correfield}/correlationID/{correlationid}
** Method: GET
** Assists zipPush.py to correlate the original record sys_id to the new one
*/

(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
	var table = request.pathParams.table;
	var correlationFieldName = request.pathParams.correfield;
	var correID = request.pathParams.correlationid;
	
	if(correID == ''){
		correID = 'empty';
	}
	//
	var sysId = [];
	var gr = new GlideRecord(table);
	gr.addQuery(correlationFieldName, correID);
	gr.query();
	if(gr.next()){
		sysId.push({
			sys_id: gr.getUniqueValue()
		});
		
	} else {
		sysId.push({
			sys_id: String('null')
		});
	}
	return sysId;

})(request, response);

```

#### 1. Execute the runner

Change to the attachment_runner directory and run in your terminal.

```sh
python runner.py
```
![runner](https://github.com/enotgnik/attachment-runner/screenshots/runner.png)

An output file should now exist containing all the records from the chosen table in excel. This file can be used to imported via a datasource into the new instance (transform where necessary)

#### 2. Execute the attachment pull

In the same directory run the following in your terminal.

```sh
python zipPull.py
```
![pull](https://github.com/enotgnik/attachment-runner/screenshots/zipPull.png)

A download file should now exist containing a log of all the attachments that were downloaded and the attachment directory should now contain sub directories named after the record with the attachment files within.


#### 3. Exucute the attachment push

In the same directory run the following in your terminal.

```sh
python zipPush.py
```
![push](https://github.com/enotgnik/attachment-runner/screenshots/zipPush.png)

Monitor the output and after receiving your summary a upload log should now exist showing what attachments failed and those that were a success.

## TODO:
1. improve runner to support streaming records over 10,000
2. improve file logging

## Author

ANTONE M KING


