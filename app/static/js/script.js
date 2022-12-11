function getFlights(fromAirportId, toAirportId, date) {
    let json = JSON.stringify({
        "fromAirport": fromAirportId,
        "toAirport": toAirportId,
        "trip-start": date
    })
    fetch("/booking", {
        method: "post",
        body: json,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(f => {
        let html = '<div class="row">'
        f.forEach(e => html += `
            <div class="col-md-3 col-sm-6 flight" id=flight${e.id} style="padding:1.5rem;">
                <a href="/flight/${e.id}">
                    <div class="flight-image">
                        <img src="static/images/${e.flight_route.departure_img}"/>
                        <img src="static/images/${e.flight_route.arrival_img}"/>
                    </div>
                    <div class="flight-info">
                        <h3 class="text-white">${e.flight_route.departure_airport} đến</h3>
                        <h3 class="text-white">${e.flight_route.arrival_airport}</h3>
                        <p class="text-white">${e.takeoff_time}</p>
                        <p class="text text-end text-white pe-4">Từ</p>
                        <h4 class="text text-end text-warning pe-4">${e.base_price} VNĐ</h4>
                    </div>
                </a>
            </div>`
        )
        document.getElementById('flights').innerHTML = html + "</div>"
    })
    .catch(err => console.log(err))
}