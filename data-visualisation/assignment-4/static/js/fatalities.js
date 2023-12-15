const config = {
    debug: true,
    test: true,
    scrubber: {
        paused: false,
        height: 5,
        width: 300,
        width_real_ms: 1000,
    }
};
const ISRAELI_BLUE = "#0038b8";
const PALESTINIAN_RED = "#EE2A35";
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
class TimeInterval {
    constructor(end, length) {
        this.start = end - length;
        this.end = end;
        if (this.start > this.end)
            throw Error("can't have start after end");
        this.start_noon = get_noon_epoch_time(this.start);
        this.end_noon = get_noon_epoch_time(this.end);
        if (this.end_noon > this.end) {
            this.end_noon = this.end_noon - ONE_DAY_MS;
        }
        this.elapsed_noons = [];
        if (this.start <= this.start_noon && this.end >= this.start_noon) {
            this.elapsed_noons.push(this.start_noon);
        }
        let current_noon = this.start_noon + ONE_DAY_MS;
        while (current_noon <= this.end_noon) {
            this.elapsed_noons.push(current_noon);
            current_noon = current_noon + ONE_DAY_MS;
        }
    }
}
function interval_to_data(data, interval) {
    let fatalities = [];
    for (const noon of interval.elapsed_noons) {
        const new_noons = data.get(noon);
        if (new_noons instanceof Array) {
            fatalities.push(...new_noons);
        }
    }
    return fatalities;
}
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
function create_thresholds(startDate, endDate, days) {
    const thresholds = [startDate];
    let currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        currentDate = new Date(currentDate.getTime() + days * 86400000); // Add 'days' days
        thresholds.push(currentDate);
    }
    return thresholds;
}
function days_to_ms(days) {
    return days * days_to_ms.factor;
}
days_to_ms.factor = 24 * 60 * 60 * 1000;
function ms_to_days(ms) {
    return ms / days_to_ms.factor;
}
function get_noon_epoch_time(milliseconds) {
    let date = new Date(milliseconds);
    date.setHours(12, 0, 0, 0);
    return date.getTime();
}
function yeet(error_msg) {
    throw new Error(error_msg);
}
const debug = {
    noon_times(noon_time_to_fatalities) {
        for (const k of noon_time_to_fatalities.keys()) {
            console.log(new Date(k));
        }
    }
};
export function on_data(data) {
    var _a, _b;
    d3.select("#vis").selectAll("*").remove();
    const width = window.innerWidth * 0.9;
    const height = 350 * 2;
    const margin = { top: 200, right: 30, bottom: 20, left: 30 };
    const histogram_center = 300;
    const histogram_height = 100;
    const histogram_width = width - margin.left - margin.right;
    const scatterPlotArea = {
        width: histogram_width,
        height: 200,
        x: 50, // x-coordinate of the top-left corner of the scatter plot area
        y: 50, // y-coordinate of the top-left corner of the scatter plot area
    };
    const age_range = d3.extent(data, d => d.age);
    console.log(age_range);
    const age_scale = d3.scaleLinear()
        .domain(age_range)
        .range([scatterPlotArea.height + scatterPlotArea.y, scatterPlotArea.y]);
    // const age_scale_invert = d3.scaleLinear()
    //     .range([0, scatterPlotArea.height])
    //     .domain(age_range);
    // Create the yAxis generator
    const yAxis = d3.axisLeft(age_scale);
    function calculateMeanAge(data) {
        const totalAges = data.reduce((sum, fatality) => sum + fatality.age, 0);
        const meanAge = totalAges / data.length;
        return meanAge;
    }
    // Assuming 'data' is the array of Fatality objects
    const meanAge = calculateMeanAge(data);
    console.log('Mean Age:', meanAge);
    function addToScatterPlot(dataItem) {
        // Generate a random position within the scatter plot area
        const xPosition = Math.random() * scatterPlotArea.width; // + scatterPlotArea.x;
        // Append a new circle to the SVG for each data item
        svg.append("circle")
            .attr("class", "fatality")
            .attr("r", 5)
            .data([dataItem]) // radius of the circle
            .attr("cx", xPosition)
            .attr("cy", d => age_scale(d.age))
            .style("fill", d => {
            if (d.citizenship === "Israeli")
                return ISRAELI_BLUE;
            if (d.citizenship === "Palestinian")
                return PALESTINIAN_RED;
            return 'white';
        })
            .on("mouseover", function (event, d) {
            // Show additional information on hover
            console.log(d.age);
            const tooltip = d3.select("#tooltip")
                .style("left", event.pageX + "px")
                .style("top", event.pageY + "px")
                .style("opacity", 1)
                .html(`<strong>Name:</strong> ${d.name}<br>
                            <strong>Age:</strong> ${d.age}<br>
                            <strong>Citizenship:</strong> ${d.citizenship}<br>
                            <strong>Date of Death:</strong> ${d.date_of_death}<br>
                            <strong>Notes:</strong> ${d.notes}`);
        })
            .on("mouseout", function (event, d) {
            // Hide the tooltip on mouseout
            d3.select("#tooltip")
                .style("opacity", 0);
        });
    }
    const noon_time_to_fatalities = new Map();
    data.forEach(d => {
        d.parsed_date = parse_date(d.date_of_death);
        d.parsed_date.setHours(12, 0, 0, 0);
        d.parsed_date_ms = d.parsed_date.getTime();
        const fatalities_list = noon_time_to_fatalities.get(d.parsed_date_ms);
        if (fatalities_list) {
            fatalities_list.push(d);
        }
        else {
            noon_time_to_fatalities.set(d.parsed_date_ms, [d]);
        }
    });
    debug.noon_times(noon_time_to_fatalities);
    data.sort((a, b) => a.parsed_date_ms - b.parsed_date_ms);
    const israeli_deaths = data.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = data.filter(d => d.citizenship === "Palestinian");
    const svg = d3.select('#vis')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    // Append the yAxis to the SVG
    svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis);
    svg.selectAll(".y-axis path")
        .style("stroke", "white");
    svg.selectAll(".y-axis text")
        .style("fill", "white");
    svg.selectAll(".y-axis line")
        .style("stroke", "white");
    // Function to handle pause button click
    function onPauseClicked() {
        config.scrubber.paused = !config.scrubber.paused;
    }
    const pauseButton = svg.append('g')
        .attr('class', 'pause-button')
        .attr('cursor', 'pointer')
        .on('click', onPauseClicked); // Attach click callback
    // Add the pause button shape (for example, a square)
    pauseButton.append('rect')
        .attr('x', 10) // Adjust position as needed
        .attr('y', 10) // Adjust position as needed
        .attr('width', 30) // Adjust size as needed
        .attr('height', 30) // Adjust size as needed
        .attr('fill', 'red'); // Color for the pause button, change as desired
    // Add a text label to the pause button (optional)
    pauseButton.append('text')
        .attr('x', 25) // Adjust position as needed
        .attr('y', 30) // Adjust position as needed
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .text('Pause'); // Text for the button, change as desired
    data.forEach(addToScatterPlot);
    const dateRange = d3.extent(data, d => d.parsed_date);
    const time_zero = dateRange[0].getTime();
    const totalMilliseconds = dateRange[1].getTime() - time_zero;
    const daysPerSecond = 365 / 2;
    const days_data_per_ms_real = daysPerSecond / 1000;
    const ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
    const framesPerSecond = 60;
    const frames_per_ms = 1000 / framesPerSecond;
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);
    config.scrubber.width = real_ms_to_width(config.scrubber.width_real_ms);
    const scrubber = svg.append('rect')
        .attr('x', 0)
        .attr('y', histogram_center)
        .attr('width', config.scrubber.width)
        .attr('height', config.scrubber.height)
        .attr('opacity', 0.3)
        .attr('stroke', 'white')
        .call(d3.drag() // Apply drag behavior
        .on('start', dragStarted)
        .on('drag', dragging)
        .on('end', dragEnded));
    // Functions to handle drag events
    function dragStarted(event, d) {
        // Handle the start of the drag event
        config.scrubber.paused = true;
    }
    const padding_time = real_ms_to_data_ms(config.scrubber.width_real_ms);
    const scrub_x = d3.scaleTime()
        .domain([time_zero - padding_time, dateRange[1].getTime()])
        .range([-config.scrubber.width, histogram_width])
        .clamp(false);
    const r = [time_zero - padding_time, dateRange[1].getTime()];
    const max_real_ms = data_ms_to_real_ms(((_a = dateRange[1]) === null || _a === void 0 ? void 0 : _a.getTime()) - ((_b = dateRange[0]) === null || _b === void 0 ? void 0 : _b.getTime()));
    const scrub_x_real_ms = d3.scaleLinear()
        .domain([0, histogram_width])
        .range([0, max_real_ms])
        .clamp(false);
    function histogram_tick(elapsed) {
        elapsed_real_ms_diff = elapsed - elapsed_real_ms_last;
        if (!config.scrubber.paused) {
            elapsed_real_ms_virtual += elapsed_real_ms_diff;
            looped_epoch_time = positiveModulo(elapsed_real_ms_virtual * ms_data_per_ms_real, totalWidthMilliseconds);
            current_time_right_ms = time_zero + looped_epoch_time;
            current_time_left_ms = current_time_right_ms - padding_time;
            const x_val = scrub_x(current_time_left_ms);
            const real_x = d3.max([0, x_val]) || 0;
            const subtraction_left = d3.min([x_val, 0]) || 0;
            const width = d3.min([config.scrubber.width, histogram_width - real_x]) + subtraction_left;
            scrubber
                .attr('x', real_x)
                .attr('width', Math.abs(width));
            update_scatter();
        }
        elapsed_real_ms_last = elapsed;
    }
    function dragging(event, d) {
        const newX = event.x;
        let elapsed_real_ms = scrub_x_real_ms(newX);
        if (elapsed_real_ms < 0) {
            elapsed_real_ms = max_real_ms + elapsed_real_ms;
        }
        elapsed_real_ms_virtual = elapsed_real_ms;
        elapsed_real_ms_last = 0;
        looped_epoch_time = (elapsed_real_ms * ms_data_per_ms_real) % totalWidthMilliseconds;
        current_time_right_ms = time_zero + looped_epoch_time;
        current_time_left_ms = current_time_right_ms - padding_time;
        const x_val = scrub_x(current_time_left_ms);
        const real_x = d3.max([0, x_val]) || 0;
        const subtraction_left = d3.min([x_val, 0]) || 0;
        const width = d3.min([config.scrubber.width, histogram_width - real_x]) + subtraction_left;
        scrubber
            .attr('x', real_x)
            .attr('width', width);
        update_scatter();
        if (config.debug) {
            // Add a circle at the dragged position
            svg.append("circle")
                .attr("cx", newX)
                .attr("cy", 50) // Adjust the y-position as needed
                .attr("r", 5)
                .attr("fill", "red")
                .transition()
                .duration(1000) // Disappear over 1 second
                .style("opacity", 0)
                .remove();
        }
    }
    function dragEnded(event, d) {
        config.scrubber.paused = false;
        // update_scatter()
    }
    const totalWidthMilliseconds = totalMilliseconds + padding_time;
    function width_to_ms_data(widthInPixels) {
        const oneDayPixelValue = scrub_x(new Date(time_zero + days_to_ms(1)));
        const days = widthInPixels / oneDayPixelValue;
        return days * (1000 / days_data_per_ms_real);
    }
    // function width_to_ms_real(width: number) {
    //     const one_day_in_pixels =
    // }
    function data_ms_to_width(data_ms) {
        const one_day_in_pixels = x(new Date(time_zero + days_to_ms(1)));
        const one_ms_in_pixels = one_day_in_pixels / ONE_DAY_MS;
        return data_ms * one_ms_in_pixels;
    }
    function real_ms_to_width(real_ms) {
        return data_ms_to_width(real_ms_to_data_ms(real_ms));
    }
    function real_ms_to_data_ms(ms_real) {
        return ms_real * ms_data_per_ms_real;
    }
    function data_ms_to_real_ms(ms_data) {
        return ms_data / ms_data_per_ms_real;
    }
    if (config.test) {
        const real_ms = 1000;
        const data_ms = real_ms_to_data_ms(real_ms);
        const out = data_ms_to_real_ms(data_ms);
        if (real_ms !== out) {
            throw new Error("inverse ms broken ${in} ${out}");
        }
    }
    const opacity_scale = d3.scaleLinear()
        .domain([real_ms_to_data_ms(config.scrubber.width_real_ms), 0])
        .range([0, 1]);
    let elapsed_real_ms_last = 0;
    let elapsed_real_ms_virtual = 0;
    let elapsed_real_ms_diff = 0;
    let looped_epoch_time = (elapsed_real_ms_virtual * ms_data_per_ms_real) % totalWidthMilliseconds;
    let current_time_right_ms = time_zero + looped_epoch_time;
    let current_time_left_ms = current_time_right_ms - padding_time;
    const dateText = svg.append("text")
        .attr("class", "date-text")
        .attr("text-anchor", "start")
        .attr("fill", "white");
    const dateFormat = d3.timeFormat("%Y %b %d");
    function update_scatter() {
        svg.selectAll(".fatality")
            .style("opacity", (d) => {
            const diff = current_time_right_ms - d.parsed_date_ms;
            if (diff < 0)
                return 0;
            return opacity_scale(diff);
        });
        const text = dateFormat(new Date(current_time_right_ms));
        const x = Number(scrubber.attr("x")) + Number(scrubber.attr("width"));
        const y = Number(scrubber.attr("y")) + 30;
        dateText.text(text)
            .attr("x", x)
            .attr("y", y);
    }
    function positiveModulo(dividend, divisor) {
        return ((dividend % divisor) + divisor) % divisor;
    }
    d3.interval(histogram_tick, frames_per_ms);
    const xAxis = svg.append("g")
        .attr("transform", `translate(0,${margin.top})`);
    const thresholds = create_thresholds(dateRange[0], dateRange[1], 14);
    const histogram = d3.bin()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(thresholds);
    const israeli_bins = histogram(israeli_deaths);
    const palestinian_bins = histogram(palestinian_deaths);
    const y_range = height - margin.top - margin.bottom;
    const rect_height = d3.scaleLinear()
        .range([histogram_height, 0])
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
        .attr("y", d => histogram_center + config.scrubber.height)
        .attr("width", d => bin_width(d))
        .attr("height", d => rect_height(d.length))
        .style("fill", ISRAELI_BLUE);
    svg.selectAll(".palestinian-rect")
        .data(palestinian_bins)
        .enter()
        .append("rect")
        .attr("class", "palestinian-rect")
        .attr("x", d => x(d.x0))
        .attr("y", d => histogram_center - rect_height(d.length))
        .attr("width", d => bin_width(d))
        .attr("height", d => rect_height(d.length))
        .style("fill", PALESTINIAN_RED);
}
fetch('/static/json/fatalities.json')
    .then(on_response)
    .then(on_data);
//# sourceMappingURL=fatalities.js.map