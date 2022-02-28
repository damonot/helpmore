// IPXAPI
function ipxapi(ip) {
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://ipxapi.com/api/ip?ip="+ip,
        "method": "GET",
        "headers": {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": "Bearer 825|TYdYvsByrjJPNR7qk7srT1I1BJk5EEsPskHS4tk4",
          "cache-control": "no-cache"
        },
        "processData": false
      }
      
      $.ajax(settings).done(function (response) {
        console.log(response);
    });    
}