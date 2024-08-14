var urlParams = new URLSearchParams(window.location.search);
var printer = urlParams.get('mac');

$(document).ready(function() {

    $("#cpurl").text(qualifyURL("cloudprint"));
    $("#cplabelurl").text(qualifyURL("cloudlabelprint"));

    UpdateDeviceTable();
    UpdateQueueTable();
    
});


function qualifyURL(url) {
    var a = document.createElement('a');
    a.href = url;
    return a.href;
}

function UpdateDeviceTable() {
    $.get("devices" )
        .done(function(data) {
            var table = "<table>"

            table += "<thead><tr><th>Device</th><th style='width: 200px'>Connection Status</th><th style='width: 150px'>Queue</th><th>Client Type</th><th>Last Connection (UTC)</th><th>Tray status</th><th></th></thead>";
            table += '<tfoot><tr><td colspan="7"><div id="no-paging">&nbsp;<a href="javascript:NewDevice();">Register A New Device</a></div></tr></tfoot>';

            for(var i = 0; i < data.length; i++)
            {
                var device = data[i];
                //var lastConnect = new Date(device.lastConnection);
                // var last_connect = new Date(1970, 0, 1);
                // console.log(device.last_poll)
                // last_connect=(device.last_poll) if (device.last_poll !== null) else new Date(1970, 0, 1);
                var last_connect = (device.last_poll != null) ? device.last_poll.toLocaleString() : "Not connected";
                table += "<tr>";
                table += "<td>" + device.devicemac + "</td>";
                table += "<td>" + device.status + "</td>";
                table += "<td>" + device.queue_name + "</td>";
                table += "<td>" + device.client_type + " (" + device.client_version + ")</td>";
                table += "<td>" + last_connect.toLocaleString() + "</td>";
                table += '<td><a href=\"javascript:clearTray(\'' + device.devicemac + '\');\">(Clear tray)</a>' + device.tray_status + '</td>';
                table += "<td>";
                table += "<a href='web/print?devicemac=" + device.devicemac +"'>Show</a>";
                table += ' <a href=\"javascript:delDevice(\'' + device.devicemac + '\');\">Delete</a>';
                table += "</td>";
                table += "</tr>"
            }

            table += "</table>"

            $("#deviceList").html(table);

            setTimeout(UpdateDeviceTable, 2000);
        })
        .fail(function() {
            setTimeout(UpdateDeviceTable, 10000);
        });               
}


function UpdateQueueTable() {
    $.get("queues")
        .done(function(data) {
            var table = "<table>"

            table += "<thead><tr><th>ID</th><th style='width: 200px'>Name</th><th style='width: 150px'>Next Position</th><th></th></thead>";
            table += '<tfoot><tr><td colspan="4"><div id="no-paging">&nbsp;<a href="javascript:NewQueue();">Add A New Queue</a></div></tr></tfoot>';

            for(var i = 0; i < data.length; i++)
            {
                var queue = data[i];

                table += "<tr>";
                table += "<td>" + queue.id + "</td>";
                table += "<td>" + queue.name + "</td>";
                table += "<td>" + queue.position + "</td>";
                table += "<td>";

                table += '<a href="javascript:delQueue(' + queue.id + `);">Delete</a>`;
                table += ' <a href="javascript:resetQueue(' + queue.id + `);">Reset</a>`;
                table += "</td>";
                
                table += "</tr>";
            }

            table += "</table>"

            $("#queueList").html(table);
            setTimeout(UpdateQueueTable, 2000);
        })
        .fail(function() {
            setTimeout(UpdateQueueTable, 10000);
        });               
}

function NewDevice()
{
    var newMac = prompt("Please enter the Mac address of the device to be registered", "");
    var newQ = prompt("Ender the ID of the queue to associate with the new device", "");

    var lowerMac = newMac.toString().toLowerCase();
    newMac = lowerMac;

    payload = {
        "devicemac": newMac,
        "queueId": newQ
    }
    $.ajax({
        type: "POST",
        url: "devices",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(payload),
        success: function (data) {
            console.log(data);
        }
    });
}

function delDevice(mac)
{
    if(confirm("Remove Device, are you sure?")){
        $.ajax({
            url: "devices",
            type: "DELETE",
            data: JSON.stringify({"devicemac": mac}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                console.log(data)
            }
        })
    }
}

function NewQueue()
{
    var newQ = prompt("Please enter the new queue name", "");
    var payload = {
        'name': newQ
    }
    $.ajax({
        type: "POST",
        url: "queues",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(payload),
        success: function (data) {
            console.log(data);
        }
    });
}

function delQueue(id)
{
    if(confirm("Remove Queue, are you sure?"))
    $.ajax({
        url: "queues",
        type: "DELETE",
        data: JSON.stringify({"id": id}),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data)
        }
    }) 
}

function clearTray(id) {
    $.ajax({
        url: "devices",
        type: "PUT",
        data: JSON.stringify({"devicemac": id}),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data);
        }
    })
}

function resetQueue(id)
{
    $.ajax({
        url: "queues",
        type: "PUT",
        data: JSON.stringify({"id": id}),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data)
        }
    }) 
}
