/*
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
