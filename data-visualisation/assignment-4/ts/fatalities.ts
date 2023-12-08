const config = {
    scrubber: {
        height: 5,
        width: 300,
    }
}


interface Fatality {
    name: string;
    date_of_event: string;
    age: number;
    citizenship: string;
    event_location: string;
    event_location_district: string;
    event_location_region: string;
    date_of_death: string;
    gender: string;
    took_part_in_the_hostilities?: any;
    place_of_residence: string;
    place_of_residence_district: string;
    type_of_injury: string;
    ammunition: string;
    killed_by: string;
    notes: string;
    parsed_date: Date;
}

function on_response(response) {
    if(!response.ok) {
        throw new Error("failed to fetch data")
    }
    return response.json()
}

function assert_non_null<T>(item: T|null): T {
    if(item === null) {
        throw new Error("found null item");
    }
    return item as T;
}

function parse_date(str: string): Date {
    return assert_non_null(d3.timeParse("%Y-%m-%d")(str))
}

function create_thresholds(startDate: Date, endDate: Date, days: number) {
    const thresholds = [startDate];
    let currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        currentDate = new Date(currentDate.getTime() + days * 86400000); // Add 'days' days
        thresholds.push(currentDate);
    }
    return thresholds;
}

function days_to_ms(days: number): number{
    return days * days_to_ms.factor;
}
days_to_ms.factor = 24 * 60 * 60 * 1000;
function ms_to_days(ms: number): number {
    return ms / days_to_ms.factor
}

function on_data(data: [Fatality]){
    console.log(data)
    d3.select("#fatalities-1").selectAll("*").remove()
    const width = window.innerWidth;
    const height = window.innerHeight;
    const margin = {top: 300, right: 30, bottom: 30, left: 40};
    data.forEach(d => d.parsed_date = parse_date(d.date_of_death));
    data.sort((a, b) => a.parsed_date - b.parsed_date);
    const israeli_deaths = data.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = data.filter(d => d.citizenship === "Palestinian")


    const svg = d3.select('#fatalities-1')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

    const scrubber = svg.append('rect')
        .attr('x', 0)
        .attr('y', margin.top)
        .attr('width', config.scrubber.width)
        .attr('height', config.scrubber.height)
        .attr('opacity',0.3)
        .attr('stroke', 'white  ');

    const dateRange = d3.extent(data, d => d.parsed_date );
    const totalMilliseconds = dateRange[1].getTime() - dateRange[0].getTime()
    const totalDays = ms_to_days(totalMilliseconds);
    const histogram_width = width - margin.left - margin.right;
    const pixelsPerDay = histogram_width / totalDays;
    const daysPerSecond = 365 * 5;
    const daysPerMillisecond = daysPerSecond / 1000;
    const millisecondsPerMillisecond = days_to_ms(daysPerMillisecond);
    const animationDuration = (totalDays/daysPerMillisecond);
    const framesPerSecond = 60;
    const pixelsPerTick = pixelsPerDay * daysPerSecond / framesPerSecond;

    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);

    const padding_time = widthToMilliseconds(config.scrubber.width);
    const scrub_x = d3.scaleTime()
        .domain([dateRange[0].getTime() - padding_time,dateRange[1].getTime()])
        .range([-config.scrubber.width, histogram_width])
        .clamp(false);

    function widthToMilliseconds(widthInPixels: number) {
        const oneDayPixelValue = x(new Date(dateRange[0].getTime() + days_to_ms(1)));
        const days = widthInPixels / oneDayPixelValue;
        return days * (1000 / daysPerMillisecond);
    }

    d3.interval(elapsed=>{
        const totalWidthMilliseconds = (totalMilliseconds + padding_time)
        const looped_epoch_time = (elapsed * millisecondsPerMillisecond) % totalWidthMilliseconds;
        const currentDate = dateRange[0].getTime() - padding_time + looped_epoch_time;
        const x_val = scrub_x(currentDate);
        const real_x = d3.max([0,x_val]);
        const subtraction_left = d3.min([x_val,0]);
        const width = d3.min([config.scrubber.width,histogram_width-real_x]) + subtraction_left;
        console.log(new Date(currentDate),x_val, real_x, width, subtraction_left)
        scrubber
            .attr('x', real_x)
            .attr('width', width)
    },1000/framesPerSecond)

    const xAxis = svg.append("g")
        .attr("transform", `translate(0,${margin.top})`)

    const thresholds = create_thresholds(dateRange[0],dateRange[1], 14)
    const histogram = d3.bin()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(thresholds)

    const israeli_bins = histogram(israeli_deaths);
    const palestinian_bins = histogram(palestinian_deaths)

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
        .attr("y", d => margin.top + config.scrubber.height)
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
    .then(on_data)