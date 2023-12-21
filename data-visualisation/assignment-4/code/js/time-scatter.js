"use strict";
const data = [
    { time: 1, x: 100, y: 150, color: 'red', size: 10 },
    { time: 2, x: 200, y: 100, color: 'blue', size: 12 },
    { time: 3, x: 300, y: 200, color: 'green', size: 8 },
    { time: 4, x: 400, y: 50, color: 'purple', size: 15 },
    { time: 5, x: 500, y: 250, color: 'orange', size: 10 },
    { time: 6, x: 150, y: 300, color: 'pink', size: 9 },
    { time: 7, x: 250, y: 350, color: 'yellow', size: 11 },
    { time: 8, x: 350, y: 400, color: 'cyan', size: 14 },
    { time: 9, x: 450, y: 450, color: 'magenta', size: 10 },
    { time: 10, x: 550, y: 100, color: 'brown', size: 13 }
];
const width = 200;
const height = 200;
const x = d3.scaleLinear()
    .range([10, width - 10])
    .domain(d3.extent(data, d => d.x));
const y = d3.scaleLinear()
    .range([10, height - 10])
    .domain(d3.extent(data, d => d.y));
// Create SVG container
const svg = d3.select('#time-scatter').append('svg')
    .attr('width', width)
    .attr('height', height);
// Create a time scale for the scrubber
const timeScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.time)])
    .range([0, width]);
// Create scrubber
const scrubber = svg.append('line')
    .attr('x1', 0)
    .attr('y1', 0)
    .attr('x2', 0)
    .attr('y2', height)
    .attr('stroke', 'black');
// Function to update the position of the scrubber and display points
const update = (time) => {
    console.log(time);
    scrubber.attr('x1', timeScale(time))
        .attr('x2', timeScale(time));
    const points = svg.selectAll('.data-point')
        .data(data.filter(d => time - 1 < d.time && d.time <= time), d => `${d.x}-${d.y}`);
    // Enter selection - new elements
    points.enter().append('circle')
        .attr('class', 'data-point')
        .attr('cx', d => x(d.x))
        .attr('cy', d => y(d.y))
        .attr('r', d => d.size)
        .attr('fill', d => d.color)
        .style('opacity', 1) // Start fully visible
        // Transition to fade out
        .transition()
        .duration(2000)
        .style('opacity', 0)
        .remove();
    // // Exit selection - elements to remove
    // points.exit()
    //   .transition()
    //   .duration(5)
    //   .style('opacity', 0)
    //   .remove();
};
// Animate scrubber
d3.interval((elapsed) => {
    const currentTime = Math.floor((elapsed / 1000) % 4); // Assuming time in your data is in seconds
    update(currentTime);
}, 1000); // Update every second
//# sourceMappingURL=time-scatter.js.map