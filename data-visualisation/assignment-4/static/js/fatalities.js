"use strict";
console.log("ok");
function on_response(response) {
    if (!response.ok) {
        throw new Error("failed to fetch data");
    }
    return response.json();
}
function on_data(data) {
    console.log(data);
    d3.select("#fatalities-1").selectAll("*").remove();
    const width = 500;
    const height = 300;
    const margin = { top: 10, right: 30, bottom: 30, left: 40 };
    data.forEach(d => d.parsed_date = d3.timeParse("%Y-%m-%d")(d.date_of_event));
    data.sort((a, b) => a.parsed_date - b.parsed_date);
    const svg = d3.select('#fatalities-1')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    const x = d3.scaleTime()
        .domain(d3.extent(data, d => d.parsed_date))
        .range([0, width - margin.left - margin.right]);
    const xAxis = svg.append("g")
        .attr("transform", `translate(0,${margin.top})`)
        .call(d3.axisTop(x));
    const histogram = d3.histogram()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(x.ticks(d3.timeDay.every(100)));
    const bins = histogram(data);
    const y = d3.scaleLinear()
        .range([height - margin.top - margin.bottom, 0])
        .domain([d3.max(bins, d => d.length), 0]);
    // const yAxis = svg.append("g")
    //    .call(d3.axisLeft(y));
    svg.selectAll("rect")
        .data(bins)
        .enter()
        .append("rect")
        .attr("x", d => x(d.x0) + 1)
        .attr("y", d => margin.top)
        .attr("width", d => {
        const width = Math.max(0, x(d.x1) - x(d.x0));
        console.log(width);
        return width;
    })
        .attr("height", d => y(d.length))
        .style("fill", "#69b3a2");
}
fetch('/static/json/fatalities.json')
    .then(on_response)
    .then(on_data);
//# sourceMappingURL=fatalities.js.map