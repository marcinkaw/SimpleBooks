$(document).ready(function() {
    $("#dialog").dialog({
        autoOpen: false,
        modal: true
    });
});

$(".confirmLink").click(function(e) {
    e.preventDefault();
    var targetUrl = $(this).attr("href");

    $("#dialog").dialog({
    buttons : {
        "Tak" : function() {
            window.location.href = targetUrl;
        },
        "Anuluj" : function() {
            $(this).dialog("close");
        }
    }
});

$("#dialog").dialog("open");
});