"use strict";
console.log("ok");
function on_response(response) {
    if (!response.ok) {
        throw new Error("failed to fetch data");
    }
    return response.json();
}
function assert_non_null(item) {
    if (item === null) {
        throw new Error("found null item");
    }
    return item;
}
function parse_date(str) {
    return assert_non_null(d3.timeParse("%Y-%m-%d")(str));
}
function createThresholds(startDate, endDate, days) {
    const thresholds = [startDate];
    let currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        currentDate = new Date(currentDate.getTime() + days * 86400000); // Add 'days' days
        thresholds.push(currentDate);
    }
    return thresholds;
}
function on_data(data) {
    console.log(data);
    d3.select("#fatalities-1").selectAll("*").remove();
    const width = 500;
    const height = 300;
    const margin = { top: 50, right: 30, bottom: 30, left: 40 };
    data.forEach(d => d.parsed_date = parse_date(d.date_of_death));
    data.sort((a, b) => a.parsed_date - b.parsed_date);
    const israeli_deaths = data.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = data.filter(d => d.citizenship === "Palestinian");
    const svg = d3.select('#fatalities-1')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    const dateRange = d3.extent(data, d => d.parsed_date);
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, width - margin.left - margin.right]);
    const xAxis = svg.append("g")
        .attr("transform", `translate(0,${margin.top})`);
    const thresholds = createThresholds(dateRange[0], dateRange[1], 14);
    const histogram = d3.bin()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(thresholds);
    const israeli_bins = histogram(israeli_deaths);
    const palestinian_bins = histogram(palestinian_deaths);
    const y = d3.scaleLinear()
        .range([height - margin.top - margin.bottom, 0])
        // use the max of both israeli and palestinian deaths so both are on the same scale
        .domain([d3.max(histogram(data), d => d.length), 0]);
    function bin_width(d) {
        return Math.max(0, x(d.x1) - x(d.x0));
    }
    svg.selectAll("rect")
        .data(israeli_bins)
        .enter()
        .append("rect")
        .attr("x", d => x(d.x0))
        .attr("y", d => margin.top)
        .attr("width", d => bin_width(d))
        .attr("height", d => y(d.length))
        .style("fill", "#0038b8");
    svg.selectAll(".palestinian-rect")
        .data(palestinian_bins)
        .enter()
        .append("rect")
        .attr("class", "palestinian-rect")
        .attr("x", d => x(d.x0))
        .attr("y", d => margin.top - y(d.length))
        .attr("width", d => bin_width(d))
        .attr("height", d => y(d.length))
        .style("fill", "#EE2A35");
}
fetch('/static/json/fatalities.json')
    .then(on_response)
    .then(on_data);
//# sourceMappingURL=fatalities.js.map