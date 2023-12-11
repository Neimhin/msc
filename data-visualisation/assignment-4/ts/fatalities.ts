const config = {
    test: true,
    scrubber: {
        height: 5,
        width: 300,
        width_real_ms: 12000,
    }
}

const ISRAELI_BLUE = "#0038b8";
const PALESTINIAN_RED = "#EE2A35";

export interface Fatality {
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
    parsed_date_ms: number;
}

const ONE_DAY_MS = 24 * 60 * 60 * 1000;

class TimeInterval{
    start: number;
    end: number;
    start_noon: number;
    end_noon: number;
    elapsed_noons: number[];
    constructor(end: number, length: number) {
        this.start = end - length;
        this.end = end;
        if(this.start > this.end) throw Error("can't have start after end")
        this.start_noon = get_noon_epoch_time(this.start);
        this.end_noon = get_noon_epoch_time(this.end);
        if(this.end_noon > this.end) {
            this.end_noon = this.end_noon - ONE_DAY_MS;
        }
        this.elapsed_noons = [];
        if(this.start <= this.start_noon && this.end >= this.start_noon) {
            this.elapsed_noons.push(this.start_noon);
        }
        let current_noon = this.start_noon + ONE_DAY_MS;
        while(current_noon <= this.end_noon) {
            this.elapsed_noons.push(current_noon);
            current_noon = current_noon + ONE_DAY_MS;
        }
    }
}

function interval_to_data(data: Map<number,Fatality[]>, interval: TimeInterval): Fatality[] {
    let fatalities: Fatality[] = [];
    for(const noon of interval.elapsed_noons) {
        const new_noons = data.get(noon);
        if(new_noons instanceof Array) {
            fatalities.push(...new_noons);
        }
    }
    return fatalities;
}

function on_response(response: Response) {
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

function get_noon_epoch_time(milliseconds: number) {
    let date = new Date(milliseconds);
    date.setHours(12, 0, 0, 0);
    return date.getTime();
}

function yeet(error_msg:string) {
    throw new Error(error_msg);
}

const debug = {
    noon_times(noon_time_to_fatalities: Map<number, Fatality[]>) {
        for(const k of noon_time_to_fatalities.keys()) {
            console.log(new Date(k));
        }

    }
}

export function on_data(data: [Fatality]){
    d3.select("#vis").selectAll("*").remove()
    const width = window.innerWidth * 0.9;
    const height = Number(window.innerHeight) * 0.95;
    const margin = {top: 200, right: 20, bottom: 20, left: 20};
    const histogram_center = 300;
    const histogram_height = 100;

    const scatterPlotArea = {
        width: 300,
        height: 200,
        x: 50,  // x-coordinate of the top-left corner of the scatter plot area
        y: 50, // y-coordinate of the top-left corner of the scatter plot area
    };

    function addToScatterPlot(dataItem: Fatality) {
        // Generate a random position within the scatter plot area
        const xPosition = Math.random() * scatterPlotArea.width + scatterPlotArea.x;
        const yPosition = Math.random() * scatterPlotArea.height + scatterPlotArea.y;
    
        // Append a new circle to the SVG for each data item
        svg.append("circle")
            .attr("cx", xPosition)
            .attr("cy", yPosition)
            .attr("r", 5)
            .data([dataItem])  // radius of the circle
            .style("fill", d=>{
                if(d.citizenship === "Israeli")     return ISRAELI_BLUE;
                if(d.citizenship === "Palestinian") return PALESTINIAN_RED;
                return 'white';
            })
            .transition()
            .duration(config.scrubber.width_real_ms)
            .style("opacity", 0)
            .remove();  // remove the circle after the transition
    }
    
    

    const noon_time_to_fatalities = new Map<number, Fatality[]>();
    data.forEach(d => {
        d.parsed_date = parse_date(d.date_of_death);
        d.parsed_date.setHours(12,0,0,0);
        d.parsed_date_ms = d.parsed_date.getTime();
        const fatalities_list = noon_time_to_fatalities.get(d.parsed_date_ms);
        if(fatalities_list) {
            fatalities_list.push(d);
        }
        else {
            noon_time_to_fatalities.set(d.parsed_date_ms, [d])
        }
    });
    debug.noon_times(noon_time_to_fatalities);
    data.sort((a, b) => a.parsed_date_ms - b.parsed_date_ms);
    const israeli_deaths = data.filter(d => d.citizenship === "Israeli");
    const palestinian_deaths = data.filter(d => d.citizenship === "Palestinian")

    const svg = d3.select('#vis')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);


    const dateRange = d3.extent(data, d => d.parsed_date );
    const time_zero = dateRange[0].getTime();
    const totalMilliseconds = dateRange[1].getTime() - time_zero;
    const totalDays = ms_to_days(totalMilliseconds);
    const histogram_width = width - margin.left - margin.right;
    const pixelsPerDay = histogram_width / totalDays;
    const daysPerSecond = 100; // 365 * 5;
    const days_data_per_ms_real = daysPerSecond / 1000;
    const ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
    const animationDuration = (totalDays/days_data_per_ms_real);
    const framesPerSecond = 60;
    const frames_per_ms = 1000/framesPerSecond;
    const pixelsPerTick = pixelsPerDay * daysPerSecond / framesPerSecond;
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);
    config.scrubber.width = real_ms_to_width(config.scrubber.width_real_ms);

    const scrubber = svg.append('rect')
        .attr('x', 0)
        .attr('y', histogram_center)
        .attr('width', config.scrubber.width)
        .attr('height', config.scrubber.height)
        .attr('opacity',0.3)
        .attr('stroke', 'white  ');




    const padding_time = real_ms_to_data_ms(config.scrubber.width_real_ms);

    const scrub_x = d3.scaleTime()
        .domain([time_zero - padding_time, dateRange[1].getTime()])
        .range([-config.scrubber.width, histogram_width])
        .clamp(false);

    const totalWidthMilliseconds = totalMilliseconds + padding_time;

    function widthToMilliseconds(widthInPixels: number) {
        const oneDayPixelValue = x(new Date(time_zero + days_to_ms(1)));
        const days = widthInPixels / oneDayPixelValue;
        return days * (1000 / days_data_per_ms_real);
    }

    function data_ms_to_width(data_ms: number): number {
        const one_day_in_pixels = x(new Date(time_zero + days_to_ms(1)));
        const one_ms_in_pixels = one_day_in_pixels / ONE_DAY_MS;
        return data_ms * one_ms_in_pixels;
    }

    function real_ms_to_width(real_ms: number): number {
        return data_ms_to_width(real_ms_to_data_ms(real_ms));
    }

    function real_ms_to_data_ms(ms_real: number) {
        return ms_real * ms_data_per_ms_real;
    }

    let elapsed_last = 0;
    function histogram_tick(elapsed: number) {
        const elapsed_diff = elapsed - elapsed_last;
        const looped_epoch_time = (elapsed * ms_data_per_ms_real) % totalWidthMilliseconds;
        const current_time_right_ms = time_zero + looped_epoch_time;
        const current_time_left_ms = current_time_right_ms - padding_time;
        const scenario_elapsed = real_ms_to_data_ms(elapsed_diff);
        const new_data_interval = new TimeInterval(current_time_right_ms, scenario_elapsed);
        const new_data = interval_to_data(noon_time_to_fatalities, new_data_interval);
        new_data.forEach(d =>{
            addToScatterPlot(d);
        })
        const x_val = scrub_x(current_time_left_ms);
        const real_x = d3.max([0,x_val]) || 0;
        const subtraction_left = d3.min([x_val,0]) || 0;
        const width = d3.min([config.scrubber.width,histogram_width-real_x]) + subtraction_left;
        scrubber
            .attr('x', real_x)
            .attr('width', width)

        elapsed_last = elapsed;
    }

    d3.interval(histogram_tick,frames_per_ms)

    const xAxis = svg.append("g")
        .attr("transform", `translate(0,${margin.top})`)

    const thresholds = create_thresholds(dateRange[0],dateRange[1], 14)
    const histogram = d3.bin()
        .value(d => d.parsed_date)
        .domain(x.domain())
        .thresholds(thresholds)

    const israeli_bins = histogram(israeli_deaths);
    const palestinian_bins = histogram(palestinian_deaths)

    const y_range = height - margin.top - margin.bottom;

    const rect_height = d3.scaleLinear()
        .range([histogram_height,0])
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
    .then(on_data)