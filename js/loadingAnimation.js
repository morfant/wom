$body = $("body");

$(document).on({
//            ajaxStart: function() { $('#loading').load('loadingAnimation.html');    },
//            ajaxStop: function() {  $('#loading').unload('loadingAnimation.html');}    
            ajaxStart: function() {
console.log("ajaxStart");
                                },            
ajaxStop: function() {
console.log("ajaxStop");
}
           // ajaxStop: function() { $body.removeClass("loading"); }    
                 });
