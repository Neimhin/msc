const global = {
    debug: true,
    test: true,
    scrubber: {
        dragging: false,
        paused: false,
        height: 10,
        width: 30,
        width_real_ms: 3000,
        click_diff: 0,
        set_width: () => { },
    },
    lazy: {
        fatalities: undefined,
        districts: undefined,
        noon_time_to_fatalities: undefined,
        type_of_injury_unique: undefined,
        type_of_injury_index: undefined,
        type_of_injury_scale: undefined,
    },
    mercator: {},
};
const ISRAELI_BLUE = "#0038b8";
const ISRAELI_BLUE_HIGHLIGHT = d3.interpolate(ISRAELI_BLUE, "white")(0.3);
const PALESTINIAN_RED = "#EE2A35";
const PALESTINIAN_RED_HIGHLIGHT = d3.interpolate(PALESTINIAN_RED, "white")(0.3);
const CENTER_LONG = 35;
const CENTER_LAT = 31;
const CENTER_COORD = [CENTER_LONG, CENTER_LAT];
d3.select("#vis").selectAll("*").remove();
const width = window.innerWidth * 0.9;
const height = 350 * 8;
const margin = { top: 200, right: 30, bottom: 20, left: 30 };
const svg_root = d3.select('#vis')
    .append('svg')
    .attr('width', width)
    .attr('height', height);
const svg = svg_root
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
const slider_width = 200;
const slider_height = 3;
const slider_center = 400;
const sliderScale = d3.scaleLinear()
    .domain([0, 100])
    .range([0, slider_width])
    .clamp(true);
const sliderDrag = d3.drag()
    .on("drag", function (event) {
    const newX = Math.max(0, Math.min(slider_width, event.x));
    handle.attr("cx", newX);
    slider_rect.attr("width", newX);
    global.scrubber.set_width(newX);
});
let slider_rect = svg.append("rect")
    .attr("width", slider_width)
    .attr("height", slider_height)
    .attr("y", slider_center)
    .attr("fill", "#ddd");
const handle = svg.append("circle")
    .attr("cx", slider_width)
    .attr("cy", slider_center + slider_height / 2)
    .attr("r", 8)
    .attr("fill", "steelblue")
    .call(sliderDrag);
function on_fatalities(d) {
    global.lazy.fatalities = d;
    global.lazy.noon_time_to_fatalities = new Map();
    global.lazy.fatalities.forEach(d => {
        d.parsed_date = parse_date(d.date_of_death);
        d.parsed_date.setHours(12, 0, 0, 0);
        d.parsed_date_ms = d.parsed_date.getTime();
        d.parsed_date_ms_with_noise = d.parsed_date_ms + Math.random() * ONE_DAY_MS;
        d.age_with_noise = d.age + Math.random();
        const fatalities_list = global.lazy.noon_time_to_fatalities.get(d.parsed_date_ms);
        if (fatalities_list) {
            fatalities_list.push(d);
        }
        else {
            global.lazy.noon_time_to_fatalities.set(d.parsed_date_ms, [d]);
        }
    });
    debug.noon_times(global.lazy.noon_time_to_fatalities);
    global.lazy.fatalities.sort((a, b) => a.parsed_date_ms - b.parsed_date_ms);
    global.lazy.type_of_injury_unique = new Set(global.lazy.fatalities.map(d => d.type_of_injury).filter(d => d));
    console.log("num types of injury:", global.lazy.type_of_injury_unique.size);
    const types_of_injury = Array.from(global.lazy.type_of_injury_unique).sort();
    const type_of_injury_map = {};
    types_of_injury.forEach((v, i) => {
        type_of_injury_map[v] = i;
    });
    function type_of_injury_index(t) {
        return type_of_injury_map[t];
    }
    global.lazy.type_of_injury_index = type_of_injury_index;
    maybe_main();
}
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
class Interval {
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }
    has(t) {
        return t > this.start && t <= this.end;
    }
    as_dates() {
        return [new Date(this.start), new Date(this.end)];
    }
    subtract_same_length(it) {
        // assuming both intervals have same length
        // case 1
        //       ..
        //    ..
        // or
        //  ..
        //       ..
        if ((it.end <= this.start) || it.start >= this.end) {
            return this.clone();
        }
        // case 2
        //    .........
        //  .........
        if (it.end > this.start && it.start <= this.start) {
            return new Interval(it.end, this.end);
        }
        // case 3
        // ......
        // ......
        if (it.start == this.start) {
            return new Interval(this.end, this.end);
        }
        // case 4
        // ...
        //  ...
        if (it.start > this.start) {
            return new Interval(this.start, it.start);
        }
    }
    clone() {
        return new Interval(this.start, this.end);
    }
}
if (global.test) {
    (() => {
        const i1 = new Interval(100, 110);
        const i2 = new Interval(50, 60);
        const sub = i1.subtract_same_length(i2);
        if (sub.start === i1.start && sub.end === i1.end) {
            console.log("test passed:", i1, "-", i2, "=", sub);
        }
        else {
            console.error("test failed:", i1, "-", i2, "=", sub);
        }
    })("subtract case 1");
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
            // console.log(new Date(k));
        }
    }
};
function data_to_lists_of_districts(fs) {
    const ret = {
        "West Bank": new Set(),
        "Gaza Strip": new Set(),
        "Israel": new Set(),
    };
    const regions = new Set(Object.getOwnPropertyNames(ret));
    function each(fatality) {
        if (global.test) {
            if (!regions.has(fatality.event_location_region)) {
                throw new Error(`data has no region: ${JSON.stringify(fatality)}`);
            }
        }
        ret[fatality.event_location_region].add(fatality.event_location_district);
    }
    fs.forEach(each);
    return ret;
}
function find_in_interval(it) {
    return global.lazy.fatalities.filter(d => {
        return it.has(d.parsed_date_ms_with_noise);
    });
}
function on_districts(d) {
    global.lazy.districts = d;
    const lat_1 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.northeast.lat);
    const lat_2 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.southwest.lat);
    const lng_1 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.northeast.lng);
    const lng_2 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.southwest.lng);
    const extent_lat = d3.extent(lat_1.concat(lat_2));
    const extent_lng = d3.extent(lng_1.concat(lng_2));
    const bounds = [
        [extent_lng[0], extent_lat[0]],
        [extent_lng[1], extent_lat[1]]
    ];
    global.mercator = {};
    global.mercator.extent_lat = extent_lat;
    global.mercator.extent_lng = extent_lng;
    global.mercator.bounds = bounds;
    global.mercator.center = [d3.mean(extent_lng), d3.mean(extent_lat)];
    // console.log(bounds);
    // console.log(projection(CENTER_COORD));
    // // projection.fitSize([960,500],
    // //     // {
    // //     // type: "FeatureCollection",
    // //     // features: [
    // //     //     {
    // //     //         type: "MultiPoint",
    // //     //         coordinates: bounds,
    // //     //     }
    // //     // ],
    // //     // }
    // // )
    // projection.center(CENTER_COORD);
    // console.log(projection(CENTER_COORD));
    maybe_main();
}
function add_injury_labels(types_of_injury, svg) {
    const xAxisHeight = 20; // Adjust this according to your visualization
    const zero = global.lazy.type_of_injury_scale(0);
    const one = global.lazy.type_of_injury_scale(1);
    const width = one - zero;
    function height(d) {
        return xAxisHeight;
    }
    svg.selectAll('.injury-label')
        .data(types_of_injury)
        .enter()
        .append('text')
        .attr('class', 'injury-label')
        .attr('width', width - 20)
        .attr('height', 200)
        .attr('x', d => global.lazy.type_of_injury_scale(global.lazy.type_of_injury_index(d)) + 5) // Adjust text positioning
        .attr('y', height) // Adjust vertical positioning
        .text(d => d)
        .style('fill', 'white') // Adjust text color
        .style('font-size', '6px')
        .each(function () {
        const x = d3.select(this).attr('x'); // Access x attribute
        const y = d3.select(this).attr('y'); // Access y attribute
        d3.select(this).attr('transform', `rotate(-30 ${x} ${y})`); // Apply rotation
    });
}
function maybe_main() {
    if (global.lazy.fatalities && global.lazy.districts) {
        main();
    }
}
function main() {
    var _a, _b;
    const lists_of_districts = data_to_lists_of_districts(global.lazy.fatalities);
    const projection = d3.geoMercator()
        .center(global.mercator.center)
        .scale(980 * 8)
        .translate([width / 2, height / 2 + height / 4]);
    const mercator_grid = [];
    const lng_span = global.mercator.extent_lng[1] - global.mercator.extent_lng[0];
    const lng_stride = lng_span / 10;
    const lat_span = global.mercator.extent_lat[1] - global.mercator.extent_lat[0];
    const lat_stride = lat_span / 10;
    for (let i = global.mercator.extent_lng[0]; i < global.mercator.extent_lng[1]; i += lng_stride) {
        for (let j = global.mercator.extent_lat[0]; j < global.mercator.extent_lat[1]; j += lat_stride) {
            const p = projection([i, j]);
            mercator_grid.push({ x: p[0], y: p[1] });
        }
    }
    console.log(mercator_grid);
    svg.selectAll(".mercator-grid")
        .data(mercator_grid)
        .enter()
        .append("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", 1)
        .style("fill", "gray");
    svg.append("circle")
        .attr("cx", d => projection(global.mercator.center)[0])
        .attr("cy", d => projection(global.mercator.center)[1])
        .attr("r", 1);
    const histogram_center = 300;
    const histogram_height = 100;
    const histogram_width = width - margin.left - margin.right;
    global.lazy.type_of_injury_scale = d3.scaleLinear()
        .domain([0, 12])
        .range([0, histogram_width]);
    add_injury_labels(Array.from(global.lazy.type_of_injury_unique), svg);
    const scatterPlotArea = {
        width: histogram_width,
        height: 200,
        x: 50,
        y: 50,
    };
    const age_range = d3.extent(global.lazy.fatalities, d => d.age);
    const age_scale = d3.scaleLinear()
        .domain(age_range)
        .range([scatterPlotArea.height + scatterPlotArea.y, scatterPlotArea.y]);
    const yAxis = d3.axisLeft(age_scale);
    function calculateMeanAge(data) {
        const totalAges = data.reduce((sum, fatality) => sum + fatality.age, 0);
        const meanAge = totalAges / data.length;
        return meanAge;
    }
    // Assuming 'data' is the array of Fatality objects
    const meanAge = calculateMeanAge(global.lazy.fatalities);
    console.log('Mean Age:', meanAge);
    function addToScatterPlot(dataItem) {
        let offset = 0;
        let noise = 0;
        if (dataItem.event_location_region == "Gaza Strip") {
            noise = Math.random() / (1.0 / 0.4);
            offset = 0;
        }
        else if (dataItem.event_location_region == "West Bank") {
            noise = Math.random() / (1.0 / 0.4);
            offset = 0.4;
        }
        else if (dataItem.event_location_region == "Israel") {
            offset = 0.8;
            noise = Math.random() / (1.0 / 0.2);
        }
        const xPosition = global.lazy.type_of_injury_scale(global.lazy.type_of_injury_index(dataItem.type_of_injury) + noise + offset);
        svg.append("circle")
            .attr("class", "fatality")
            .attr("r", 3)
            .data([dataItem])
            .attr("cx", xPosition)
            .attr("cy", d => age_scale(d.age_with_noise))
            .style("fill", d => {
            if (d.citizenship === "Israeli")
                return ISRAELI_BLUE;
            if (d.citizenship === "Palestinian")
                return PALESTINIAN_RED;
            return 'white'; // Jordanian or American
        })
            .on("mouseover", function (event, d) {
            d3.select(this).attr("color", "green");
            const opacity = fatality_to_opacity(d);
            if (opacity < 0.00001)
                return;
            tooltip.transition()
                .duration(10)
                .style("opacity", 0.9);
            tooltip.html(`<strong>Name:</strong> ${d.name}<br>
                                <strong>Region:</strong> ${d.event_location_region}<br>
                                <strong>Age:</strong> ${d.age}<br>
                                <strong>Citizenship:</strong> ${d.citizenship}<br>
                                <strong>Date of Death:</strong> ${d.date_of_death}<br>
                                <strong>Notes:</strong> ${d.notes}`);
        })
            .on("mouseout", function (event, d) {
            tooltip.transition()
                .duration(10)
                .style("opacity", 0);
        });
    }
    const israeli_deaths = global.lazy.fatalities.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = global.lazy.fatalities.filter(d => d.citizenship === "Palestinian");
    // console.log(global.lazy.districts);
    const district_rects = svg.selectAll(".geo-bounds")
        .data(global.lazy.districts)
        .enter()
        .append("rect")
        .on("mouseover", function (event, d) {
        d3.select(this).classed("hover", true);
    })
        .on("mouseout", function (event, d) {
        d3.select(this).classed("hover", false);
    })
        .attr("class", "geo-bounds")
        .attr("x", d => {
        const northeast = d.geocode_result[0].geometry.viewport.northeast;
        const southwest = d.geocode_result[0].geometry.viewport.southwest;
        d.northeast_x_y = projection([northeast.lng, northeast.lat]);
        d.southwest_x_y = projection([southwest.lng, southwest.lat]);
        d.x = d.southwest_x_y[0];
        d.y = d.northeast_x_y[1];
        d.width = d.northeast_x_y[0] - d.southwest_x_y[0];
        d.height = d.southwest_x_y[1] - d.northeast_x_y[1];
        return d.x;
    })
        .attr("y", d => d.y)
        .attr("width", d => d.width)
        .attr("height", d => d.height)
        .style("fill", "blue")
        .style("opacity", 0.2);
    const tooltip = svg.append("foreignObject")
        .attr("class", "tooltip")
        .attr("width", 400)
        .attr("height", 300)
        .attr("x", 0)
        .attr("y", 0)
        .style("text-align", "left")
        .style("color", "white")
        .append("xhtml:div")
        .style("opacity", 0)
        .attr("class", "tooltip-content");
    svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis);
    svg.selectAll(".y-axis path")
        .style("stroke", "white");
    svg.selectAll(".y-axis text")
        .style("fill", "white");
    svg.selectAll(".y-axis line")
        .style("stroke", "white");
    function onPauseClicked() {
        global.scrubber.paused = !global.scrubber.paused;
    }
    const pauseButton = svg.append('g')
        .attr('class', 'pause-button')
        .attr('cursor', 'pointer')
        .on('click', onPauseClicked);
    pauseButton.append('rect')
        .attr('x', 10)
        .attr('y', 10)
        .attr('width', 30)
        .attr('height', 30)
        .attr('fill', 'red');
    pauseButton.append('text')
        .attr('x', 25)
        .attr('y', 30)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .text('Pause');
    // global.lazy.fatalities.forEach(addToScatterPlot)
    const dateRange = d3.extent(global.lazy.fatalities, d => d.parsed_date);
    const time_zero = dateRange[0].getTime();
    const totalMilliseconds = dateRange[1].getTime() - time_zero;
    const daysPerSecond = 365 / 2;
    const days_data_per_ms_real = daysPerSecond / 1000;
    const ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
    const framesPerSecond = 12;
    const frames_per_ms = 1000 / framesPerSecond;
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);
    global.scrubber.width = real_ms_to_width(global.scrubber.width_real_ms);
    const scrubber = svg.append('rect')
        .attr('x', 0)
        .attr('y', histogram_center)
        .attr('width', global.scrubber.width)
        .attr('height', global.scrubber.height)
        .attr('opacity', 0.3)
        .attr('stroke', 'white')
        .call(d3.drag() // Apply drag behavior
        .on('start', dragStarted)
        .on('drag', dragging)
        .on('end', dragEnded));
    function refresh_scatter() {
        console.log("refreshing scatter");
        svg.selectAll(".fatality").remove();
        const to_add = find_in_interval(current_interval);
        console.log(current_interval.as_dates(), dateRange, to_add);
        to_add.forEach(addToScatterPlot);
        // global.lazy.fatalities.forEach(d=>{
        //     console.log(current_interval);
        //     if(current_interval.has(d.parsed_date_ms_with_noise)) {
        //         console.count("adding to scatter")
        //         addToScatterPlot(d);
        //     }
        // })
    }
    // scrubber.on("mouseover",function(){
    //     global.scrubber.paused = true;
    // });
    // scrubber.on("mouseout",function(){
    //     global.scrubber.paused = false;
    // })
    // Functions to handle drag events
    function dragStarted(event, d) {
        global.scrubber.click_diff = event.x - Number(scrubber.attr('x'));
        // Handle the start of the drag event
        global.scrubber.dragging = true;
    }
    let padding_time_data_ms = real_ms_to_data_ms(global.scrubber.width_real_ms);
    let scrub_x = d3.scaleTime()
        .domain([time_zero - padding_time_data_ms, dateRange[1].getTime()])
        .range([-global.scrubber.width, histogram_width])
        .clamp(false);
    let max_real_ms = data_ms_to_real_ms(((_a = dateRange[1]) === null || _a === void 0 ? void 0 : _a.getTime()) - ((_b = dateRange[0]) === null || _b === void 0 ? void 0 : _b.getTime()));
    const scrub_x_real_ms = d3.scaleLinear()
        .domain([0, histogram_width])
        .range([0, max_real_ms])
        .clamp(false);
    // d3.interval(function(){
    //     console.log(svg.selectAll(".fatality").size());
    // },1000)
    function calc_intervals_from_elapsed_real_ms() {
        looped_epoch_time = positiveModulo(elapsed_real_ms_virtual * ms_data_per_ms_real, totalWidthMilliseconds);
        last_time_left_ms = current_time_left_ms;
        last_time_right_ms = current_time_right_ms;
        last_interval.start = last_time_left_ms;
        last_interval.end = last_time_right_ms;
        current_time_right_ms = time_zero + looped_epoch_time;
        current_time_left_ms = current_time_right_ms - padding_time_data_ms;
        current_interval.start = current_time_left_ms;
        current_interval.end = current_time_right_ms;
        interval_to_add = current_interval.subtract_same_length(last_interval);
        interval_to_remove = last_interval.subtract_same_length(current_interval);
    }
    function histogram_tick(elapsed) {
        elapsed_real_ms_diff = elapsed - elapsed_real_ms_last;
        if (!global.scrubber.paused && !global.scrubber.dragging) {
            elapsed_real_ms_virtual += elapsed_real_ms_diff;
        }
        calc_intervals_from_elapsed_real_ms();
        const items_to_add = find_in_interval(interval_to_add);
        items_to_add.forEach(addToScatterPlot);
        const x_val = scrub_x(current_time_left_ms);
        const real_x = d3.max([0, x_val]) || 0;
        const subtraction_left = d3.min([x_val, 0]) || 0;
        const width = d3.min([global.scrubber.width, histogram_width - real_x]) + subtraction_left;
        scrubber
            .attr('x', real_x)
            .attr('width', Math.abs(width));
        update_scatter();
        elapsed_real_ms_last = elapsed;
    }
    function scrub_x_to_elapsed_real_ms(scrubber_x) {
        let elapsed_real_ms = scrub_x_real_ms(scrubber_x);
        if (elapsed_real_ms < 0) {
            elapsed_real_ms = max_real_ms + global.scrubber.width_real_ms + elapsed_real_ms;
        }
        return elapsed_real_ms;
    }
    global.scrubber.set_width = function (width) {
        var _a;
        const scrub_data_ms_from_x = d3.scaleTime()
            .domain([0, histogram_width])
            .range([time_zero, (_a = dateRange[1]) === null || _a === void 0 ? void 0 : _a.getTime()])
            .clamp(false);
        const width_data_ms = scrub_data_ms_from_x(width) - scrub_data_ms_from_x(0);
        const width_real_ms = data_ms_to_real_ms(width_data_ms);
        console.log('widths', width, width_data_ms, width_real_ms, data_ms_to_width(width_data_ms));
        const x_right = +scrubber.attr('x') + +scrubber.attr('width');
        const new_x_left = x_right - width;
        global.scrubber.width = width;
        global.scrubber.width_real_ms = width_real_ms;
        padding_time_data_ms = real_ms_to_data_ms(global.scrubber.width_real_ms);
        opacity_scale = d3.scaleLinear()
            .domain([real_ms_to_data_ms(global.scrubber.width_real_ms), 0])
            .range([0, 1]);
        scrub_x = d3.scaleTime()
            .domain([time_zero - padding_time_data_ms, dateRange[1].getTime()])
            .range([-global.scrubber.width, histogram_width])
            .clamp(false);
        scrubber.attr("width", global.scrubber.width);
        scrubber.attr("x", new_x_left);
        totalWidthMilliseconds = totalMilliseconds + padding_time_data_ms;
        elapsed_real_ms_virtual = 0; // scrub_x_to_elapsed_real_ms(x_right);
        elapsed_real_ms_last = 0;
        console.log('calculating intervals');
        calc_intervals_from_elapsed_real_ms();
        refresh_scatter();
        last_interval.start = -1;
        last_interval.end = -1;
    };
    function dragging(event, d) {
        const newX = event.x + global.scrubber.click_diff;
        elapsed_real_ms_virtual = scrub_x_to_elapsed_real_ms(newX);
        elapsed_real_ms_last = 0;
        if (global.debug) {
            // Add a circle at the dragged position
            svg.append("circle")
                .attr("cx", newX)
                .attr("cy", 50) // Adjust the y-position as needed
                .attr("r", 8)
                .attr("fill", "red")
                .transition()
                .duration(1000) // Disappear over 1 second
                .style("opacity", 0)
                .remove();
        }
    }
    function dragEnded() {
        global.scrubber.dragging = false;
    }
    let totalWidthMilliseconds = totalMilliseconds + padding_time_data_ms;
    function width_to_ms_data(widthInPixels) {
        const oneDayPixelValue = scrub_x(new Date(time_zero + days_to_ms(1)));
        const days = widthInPixels / oneDayPixelValue;
        return days * (1000 / days_data_per_ms_real);
    }
    function width_to_real_ms(widthInPixels) {
        const data_ms = width_to_ms_data(widthInPixels);
        return data_ms_to_real_ms(data_ms);
    }
    if (global.test) {
        // Define a test real milliseconds value
        const testRealMilliseconds = 5000;
        // Convert real milliseconds to width in pixels
        const widthPixels = real_ms_to_width(testRealMilliseconds);
        // Convert width in pixels back to real milliseconds
        const convertedRealMilliseconds = width_to_real_ms(widthPixels);
        console.log("Original Real Milliseconds:", testRealMilliseconds);
        console.log("Converted Real Milliseconds:", convertedRealMilliseconds);
        // Check if the conversions are close or equal (within a tolerance)
        if (Math.abs(testRealMilliseconds - convertedRealMilliseconds) < 0.0001) {
            console.log("Conversion test passed!");
        }
        else {
            console.error("Conversion test failed!");
        }
    }
    function data_ms_to_width(data_ms) {
        const scale = d3.scaleLinear()
            .domain([time_zero, dateRange[1].getTime()])
            .range([0, histogram_width]);
        const one_day_in_pixels = scale(new Date(time_zero + days_to_ms(1)));
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
    if (global.test) {
        const real_ms = 1000;
        const data_ms = real_ms_to_data_ms(real_ms);
        const out = data_ms_to_real_ms(data_ms);
        if (real_ms !== out) {
            throw new Error("inverse ms broken ${in} ${out}");
        }
    }
    let opacity_scale = d3.scaleLinear()
        .domain([real_ms_to_data_ms(global.scrubber.width_real_ms), 0])
        .range([0, 1]);
    let elapsed_real_ms_last = 0;
    let elapsed_real_ms_virtual = 0;
    let elapsed_real_ms_diff = 0;
    let looped_epoch_time = (elapsed_real_ms_virtual * ms_data_per_ms_real) % totalWidthMilliseconds;
    let current_time_right_ms = time_zero + looped_epoch_time;
    let last_time_right_ms = current_time_right_ms;
    let current_time_left_ms = current_time_right_ms - padding_time_data_ms;
    let current_interval = new Interval(current_time_left_ms, current_time_right_ms);
    let last_interval = current_interval.clone();
    let last_time_left_ms = current_time_left_ms;
    let interval_to_add = current_interval.subtract_same_length(last_interval);
    let interval_to_remove = last_interval.subtract_same_length(current_interval);
    const dateText = svg.append("text")
        .attr("class", "date-text")
        .attr("text-anchor", "start")
        .attr("fill", "white");
    const dateFormat = d3.timeFormat("%Y %b %d");
    function fatality_to_opacity(d) {
        const diff = current_time_right_ms - d.parsed_date_ms_with_noise;
        if (diff < 0)
            return 0;
        return opacity_scale(diff);
    }
    function update_scatter() {
        svg.selectAll(".fatality")
            .each(function (d) {
            if (interval_to_remove.has(d.parsed_date_ms_with_noise)) {
                this.remove();
            }
        })
            .style("opacity", fatality_to_opacity);
        const text = dateFormat(new Date(current_time_right_ms));
        const x = Number(scrubber.attr("x")) + Number(scrubber.attr("width")) - 20;
        const y = Number(scrubber.attr("y")) + 30;
        dateText.text(text)
            .attr("x", x)
            .attr("y", y);
    }
    function positiveModulo(dividend, divisor) {
        return ((dividend % divisor) + divisor) % divisor;
    }
    d3.interval(histogram_tick, frames_per_ms);
    const thresholds = create_thresholds(dateRange[0], dateRange[1], 1);
    const histogram = d3.bin()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(thresholds);
    function index_it(bin, index) { bin.index = index; }
    const israeli_bins = histogram(israeli_deaths);
    israeli_bins.forEach(index_it);
    const palestinian_bins = histogram(palestinian_deaths);
    palestinian_bins.forEach(index_it);
    const rect_height = d3.scaleLinear()
        .range([histogram_height, 0])
        // use the max of both israeli and palestinian deaths so both are on the same scale
        .domain([d3.max(histogram(global.lazy.fatalities), d => d.length), 0]);
    function bin_width(d) {
        return Math.max(0, x(d.x1) - x(d.x0));
    }
    svg.selectAll(".israeli-bin")
        .data(israeli_bins)
        .enter()
        .append("rect")
        .attr("class", "israeli-bin")
        .attr("x", d => x(d.x0))
        .attr("y", d => histogram_center + global.scrubber.height)
        .attr("width", d => bin_width(d))
        .attr("height", d => rect_height(d.length))
        .style("fill", ISRAELI_BLUE)
        .each(function (d) { d.element = this; });
    svg.selectAll(".palestinian-bin")
        .data(palestinian_bins)
        .enter()
        .append("rect")
        .attr("class", "palestinian-bin")
        .attr("index", d => d.index)
        .attr("x", d => x(d.x0))
        .attr("y", d => histogram_center - rect_height(d.length))
        .attr("width", d => bin_width(d))
        .attr("height", d => rect_height(d.length))
        .style("fill", PALESTINIAN_RED)
        .each(function (d) { d.element = this; });
    let hovered_palestinian_bin = undefined;
    let hovered_israeli_bin = undefined;
    // optimization to find highlighted bin faster
    const px_to_bin = new Array(Math.ceil(histogram_width));
    for (let bin_idx = 0; bin_idx < israeli_bins.length; bin_idx++) {
        const bin_i = israeli_bins[bin_idx];
        const bin_p = palestinian_bins[bin_idx];
        const low = x(bin_i.x0);
        const high = x(bin_i.x1);
        let px = Math.ceil(low);
        while (px <= high) {
            console.count('px_assign_2');
            px_to_bin[px] = [bin_i, bin_p];
            px++;
        }
    }
    const svg_group_node = svg.node();
    svg_root.on("mousemove", function (event, data) {
        const mouse_x = d3.pointer(event, svg_group_node)[0];
        const bins = px_to_bin[Math.floor(mouse_x)];
        if (hovered_palestinian_bin) {
            hovered_palestinian_bin.style("fill", PALESTINIAN_RED);
        }
        if (hovered_israeli_bin) {
            hovered_israeli_bin.style("fill", ISRAELI_BLUE);
        }
        if (bins) {
            hovered_israeli_bin = d3.select(bins[0].element);
            hovered_israeli_bin.style("fill", ISRAELI_BLUE_HIGHLIGHT);
            hovered_palestinian_bin = d3.select(bins[1].element);
            hovered_palestinian_bin.style("fill", PALESTINIAN_RED_HIGHLIGHT);
        }
    });
    // remove highlight when mouseout of whole svg
    svg_root.on("mouseout", function (event) {
        if (hovered_palestinian_bin) {
            hovered_palestinian_bin.style("fill", PALESTINIAN_RED);
        }
        if (hovered_israeli_bin) {
            hovered_israeli_bin.style("fill", ISRAELI_BLUE);
        }
    });
}
fetch('/static/json/fatalities.json')
    .then(on_response)
    .then(on_fatalities);
fetch('/static/json/districts_geocode.json')
    .then(on_response)
    .then(on_districts);
export {};
//# sourceMappingURL=fatalities.js.map