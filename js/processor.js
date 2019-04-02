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