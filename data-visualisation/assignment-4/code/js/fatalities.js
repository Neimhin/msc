import './d3.js';
import * as pure from "./pure.js";
import { DynamicPieChart } from "./DynamicPieChart.js";
import { Slider } from './Slider.js';
const global = {
    debug: true,
    test: true,
    scrubber: {
        dragging: false,
        paused: false,
        height: 10,
        width: 30,
        width_real_ms: 1959,
        click_diff: 0,
        set_width: (width) => { },
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
    regions: ["Gaza", "Israel", "West Bank"],
};
const ISRAELI_BLUE = "#0038b8";
const ISRAELI_BLUE_HIGHLIGHT = d3.interpolate(ISRAELI_BLUE, "white")(0.3);
const PALESTINIAN_RED = "#EE2A35";
const PALESTINIAN_RED_HIGHLIGHT = d3.interpolate(PALESTINIAN_RED, "white")(0.3);
d3.select("#vis").selectAll("*").remove();
const width = window.innerWidth * 0.9;
const height = 350 * 8;
const margin = { top: 30, right: 100, bottom: 20, left: 100 };
const svg_root = d3.select('#vis')
    .append('svg')
    .attr('width', width)
    .attr('height', height);
const svg = svg_root
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
function calculateMeanAge(data) {
    const totalAges = data.reduce((sum, fatality) => sum + fatality.age, 0);
    const meanAge = totalAges / data.length;
    return meanAge;
}
function on_fatalities(d) {
    global.lazy.fatalities = d;
    global.lazy.noon_time_to_fatalities = new Map();
    const mean_age = calculateMeanAge(global.lazy.fatalities);
    global.lazy.fatalities.sort((a, b) => a.parsed_date_ms - b.parsed_date_ms);
    // global.lazy.fatalities = global.lazy.fatalities.filter(d => d.event_location_region);
    console.log(global.lazy.fatalities.filter(d => !d.event_location_region).length);
    global.lazy.fatalities.forEach(d => {
        d.parsed_date = parse_date(d.date_of_death);
        d.parsed_date.setHours(12, 0, 0, 0);
        d.parsed_date_ms = d.parsed_date.getTime();
        d.parsed_date_ms_with_noise = d.parsed_date_ms + Math.random() * ONE_DAY_MS;
        if (d.age !== 0 && !d.age) {
            d.age = mean_age; // impute mean age
        }
        d.age_with_noise = d.age + Math.random();
        d.random = Math.random();
        const fatalities_list = global.lazy.noon_time_to_fatalities.get(d.parsed_date_ms);
        if (fatalities_list) {
            fatalities_list.push(d);
        }
        else {
            global.lazy.noon_time_to_fatalities.set(d.parsed_date_ms, [d]);
        }
        d.broad_injury = pure.injury_to_broad_injury(d.type_of_injury);
    });
    debug.noon_times(global.lazy.noon_time_to_fatalities);
    global.lazy.type_of_injury_unique = new Set(global.lazy.fatalities.map(d => d.type_of_injury).filter(d => d));
    console.log(Array.from(global.lazy.type_of_injury_unique));
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
class PauseButton {
    constructor(svg, x, y) {
        this.width = 30;
        this.height = 30;
        this.svg = svg;
        this.x = x;
        this.y = y;
        this.pauseButtonGroup = this.svg.append('g')
            .attr('class', 'pause-button')
            .attr('cursor', 'pointer')
            .attr('transform', `translate(${this.x} ${this.y})`)
            .on('click', () => this.onPauseClicked());
        this.createButton();
    }
    createButton() {
        this.pauseButtonGroup.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('fill', d3.interpolate('red', 'blue')(0.3));
        this.pauseButtonGroup.append('rect')
            .attr("class", "pause-vert")
            .attr('x', this.width / 6)
            .attr('y', this.height / 6)
            .attr('width', 5)
            .attr('height', 20)
            .attr('fill', 'white');
        this.pauseButtonGroup.append('rect')
            .attr("class", "pause-vert")
            .attr('x', this.width - (this.width / 3))
            .attr('y', this.height / 6)
            .attr('width', this.width / 6)
            .attr('height', 20)
            .attr('fill', 'white');
        const triangleSize = this.height * 1.5 / 3;
        const triangleLeft = (this.width - triangleSize) / 2;
        const triangleTop = this.height / 6;
        this.pauseButtonGroup.append('path')
            .attr("class", "pause-triangle")
            .attr('d', `M ${triangleLeft} ${triangleTop} L ${triangleLeft + triangleSize} ${this.height / 2} L ${triangleLeft} ${this.height - triangleTop} Z`)
            .style('opacity', 0)
            .attr('fill', 'white');
    }
    onPauseClicked() {
        global.scrubber.paused = !global.scrubber.paused;
        if (global.scrubber.paused) {
            d3.selectAll(".pause-vert")
                .style("opacity", 0);
            d3.selectAll(".pause-triangle")
                .style("opacity", 1);
        }
        else {
            d3.selectAll(".pause-vert")
                .style("opacity", 1);
            d3.selectAll(".pause-triangle")
                .style("opacity", 0);
        }
    }
}
class YAxis {
    constructor(svg, scale, label) {
        this.svg = svg;
        this.scale = scale;
        this.label = label;
        this.createAxis();
    }
    createAxis() {
        const yAxis = d3.axisLeft(this.scale);
        this.axisGroup = this.svg.append("g")
            .attr("class", "y-axis")
            .attr("transform", "translate(-10 0)")
            .call(yAxis);
        this.axisGroup.selectAll("path")
            .style("stroke", "white")
            .style("opacity", 0);
        this.axisGroup.selectAll("text")
            .style("fill", "white");
        this.axisGroup.selectAll("line")
            .style("stroke", "white");
        this.axisGroup.append("text")
            .attr("class", "axis-label")
            .attr("transform", "rotate(-90)")
            .attr("y", -35)
            .attr("x", -100)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .style("fill", "white")
            .text(this.label);
    }
    updateScale(newScale) {
        this.scale = newScale;
        const yAxis = d3.axisLeft(this.scale);
        this.axisGroup.call(yAxis);
    }
}
function main() {
    var _a, _b, _c;
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
    const histogram_center = 300;
    const histogram_height = 100;
    const histogram_width = width - margin.left - margin.right;
    const scatterPlotArea = {
        width: histogram_width * (2 / 3),
        height: 250,
        x: 50,
        y: 0,
    };
    const age_range = d3.extent(global.lazy.fatalities, d => d.age);
    if (!age_range[0] || !age_range[1]) {
        throw new Error("no age range");
    }
    const age_scale = d3.scaleLinear()
        .domain(age_range)
        .range([scatterPlotArea.height + scatterPlotArea.y, scatterPlotArea.y]);
    const israeli_deaths = global.lazy.fatalities.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = global.lazy.fatalities.filter(d => d.citizenship === "Palestinian");
    const dateRange = d3.extent(global.lazy.fatalities, d => d.parsed_date);
    if (!dateRange[0] || !dateRange[1]) {
        throw new Error("no date range");
    }
    const time_zero = dateRange[0].getTime();
    const totalMilliseconds = dateRange[1].getTime() - time_zero;
    const daysPerSecond = 31 * 6;
    const days_data_per_ms_real = daysPerSecond / 1000;
    const ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
    const framesPerSecond = 24;
    const frames_per_ms = 1000 / framesPerSecond;
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);
    global.padding_time_data_ms = real_ms_to_data_ms(global.scrubber.width_real_ms);
    global.totalWidthMilliseconds = totalMilliseconds + global.padding_time_data_ms;
    global.scrubber.width = real_ms_to_width(global.scrubber.width_real_ms);
    global.opacity_scale = d3.scaleLinear()
        .domain([real_ms_to_data_ms(global.scrubber.width_real_ms), 0])
        .range([0, 1]);
    global.scrub_x = d3.scaleTime()
        .domain([time_zero, dateRange[1].getTime()])
        .range([0, histogram_width])
        .clamp(false);
    // .domain([time_zero - global.padding_time_data_ms, dateRange[1].getTime()])
    // .range([-global.scrubber.width, histogram_width])
    // .clamp(false);
    global.max_real_ms = data_ms_to_real_ms(((_a = dateRange[1]) === null || _a === void 0 ? void 0 : _a.getTime()) - ((_b = dateRange[0]) === null || _b === void 0 ? void 0 : _b.getTime()));
    const scrub_x_real_ms = d3.scaleLinear()
        .domain([0, histogram_width])
        .range([0, global.max_real_ms])
        .clamp(false);
    const slider_width = scrub_x_real_ms(global.scrubber.width);
    const slider_height = 3;
    const slider_center = 360;
    const slider = new Slider(svg, slider_width, slider_height, slider_center, global.scrubber.width, (newWidth) => {
        global.scrubber.set_width(newWidth);
    });
    for (let i = global.mercator.extent_lng[0]; i < global.mercator.extent_lng[1]; i += lng_stride) {
        for (let j = global.mercator.extent_lat[0]; j < global.mercator.extent_lat[1]; j += lat_stride) {
            const p = projection([i, j]);
            mercator_grid.push({ x: p[0], y: p[1] });
        }
    }
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
    global.lazy.type_of_injury_scale = d3.scaleLinear()
        .domain([0, 12])
        .range([0, histogram_width]);
    // add_injury_labels(Array.from(global.lazy.type_of_injury_unique), svg);
    global.region_scale = d3.scaleLinear()
        .domain([0, 3])
        .range(0, histogram_width);
    const scatter_region_width = scatterPlotArea.width / 3; // Assuming 'width' is the total width of your SVG
    const gutter_width = 30;
    const gazaScale = d3.scaleLinear()
        .domain([0, 1])
        .range([0, scatter_region_width - gutter_width]);
    const israelScale = d3.scaleLinear()
        .domain([0, 1])
        .range([scatter_region_width, 2 * scatter_region_width - gutter_width]);
    const westBankScale = d3.scaleLinear()
        .domain([0, 1])
        .range([2 * scatter_region_width, 3 * scatter_region_width - gutter_width]);
    const regionNames = ["Gaza Strip", "West Bank", "Israel"];
    const regionScales = [gazaScale, westBankScale, israelScale];
    const highlightRects = [];
    regionNames.forEach((region, index) => {
        const scale = regionScales[index];
        const xPosition = scale(0.5);
        svg.append("text")
            .attr("x", xPosition)
            .attr("y", scatterPlotArea.y + scatterPlotArea.height + 20) // Position below the scatter plot
            .attr("text-anchor", "middle")
            .attr("fill", "white")
            .text(region);
        highlightRects[index] = svg_root.append("rect")
            .attr("transform", `translate(${margin.left} ${margin.top})`)
            .attr("x", scale(0))
            .attr("y", scatterPlotArea.y + scatterPlotArea.height + 3)
            .attr("width", scatter_region_width - gutter_width)
            .attr("height", 20)
            .style("fill", "white")
            .style("opacity", 0.1)
            .on("mouseover", function () {
            d3.select(this).style("opacity", 0.3);
        })
            .on("mouseout", function () {
            d3.select(this).style("opacity", 0.1);
        });
    });
    const tooltip = svg.append("foreignObject")
        .attr("class", "tooltip")
        .attr("width", scatterPlotArea.width)
        .attr("height", 300)
        .attr("x", 0)
        .attr("y", 0)
        .style("text-align", "left")
        .style("text-size", "10px")
        .style("color", "white")
        .style("z-index", '10')
        .append("xhtml:div")
        .style("opacity", 0)
        .attr("class", "toooltip-content");
    const scatter_legend_spacing = 9;
    const scatter_legend_group = svg.append('g')
        .attr("transform", `translate(0 ${histogram_center + 20})`);
    const scatter_legend_palestinian_group = scatter_legend_group.append('g');
    scatter_legend_palestinian_group.append("circle")
        .attr("class", "fatality-legend")
        .attr("r", 3)
        .style("fill", PALESTINIAN_RED);
    scatter_legend_palestinian_group.append("text")
        .attr("dominant-baseline", "middle")
        .style("font-size", '10px')
        .attr("x", 5)
        .style("fill", 'white')
        .text("Death of a Palestinian Citizen");
    const scatter_legend_israeli_group = scatter_legend_group
        .append('g')
        .attr("transform", `translate(0, ${scatter_legend_spacing})`);
    scatter_legend_israeli_group.append("circle")
        .attr("class", "fatality-legend")
        .attr("r", 3)
        .style("fill", ISRAELI_BLUE);
    scatter_legend_israeli_group.append("text")
        .attr("dominant-baseline", "middle")
        .style("font-size", '10px')
        .attr("x", 5)
        .style("fill", 'white')
        .text("Death of an Israeli Citizen");
    const scatter_legend_other_group = scatter_legend_group
        .append('g')
        .attr("transform", `translate(0, ${scatter_legend_spacing * 2})`);
    scatter_legend_other_group.append("circle")
        .attr("class", "fatality-legend")
        .attr("r", 3)
        .style("fill", 'white');
    scatter_legend_other_group.append("text")
        .attr("dominant-baseline", "middle")
        .style("font-size", '10px')
        .attr("x", 5)
        .style("fill", 'white')
        .text("Death of a Jordanian or American");
    function addToScatterPlot(d) {
        let xPosition;
        switch (d.event_location_region) {
            case "Gaza Strip":
                xPosition = gazaScale(d.random);
                break;
            case "West Bank":
                xPosition = westBankScale(d.random);
                break;
            case "Israel":
                xPosition = israelScale(d.random);
                break;
            default:
                throw new Error("none of Gaza, Israel, West Bank");
                xPosition = 0;
        }
        svg.append("circle")
            .attr("class", "fatality")
            .attr("r", 3)
            .data([d])
            .attr("cx", xPosition)
            .attr("cy", d => age_scale(d.age_with_noise))
            .style("opacity", fatality_to_opacity)
            .style("fill", d => {
            if (d.citizenship === "Israeli")
                return ISRAELI_BLUE;
            if (d.citizenship === "Palestinian")
                return PALESTINIAN_RED;
            return 'white'; // Jordanian or American
        })
            .on("mouseover", function (event, d) {
            const opacity = fatality_to_opacity(d);
            if (opacity < 0.00001)
                return;
            tooltip.transition()
                .duration(300)
                .style("opacity", 0.9);
            tooltip.html(`<strong>Name:</strong> ${d.name}<br>
                                <strong>Region:</strong> ${d.event_location_region}<br>
                                <strong>Age:</strong> ${d.age}<br>
                                <strong>Citizenship:</strong> ${d.citizenship}<br>
                                <strong>Date of Death:</strong> ${dateFormat(d.parsed_date_ms)}<br>
                                <strong>Notes:</strong> ${d.notes}`);
        })
            .on("mouseout", function (event, d) {
            d;
        });
    }
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
    const yAxis = new YAxis(svg, age_scale, "Age upon Death");
    const pause_button = new PauseButton(svg, histogram_width - 30, slider_center - 20);
    const pie_chart_diameters = 70;
    const pie_chart_x = scatterPlotArea.x + scatterPlotArea.width + margin.left + 10;
    const pies_start_y = 70;
    const mannerOfDeathColors = d3.scaleOrdinal()
        .domain(["gunfire", "assault", "explosive", "fire/demolition"])
        .range(["#355070", "#B56576", "#48B8D0", "#D16014"]); // Darker, richer tones
    const demographicColors = d3.scaleOrdinal()
        .domain(["palestinian man", "palestinian woman", "palestinian minor", "israeli man", "israeli woman", "israeli minor"])
        .range(["#6C8CA1", "#035E7B", "#21A179", "#D1A368", "#C8758F", "#E59500"]); // More saturated colors
    // Perpetrator Color Palette
    const perpetratorColors = d3.scaleOrdinal()
        .domain(["israeli civilians", "palestinian civilians", "israeli security forces"])
        .range(["#F5F749", "#F24236", "#2E86AB"]); // Enhanced contrast colors
    const injury_pie_chart = new DynamicPieChart(svg_root, pie_chart_diameters, pie_chart_x, pies_start_y + 0 * (pie_chart_diameters + 30), false)
        .title("Manner of death")
        .color(mannerOfDeathColors);
    const gender_age_pie_chart = new DynamicPieChart(svg_root, pie_chart_diameters, pie_chart_x, pies_start_y + 1 * (pie_chart_diameters + 30), false)
        .title("Demographic of Victim")
        .color(demographicColors);
    const perpetrator_pie_chart = new DynamicPieChart(svg_root, pie_chart_diameters, pie_chart_x, pies_start_y + 2 * (pie_chart_diameters + 30), false)
        .title("Perpetrator")
        .color(perpetratorColors);
    const scrubber_group = svg.append('g');
    const scrubber = scrubber_group.append('rect')
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
    const lineLength = -10; // Length of the lines
    const scrubberY = histogram_center; // Y-coordinate for the scrubber lines
    const scrubber_line_start = scrubber_group.append('line')
        .attr('class', 'scrubber-start-line')
        .attr('x1', 0)
        .attr('y1', scrubberY)
        .attr('x2', 0)
        .attr('y2', scrubberY + lineLength - 10)
        .attr('stroke', 'white')
        .attr('stroke-width', 0.3);
    const scrubber_line_start_hor = scrubber_group.append('line')
        .attr('class', 'scrubber-end-start-hor')
        .attr('x1', 0)
        .attr('y1', scrubberY + lineLength - 10)
        .attr('x2', histogram_width + 5)
        .attr('y2', scrubberY + lineLength - 10)
        .attr('stroke', 'white')
        .attr('stroke-width', 0.3);
    const scrubber_line_end = scrubber_group.append('line')
        .attr('class', 'scrubber-end-line')
        .attr('x1', global.scrubber.width)
        .attr('y1', scrubberY)
        .attr('x2', global.scrubber.width)
        .attr('y2', scrubberY + lineLength)
        .attr('stroke', 'white')
        .attr('stroke-width', 0.3);
    const scrubber_line_end_hor = scrubber_group.append('line')
        .attr('class', 'scrubber-end-line-hor')
        .attr('x1', global.scrubber.width)
        .attr('y1', scrubberY + lineLength)
        .attr('x2', histogram_width + 5)
        .attr('y2', scrubberY + lineLength)
        .attr('stroke', 'white')
        .attr('stroke-width', 0.3);
    const scrubber_start_text = scrubber_group.append("text")
        .attr('x', histogram_width + 5)
        .attr('y', scrubberY - 20)
        .attr('dominant-baseline', 'middle')
        .style('fill', 'white')
        .style('font-size', '10px')
        .text('hello');
    const scrubber_end_text = scrubber_group.append("text")
        .attr('x', histogram_width + 5)
        .attr('y', scrubberY - 10)
        .attr('dominant-baseline', 'middle')
        .style('fill', 'white')
        .style('font-size', '10px')
        .text('hello');
    function update_scrubber_lines() {
        const x_start = +scrubber.attr('x');
        scrubber_line_start
            .attr('x1', x_start)
            .attr('x2', x_start);
        const x_end = x_start + +scrubber.attr('width');
        scrubber_line_end
            .attr('x1', x_end)
            .attr('x2', x_end);
        scrubber_line_end_hor
            .attr('x1', x_end);
        scrubber_line_start_hor
            .attr('x1', x_start);
        scrubber_start_text.text(dateFormat(scrub_data_ms_from_x(x_start)));
        scrubber_end_text.text(dateFormat(scrub_data_ms_from_x(x_end)));
    }
    global.scrubber.set_width(global.scrubber.width);
    //slider.on_drag(global.scrubber.width);
    function refresh_scatter() {
        console.log("refreshing scatter");
        svg.selectAll(".fatality").remove();
        const to_add = find_in_interval(current_interval);
        console.log(current_interval.as_dates(), dateRange, to_add);
        to_add.forEach(addToScatterPlot);
    }
    function dragStarted(event, d) {
        global.scrubber.click_diff = event.x - Number(scrubber.attr('x'));
        // Handle the start of the drag event
        global.scrubber.dragging = true;
    }
    function calc_intervals_from_elapsed_real_ms() {
        global.looped_epoch_time = positiveModulo(global.elapsed_real_ms_virtual * ms_data_per_ms_real, global.totalWidthMilliseconds);
        last_time_left_ms = current_time_left_ms;
        last_time_right_ms = global.current_time_right_ms;
        last_interval.start = last_time_left_ms;
        last_interval.end = last_time_right_ms;
        global.current_time_right_ms = time_zero + global.looped_epoch_time;
        current_time_left_ms = global.current_time_right_ms - global.padding_time_data_ms;
        current_interval.start = current_time_left_ms;
        current_interval.end = global.current_time_right_ms;
        interval_to_add = current_interval.subtract_same_length(last_interval);
        interval_to_remove = last_interval.subtract_same_length(current_interval);
    }
    function histogram_tick(elapsed) {
        global.elapsed_real_ms_diff = elapsed - global.elapsed_real_ms_last;
        if (!global.scrubber.paused && !global.scrubber.dragging) {
            global.elapsed_real_ms_virtual += global.elapsed_real_ms_diff;
        }
        calc_intervals_from_elapsed_real_ms();
        const items_to_add = find_in_interval(interval_to_add);
        items_to_add.forEach(addToScatterPlot);
        const x_val = global.scrub_x(current_time_left_ms);
        const real_x = d3.max([0, x_val]) || 0;
        const subtraction_left = d3.min([x_val, 0]) || 0;
        const width = d3.min([global.scrubber.width, histogram_width - real_x]) + subtraction_left;
        scrubber
            .attr('x', real_x)
            .attr('width', Math.abs(width));
        update_scatter();
        update_scrubber_lines();
        global.elapsed_real_ms_last = elapsed;
        // highlight relevant histogram bars
        const x0 = real_x;
        const x1 = real_x + Math.abs(width);
        const data_for_pie = [];
        d3.selectAll(".palestinian-bin")
            .each(function (palestine_bin) {
            const israel_bin = israeli_bins[palestine_bin.index];
            const el = d3.select(this);
            if (x(palestine_bin.x1) > x0 && x(palestine_bin.x0) < x1) {
                el.style("fill", PALESTINIAN_RED_HIGHLIGHT);
                d3.select(israel_bin.element)
                    .style("fill", ISRAELI_BLUE_HIGHLIGHT);
                data_for_pie.push(palestine_bin);
                data_for_pie.push(israel_bin);
            }
            else {
                el.style("fill", PALESTINIAN_RED);
                d3.select(israeli_bins[palestine_bin.index].element)
                    .style("fill", ISRAELI_BLUE);
            }
        });
        const injuries = pure.flatten_and_count_injuries(data_for_pie);
        if (Math.random() < 0.1) {
            console.log(injuries);
        }
        injury_pie_chart.updateData(injuries);
        const gender_age = pure.flatten_and_count_man_woman_child(data_for_pie);
        gender_age_pie_chart.updateData(gender_age);
        const perpetrators = pure.flatten_and_perpetrator(data_for_pie);
        perpetrator_pie_chart.updateData(perpetrators);
    }
    function scrub_x_to_elapsed_real_ms(scrubber_x) {
        let elapsed_real_ms = scrub_x_real_ms(scrubber_x);
        if (elapsed_real_ms < 0) {
            elapsed_real_ms = global.max_real_ms + global.scrubber.width_real_ms + elapsed_real_ms;
        }
        return elapsed_real_ms;
    }
    const scrub_data_ms_from_x = d3.scaleTime()
        .domain([0, histogram_width])
        .range([time_zero, (_c = dateRange[1]) === null || _c === void 0 ? void 0 : _c.getTime()])
        .clamp(false);
    slider.text_formatter(function (width) {
        const width_data_ms = scrub_data_ms_from_x(width) - scrub_data_ms_from_x(0);
        return `Memory: ${ms_to_days(width_data_ms).toFixed(1)} days`;
    });
    global.scrubber.set_width = function (width) {
        const width_data_ms = scrub_data_ms_from_x(width) - scrub_data_ms_from_x(0);
        const width_real_ms = data_ms_to_real_ms(width_data_ms);
        const x_right = +scrubber.attr('x') + +scrubber.attr('width');
        const new_x_left = x_right - width;
        const new_data_ms_left = scrub_data_ms_from_x(new_x_left);
        global.elapsed_ms_real_virtual = new_data_ms_left;
        global.scrubber.width = width;
        global.scrubber.width_data_ms = width_data_ms;
        global.scrubber.width_real_ms = width_real_ms;
        global.padding_time_data_ms = real_ms_to_data_ms(global.scrubber.width_real_ms);
        global.opacity_scale = d3.scaleLinear()
            .domain([real_ms_to_data_ms(global.scrubber.width_real_ms), 0])
            .range([0, 1]);
        global.totalWidthMilliseconds = totalMilliseconds + global.padding_time_data_ms;
        calc_intervals_from_elapsed_real_ms();
        refresh_scatter();
        last_interval.start = -1;
        last_interval.end = -1;
    };
    function dragging(event, d) {
        const newX = event.x + global.scrubber.width - global.scrubber.click_diff;
        global.elapsed_real_ms_virtual = scrub_x_to_elapsed_real_ms(newX);
        global.elapsed_real_ms_last = 0;
        if (global.debug) {
            svg.append("circle")
                .attr("cx", newX)
                .attr("cy", 50)
                .attr("r", 8)
                .attr("fill", "red")
                .transition()
                .duration(1000)
                .style("opacity", 0)
                .remove();
        }
    }
    function dragEnded() {
        global.scrubber.dragging = false;
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
    global.elapsed_real_ms_last = 0;
    global.elapsed_real_ms_virtual = global.scrubber.width_real_ms;
    global.elapsed_real_ms_diff = 0;
    global.looped_epoch_time = (global.elapsed_real_ms_virtual * ms_data_per_ms_real) % global.totalWidthMilliseconds;
    global.current_time_right_ms = time_zero + global.looped_epoch_time;
    let last_time_right_ms = global.current_time_right_ms;
    let current_time_left_ms = global.current_time_right_ms - global.padding_time_data_ms;
    let current_interval = new Interval(current_time_left_ms, global.current_time_right_ms);
    let last_interval = current_interval.clone();
    let last_time_left_ms = current_time_left_ms;
    console.log('real_ms', data_ms_to_real_ms(days_to_ms(365)));
    let interval_to_add = current_interval.subtract_same_length(last_interval);
    let interval_to_remove = last_interval.subtract_same_length(current_interval);
    const dateTextRect = svg.append('g');
    const dateText = dateTextRect.append("text")
        .attr("class", "date-text")
        .attr("text-anchor", "start")
        .attr("fill", "white")
        .style('font-size', "6px")
        .attr("transform", 'rotate(15)');
    const dateFormat = d3.timeFormat("%Y %b %d");
    function fatality_to_opacity(d) {
        const diff = global.current_time_right_ms - d.parsed_date_ms_with_noise;
        if (diff < 0)
            return 0;
        return global.opacity_scale(diff);
    }
    function update_scatter() {
        svg.selectAll(".fatality")
            .each(function (d) {
            if (interval_to_remove.has(d.parsed_date_ms_with_noise)) {
                this.remove();
            }
        })
            .style("opacity", fatality_to_opacity);
    }
    function positiveModulo(dividend, divisor) {
        return ((dividend % divisor) + divisor) % divisor;
    }
    d3.interval(histogram_tick, frames_per_ms);
    const thresholds = create_thresholds(dateRange[0], dateRange[1], 21);
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
    // let hovered_palestinian_bin = undefined;
    // let hovered_israeli_bin = undefined;
    // // optimization to find highlighted bin faster
    // const px_to_bin = new Array(Math.ceil(histogram_width));
    // for(let bin_idx = 0; bin_idx < israeli_bins.length; bin_idx++) {
    //     const bin_i = israeli_bins[bin_idx];
    //     const bin_p = palestinian_bins[bin_idx];
    //     const low = x(bin_i.x0);
    //     const high = x(bin_i.x1);
    //     let px = Math.ceil(low);
    //     px_to_bin[px] = [bin_i,bin_p];
    //     while(px <= high) {
    //         console.count('px_assign_2');
    //         px_to_bin[px] = [bin_i,bin_p];
    //         px++;
    //     }
    // }
    // const svg_group_node = svg.node();
    // svg_root.on("mousemove", function(event, data) {
    //     const mouse_x = d3.pointer(event,svg_group_node)[0];
    //     const bins = px_to_bin[Math.floor(mouse_x)];
    //     if(hovered_palestinian_bin) {
    //         hovered_palestinian_bin.style("fill", PALESTINIAN_RED);
    //     }
    //     if(hovered_israeli_bin) {
    //         hovered_israeli_bin.style("fill", ISRAELI_BLUE);
    //     }
    //     if(bins) {
    //         hovered_israeli_bin = d3.select(bins[0].element)
    //         hovered_israeli_bin.style("fill", ISRAELI_BLUE_HIGHLIGHT)
    //         hovered_palestinian_bin = d3.select(bins[1].element)
    //         hovered_palestinian_bin.style("fill", PALESTINIAN_RED_HIGHLIGHT)
    //     }
    // });
    // // remove highlight when mouseout of whole svg
    // svg_root.on("mouseout", function(event) {
    //     if(hovered_palestinian_bin) {
    //         hovered_palestinian_bin.style("fill", PALESTINIAN_RED);
    //     }
    //     if(hovered_israeli_bin) {
    //         hovered_israeli_bin.style("fill", ISRAELI_BLUE);
    //     }
    // })
}
fetch('/json/fatalities.json')
    .then(on_response)
    .then(on_fatalities);
fetch('/json/districts_geocode.json')
    .then(on_response)
    .then(on_districts);
//# sourceMappingURL=fatalities.js.map