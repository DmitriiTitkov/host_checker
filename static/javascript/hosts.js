// const
const urls = {
    addHost: window.location.href + "hosts",
    removeHost: window.location.href + "/users/{login}/hosts/{host_id}",
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

function removeHostForUser (login, host_id){
    $.ajax({
	    url: "/users/" + login "/hosts/" + host_id,
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