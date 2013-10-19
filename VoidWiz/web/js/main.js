/*

# Author: Christina Christodoulakis
# 
#    Copyright 2013 Christina Christodoulakis
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
*/

$(document).ready(function() {

    visits = "{}";
    $.ajax({
        'async': false,
        'global': false,
        'url': 'controller?action=GETPVSTS',
        'dataType': "json",
        'success': function(data) {
            visits = data;
        }
    });
    $("#tuple_preview").empty();
    html = "<table id=\"tuple_preview_table\" class=\"table table-bordered\">\n\
            <th class=\"span1\"> # </th>\n\
            <th class=\"span5\"> Patient Name </th>\n\
            <th class=\"span5\"> Doctor Name </th>\n\
            <th class=\"span5\"> Diagnosis </th>\n\
            <th class=\"span1\"> Treatment </th>\n\
<tbody>\n\ ";
    $.each(visits.patientVisits, function(i, item) {
        if (item.treatment === "" || item.treatment === "NULL")
            html = html + "<tr class=\"error\" id=\"datarow" + i + "\">\n\ ";
        else
            html = html + "<tr id=\"datarow" + i + "\">\n\ ";
        html = html + "<td >" + i + "</td>\n\
<td >" + item.patientName + "</td>\n\
<td >" + item.doctorName + "</td>\n\
<td >" + item.diagnosis + "</td>\n\
<td id=\"tbl_drug" + i + "\">" + item.treatment + "</td>\n\
</tr>\n\ ";
    });
    html = html + "</tbody></table>";
    $("#tuple_preview").append(html);
});

function retrieveBBP() {
    probs = "{}";
    $.ajax({
        'async': false,
        'global': false,
        'url': 'controller?action=RNBBP',
        'dataType': "json",
        'success': function(data) {
            probs = data;
        },
        'error': function() {
            alert("woe is me, there is something fishy with the deployment. Sorry, no json for you... Make sure your script is being executed?");
        }
    });
    myarray = probs.probableNodes;
    sortJsonArrayByProperty(myarray, 'prob', -1);

    $("#bbp_results").empty();
    html = "<p>Most probable links for node 3 of type perscription (in green):</p>\n\
<table id=\"bbp_results_table\" class=\"table table-bordered\">\n\
            <th class=\"span1\"> Value </th>\n\
            <th class=\"span1\"> Prob <a id=\"bbptbl_probheader\" href=\"#\" title=\"Rounded to 3 decimal points.\" rel=\"tooltip\"><i class=\"icon-info\"></i></a></th>\n\
<th>Accept</th><tbody>\n\ ";

    $.each(myarray, function(i, item) {
        if (dnodes[item.id - 1].type === "perscription"){
//            html = html + "<tr class=\"success\" >\n\ ";
//        else
            html = html + "<tr >\n\ ";
        html = html + "<td >" + dnodes[item.id - 1].name + "</td>\n\
<td >" + parseFloat(item.prob, 10).toFixed(3) + "</td>";
       // if (dnodes[item.id - 1].type === "perscription")
            html = html + "<td>\n\
<a href=\"#\" title=\"Select to use this value for the missing data.\" \n\
class=\"linkInfo\" rel=\"tooltip\"  \n\
onclick=\"acceptValue(2," + item.id + "," + i + ")\"><i id=\"thumb" + i + "\" class=\"icon-thumbs-up-alt\"></i></a></td></tr>";

        //else
            //html = html + "<td><i id=\"thumb" + i + "\" class=\"icon-thumbs-up-alt\"></i></td></tr>";
            }

    });
    html = html + "</tbody></table>";
    $("#bbp_results").append(html);
    //have to activate the tooltip HERE, not on document load!!! (we just created it silly!!)
    $(".linkInfo").tooltip({trigger: "hover", placement: 'bottom'});
    $("#bbptbl_probheader").tooltip({trigger: "hover", placement: 'bottom'});
}

function acceptValue(sid, tid, i) {
    targetid = tid - 1;
    alert("Adding a link between " + dnodes[sid].name + " and " + dnodes[targetid].name);
    $('#thumb' + i).addClass('icon-thumbs-up').removeClass('icon-thumbs-up-alt');
    dlinks.push({source: sid, target: targetid, value: 1, age: "new"});
    start();

    $("#tbl_drug" + dnodes[sid].name).append(dnodes[targetid].name);
    resolvedNulls(dnodes[sid].name);
    $('#datarow' + dnodes[sid].name).addClass('warning-cc').removeClass('error');
}


function alertNulls(nodeid) {
    $("#null_node").empty();
    html = "<span style=\"font-size:100%\" class=\"label label-important\">Node " + nodeid + " is missing a link  <i class=\"icon-frown\"></i></span>";
    $("#null_node").append(html);
}
function resolvedNulls(nodeid) {
    $("#null_node").empty();
    html = "<span style=\"font-size:100%\" class=\"label label-warning-cc\">Node " + nodeid + " missing link is resolved  <i class=\"icon-smile\"></i></span>";
    $("#null_node").append(html);
}
function sortJsonArrayByProperty(objArray, prop, direction) {

    if (arguments.length < 2)
        throw new Error("sortJsonArrayByProp requires 2 arguments");
    var direct = arguments.length > 2 ? arguments[2] : 1; //Default to ascending

    if (objArray && objArray.constructor === Array) {
        var propPath = (prop.constructor === Array) ? prop : prop.split(".");
        objArray.sort(function(a, b) {
            for (var p in propPath) {
                if (a[propPath[p]] && b[propPath[p]]) {
                    a = a[propPath[p]];
                    b = b[propPath[p]];
                }
            }
            // convert numeric strings to integers
            a = a.match(/^\d+$/) ? +a : a;
            b = b.match(/^\d+$/) ? +b : b;
            return ((a < b) ? -1 * direct : ((a > b) ? 1 * direct : 0));
        });
    }
}

