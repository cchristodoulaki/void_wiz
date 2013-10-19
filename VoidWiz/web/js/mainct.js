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
    $('#Graph').tab('show');
    $('#Tabular').tab('show');
    ct = "{}";
    $.ajax({
        'async': true,
        'global': false,
        'url': 'controller?action=GETCT',
        'dataType': "json",
        'success': function(data) {ct = data;
            $("#tuple_preview").empty();
    html = "<table id=\"tuple_preview_table\" class=\"table table-bordered tablesorter\">\n\<thead><tr><th class=\"span1\"> # </th>\n\
<th class=\"span3\"> CTID </th>\n\
            <th class=\"span4\"> Source </th>\n\
            <th class=\"span4\"> Condition </th>\n\
            <th class=\"span3\"> Drug </th></tr></thead>\n\
<tbody>\n\ ";
    $.each(ct.trials, function(i, item) {
        if (item.drug === "" || item.drug === "NULL")
            html = html + "<tr class=\"error\" id=\"datarow" + i + "\">\n\ ";
        else
            html = html + "<tr id=\"datarow" + i + "\">\n\ ";
        html = html + "<td >" + i + "</td>\n\<td >" + item.ctid + "</td>\n\
<td >" + item.source + "</td>\n\
<td >" + item.medcondition + "</td>\n\
<td id=\"ct_drug" + i + "\">" + item.drug + "<a href=\"javascript:removeDrug(" + i + ",'" + item.ctid + "','" + item.drug + "');\" > <span style=\"color:'red';\">x</span></a></td>\n\
</tr>\n\ ";
    });
    html = html + "</tbody></table>";
    $("#tuple_preview").append(html);

    jQuery.noConflict();
    $("#tuple_preview_table").tablesorter({sortList: [[0, 0], [1, 0]]});//sort first and second column ascending
        },
        'error': function() {alert("Nothing to see here, move along, move along... ")}
    });
    
});

// todo: if there is only one link to the target, it will be removed but the node will remain!
function removeLink(nodeA, nodeB) {
    Aindx = getIndxOf(dnodes, nodeA);
    Bindx = getIndxOf(dnodes, nodeB);
    rmv(dlinks, Aindx, Bindx);
    alert("Attempting to redraw graph");
    magic();
}

function getIndxOf(nodearray, nodename) {
    $.each(nodearray, function(index, value) {
        if (value.name === nodename)
            return index;
    });
}
function rmv(array, src, trg) {
    dlinks = $.grep(array, function(element, index) {
        return !(element.source === src && element.target === trg)
    });
}
//todo
// tell server to remove row with ctid and drug
// recompute/and redraw graph
// add bbp button to cell
// ATTENTION!!! information isbeing lost using ctid as the source node. should use the tuple identifier

function removeDrug(i, ctid, drug) {
    alert("remove element under construction.");
    console.log("clicked remove drug");
    // first remove link from file used by BBP
    // then on success remove link from json object in browser memory

    $.ajax({
        'async': false,
        'global': false,
        'url': 'controller?action=RMVDRG&ctid=' + ctid + '&drg=' + drug,
        'dataType': "text",
        'success': function(data) {
            removeLink(ctid, drug);
            alert(data);
        },
        'error': function() {
            alert("Recieved error from server. Implementation not complete.")
        }
    });

    $("#ct_drug" + i).empty();

}

function retrieveBBPct() {
    var attrtype = dnodes[selected].type;
    var attrname = dnodes[selected].name;
    $("#runBBPbtn").addClass("active");
    $("#bbp_results").empty();
    $("#bbp_results").append("<p>Predicting links...</p><img src=\"img/ajax-loader.gif\"\>");
    $.ajax({
        'async': true,
        'global': false,
        'url': 'controller?action=RNBBPCT&nodeid=' + selected + '&attrtype=' + attrtype + '&attrname=' + attrname,
        'dataType': "json",
        'success': function(data) {
            myarray = data.probableNodes;
            sortJsonArrayByProperty(myarray, 'prob', -1);

            $("#bbp_results").empty();
            html = "<p>Most probable new links for node " + attrname + " (" + attrtype + " " + selected + "):</p>\n\
<table id=\"bbp_results_table\" class=\"table table-bordered\">\n\
            <th class=\"span1\"> Value </th>\n\
            <th class=\"span1\"> Prob <a id=\"bbptbl_probheader\" href=\"#\" title=\"Rounded to 3 decimal points.\" rel=\"tooltip\"><i class=\"icon-info\"></i></a></th>\n\
<th>Accept</th><tbody>\n\ ";

            $.each(myarray, function(i, item) {
                if (dnodes[item.id].type !== attrtype && dnodes[item.id].type !== "tuple_identifier" && dnodes[item.id].type !== "ctid") {
                    html = html + "<tr >\n\ ";
                    html = html + "<td >" + dnodes[item.id].name + "</td>\n\
<td >" + parseFloat(item.prob, 10).toFixed(3) + "</td>";
                    html = html + "<td>\n\
<a href=\"#\" title=\"Select to see new link in graph.\" \n\
class=\"linkInfo\" rel=\"tooltip\"  \n\
onclick=\"acceptValue(" + selected + "," + item.id + "," + i + ")\"><i id=\"thumb" + i + "\" class=\"icon-thumbs-up-alt\"></i></a></td></tr>";
                }

            });
            html = html + "</tbody></table>";
            $("#bbp_results").append(html);
            $("#runBBPbtn").removeClass("active");
            $("#runBBPbtn").addClass("disabled");
            //have to activate the tooltip HERE, not on document load!!! (we just created it silly!!)
            $(".linkInfo").tooltip({trigger: "hover", placement: 'bottom'});
            $("#bbptbl_probheader").tooltip({trigger: "hover", placement: 'bottom'});
        },
        'error': function() {
            alert("Sorry, we've hit a glitch :S");
        }
    });

}

function acceptValue(sid, tid, i) {
    targetid = tid;
    alert("Adding a link between " + dnodes[sid].name + " and " + dnodes[targetid].name);
    $('#thumb' + i).addClass('icon-thumbs-up').removeClass('icon-thumbs-up-alt');
    dlinks.push({source: sid, target: targetid, value: 1, age: "new"});
    start();
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

function populateCTTable() {

    var attrtype = dnodes[selected].type;
    var attrname = dnodes[selected].name;
    $.ajax({
        'async': true,
        'global': false,
        'url': 'controller?action=FILTR&nodeid=' + selected + '&attrtype=' + attrtype + '&attrname=' + attrname,
        'dataType': "json",
        'success': function(data) {
            $("#filtered_data").empty();
            html = "<table id=\"filter_table\" class=\"table table-bordered tablesorter\"> <colgroup><col></col><col class=\"";
            if (attrtype === "ctid")
                html = html + "warning";
            html = html + "\"></col><col class=\"";
            if (attrtype === "source")
                html = html + "warning";
            html = html + "\"></col> <col class=\"";
            if (attrtype === "medcondition")
                html = html + "warning";
            html = html + "\"></col><col class=\"";
            if (attrtype === "drug")
                html = html + "warning";
            html = html + "\"></col></colgroup><thead><tr><th class=\"span1\"> # </th>\n\
<th class=\"span3\"> CTID </th>\n\
            <th class=\"span4\"> Source </th>\n\
            <th class=\"span4\"> Condition </th>\n\
            <th class=\"span3\">  Drug </th></tr></thead>\n\
<tbody>";
            $.each(data.trials, function(i, item) {
                html = html + "<tr id=\"datarow" + i + "\"><td >" + i + "</td>\n\
<td class=\"\"> " + item.ctid + "</td>\n\
<td class=\"\">" + item.source + "</td>\n\
<td class=\"\">" + item.medcondition + "</td>\n\
<td id=\"ct_drug" + i + "\"class=\"\">" + item.drug + "</td>\n\
</tr>";
            });
            html = html + "</tbody></table>";
            $("#filtered_data").append(html);
               jQuery.noConflict();
    $("#filter_table").tablesorter({sortList: [[0, 0], [1, 0]]});//sort first and second column ascending
        
        },
        'error': function() {
            alert("Server not returning valid json, sorry");
        }
    });
}

function addBBPtools() {
    var attrtype = dnodes[selected].type;
    var attrname = dnodes[selected].name;
    $("#bbp_results").empty();
    $("#toolbox").empty();
    html = "Selected node: " + attrname;
//    html = html + "<div class=\"btn-group\">"+
//"  <button type=\"button\" class=\"btn btn-default btn-xs dropdown-toggle\" data-toggle=\"dropdown\"> All <span class=\"caret\"></span>"
//  +"</button><ul class=\"dropdown-menu\" role=\"menu\">"+
//"    <li><a href=\"#\">All</a></li>"+
//"    <li><a href=\"#\">Source</a></li>"+
//"    <li><a href=\"#\">Condition</a></li>"+
//"    <li><a href=\"#\">Drug</a></li>"+
//"    </ul></div>";
    html = html + "<p><a id=\"runBBPbtn\" class=\"btn btn-info \" href=\"javascript:retrieveBBPct();\">Predict links</a></p>"
    $("#toolbox").append(html);
}

