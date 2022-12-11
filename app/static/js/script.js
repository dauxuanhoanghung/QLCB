function getFlights(fromAirportId, toAirportId, date) {
    fetch("/booking", {
        method: "post",
        body: JSON.stringify({
            "fromAirport": fromAirportId,
            "toAirport": toAirportId,
            "trip-start": date
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
    })
}

function addToCart(id, name, price) {
    fetch("/booking", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) { return res.json() }).then(function(data) {
        console.log(data)
    })
}