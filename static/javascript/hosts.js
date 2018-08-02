// const
url = {
    addHost: window.location.href + "hosts"
}

function addHost(hostname, protocol, port){
    $.ajax({
	    url: url.addHost,
		type: 'POST',
		dataType: 'json',
		contentType: "application/json",
		data: JSON.stringify({
		    host: hostname,
		    protocol: protocol,
		    port: port
		})
    })
}