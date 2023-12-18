const global = {
    debug: true,
    test: true,
    scrubber: {
        dragging: false,
        paused: false,
        height: 10,
        width: undefined,
        width_real_ms: 3000,
        click_diff: 0,
    },
    lazy: {
        fatalities: undefined as unknown as Fatality[],
        districts: undefined as unknown as DistrictGeo[],
        noon_time_to_fatalities: undefined as unknown as Map<number, Fatality[]>,
        type_of_injury_unique: undefined as unknown as Set<string>,
        type_of_injury_index: undefined as unknown as (input: string) => number,
        type_of_injury_scale: undefined,
    },

}

const ISRAELI_BLUE = "#0038b8";
const PALESTINIAN_RED = "#EE2A35";
const CENTER_LONG = 31.694636423652604;
const CENTER_LAT = 34.90729984570858;
const CENTER_COORD = [CENTER_LONG, CENTER_LAT];

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
    parsed_date_ms_with_noise: number;
    age_with_noise: number;
}

function on_fatalities(d: Fatality[]){
    global.lazy.fatalities = d;
    global.lazy.noon_time_to_fatalities = new Map<number, Fatality[]>();
    global.lazy.fatalities.forEach(d => {
        d.parsed_date = parse_date(d.date_of_death);
        d.parsed_date.setHours(12,0,0,0);
        d.parsed_date_ms = d.parsed_date.getTime();
        d.parsed_date_ms_with_noise = d.parsed_date_ms + Math.random() * ONE_DAY_MS;
        d.age_with_noise = d.age + Math.random();
        const fatalities_list = global.lazy.noon_time_to_fatalities.get(d.parsed_date_ms);
        if(fatalities_list) {
            fatalities_list.push(d);
        }
        else {
            global.lazy.noon_time_to_fatalities.set(d.parsed_date_ms, [d])
        }
    });
    debug.noon_times(global.lazy.noon_time_to_fatalities);
    global.lazy.fatalities.sort((a, b) => a.parsed_date_ms - b.parsed_date_ms);

    global.lazy.type_of_injury_unique = new Set(global.lazy.fatalities.map(d => d.type_of_injury).filter(d=>d));
    console.log("num types of injury:", global.lazy.type_of_injury_unique.size);
    const types_of_injury = Array.from(global.lazy.type_of_injury_unique).sort();
    const type_of_injury_map: {[key: string]: number} = {};
    types_of_injury.forEach((v,i)=>{
        type_of_injury_map[v] = i;
    })
    function type_of_injury_index(t: string) {
        return type_of_injury_map[t];
    }
    global.lazy.type_of_injury_index = type_of_injury_index;
    maybe_main();
}

export interface DistrictGeo {
  district_tuple: string[]
  search_string: string
  geocode_result: GeocodeResult[]
}

export interface GeocodeResult {
  address_components: AddressComponent[]
  formatted_address: string
  geometry: Geometry
  place_id: string
  types: string[]
  partial_match?: boolean
}

export interface AddressComponent {
  long_name: string
  short_name: string
  types: string[]
}

export interface Geometry {
  bounds?: Bounds
  location: Location
  location_type: string
  viewport: Viewport
}

export interface Bounds {
  northeast: Northeast
  southwest: Southwest
}

export interface Northeast {
  lat: number
  lng: number
}

export interface Southwest {
  lat: number
  lng: number
}

export interface Location {
  lat: number
  lng: number
}

export interface Viewport {
  northeast: Northeast2
  southwest: Southwest2
}

export interface Northeast2 {
  lat: number
  lng: number
}

export interface Southwest2 {
  lat: number
  lng: number
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

class Interval {
    start: number;
    end: number;
    constructor(start:number,end:number) {
        this.start = start;
        this.end = end;
    }

    has(t: number) {
        return t > this.start && t <= this.end
    }

    subtract_same_length(it: Interval): Interval {
        // assuming both intervals have same length
        // case 1
        //       ..
        //    ..
        // or
        //  ..
        //       ..
        if((it.end <= this.start) || it.start >= this.end) {
            return this.clone();
        }

        // case 2
        //    .........
        //  .........
        if(it.end > this.start && it.start <= this.start) {
            return new Interval(it.end, this.end);
        }

        // case 3
        // ......
        // ......
        if(it.start == this.start) {
            return new Interval(this.end,this.end);
        }

        // case 4
        // ...
        //  ...
        if(it.start > this.start) {
            return new Interval(this.start, it.start);
        }

    }

    clone(): Interval {
        return new Interval(this.start,this.end);
    }
}

if(global.test) {
    (()=>{
        const i1 = new Interval(100,110);
        const i2 = new Interval(50, 60);
        const sub = i1.subtract_same_length(i2);
        if(sub.start === i1.start && sub.end === i1.end) {
            console.log("test passed:", i1, "-", i2, "=", sub);
        }
        else {
            console.error("test failed:", i1, "-", i2, "=", sub);
        }
    })("subtract case 1")
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
            // console.log(new Date(k));
        }

    }
}

function data_to_lists_of_districts(fs: Fatality[]): {"West Bank": Set<string>, "Gaza Strip": Set<string>, "Israel": Set<string>} {
    const ret = {
        "West Bank": new Set(),
        "Gaza Strip": new Set(),
        "Israel": new Set(),
    }
    const regions = new Set(Object.getOwnPropertyNames(ret));
    function each(fatality: Fatality) {
        if(global.test) {
            if(!regions.has(fatality.event_location_region)) {
                throw new Error(`data has no region: ${JSON.stringify(fatality)}`)
            }
        }
        ret[fatality.event_location_region].add(fatality.event_location_district)
    }
    fs.forEach(each)
    return ret;
}



function find_first(time_ms: number) {
    const len = global.lazy.fatalities.length;

}

function find_in_interval(it: Interval) {
    return global.lazy.fatalities.filter(d=>{
        return it.has(d.parsed_date_ms_with_noise)
    })
}

function on_districts(d: DistrictGeo[]){
    global.lazy.districts = d;
    // const lat_1 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.northeast.lat)
    // const lat_2 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.southwest.lat)
    // const lng_1 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.northeast.lng)
    // const lng_2 = global.lazy.districts.map(d => d.geocode_result[0].geometry.viewport.southwest.lng)
    // const extent_lat = d3.extent(lat_1.concat( lat_2 ));
    // const extent_lng = d3.extent(lng_1.concat( lng_2 ));
    // const bounds = [
    //     [extent_lng[0], extent_lat[0]],
    //     [extent_lng[1], extent_lat[1]]
    // ];
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

function add_injury_labels(types_of_injury,svg) {
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
            d3.select(this).attr('transform', `rotate(-45 ${x} ${y})`); // Apply rotation
        });
}


function maybe_main() {
    if(global.lazy.fatalities && global.lazy.districts) {
        main();
    }
}



function main() {
    const lists_of_districts = data_to_lists_of_districts(global.lazy.fatalities);

    d3.select("#vis").selectAll("*").remove()
    const width = window.innerWidth * 0.9;
    const height = 350 * 2;


    const margin = {top: 200, right: 30, bottom: 20, left: 30};

    const svg = d3.select('#vis')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append("g")     
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const projection = d3.geoMercator()
        .center(CENTER_COORD)
        .scale(980 *2 )
        .translate([width/2, height/2]);

    svg.append("circle")
        .attr("cx", d => projection(CENTER_COORD)[0])
        .attr("cy", d => projection(CENTER_COORD)[1])
        .attr("r", 1);
    const histogram_center = 300;
    const histogram_height = 100;
    const histogram_width = width - margin.left - margin.right;

    global.lazy.type_of_injury_scale = d3.scaleLinear()
        .domain([0,12])
        .range([0, histogram_width]);
    add_injury_labels(Array.from(global.lazy.type_of_injury_unique), svg);
    

    const scatterPlotArea = {
        width: histogram_width,
        height: 200,
        x: 50,
        y: 50,
    };

    const age_range = d3.extent(global.lazy.fatalities, d=>d.age);
    const age_scale = d3.scaleLinear()
        .domain(age_range)
        .range([scatterPlotArea.height + scatterPlotArea.y, scatterPlotArea.y])

    const yAxis = d3.axisLeft(age_scale);

    function calculateMeanAge(data: Fatality[]): number {
        const totalAges = data.reduce((sum, fatality) => sum + fatality.age, 0);
        const meanAge = totalAges / data.length;
        return meanAge;
    }
    
    // Assuming 'data' is the array of Fatality objects
    const meanAge = calculateMeanAge(global.lazy.fatalities);
    console.log('Mean Age:', meanAge);
    


    function addToScatterPlot(dataItem: Fatality) {
        const xPosition = global.lazy.type_of_injury_scale(global.lazy.type_of_injury_index(dataItem.type_of_injury) + Math.random());
    
        svg.append("circle")
            .attr("class", "fatality")
            .attr("r", 3)
            .data([dataItem])
            .attr("cx", xPosition)
            .attr("cy", d => age_scale(d.age_with_noise))
            .style("fill", d=>{
                if(d.citizenship === "Israeli")     return ISRAELI_BLUE;
                if(d.citizenship === "Palestinian") return PALESTINIAN_RED;
                return 'white'; // Jordanian or American
            })
            .on("mouseover", function (event, d) {
                console.count("mouseover-circle")
                const opacity = fatality_to_opacity(d);
                if(opacity < 0.00001) return
                tooltip.transition()
                .duration(10)
                .style("opacity", 0.9);
                tooltip.html(`<strong>Name:</strong> ${d.name}<br>
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
    const palestinian_deaths = global.lazy.fatalities.filter(d => d.citizenship === "Palestinian")

    // console.log(global.lazy.districts);
    // const district_rects = svg.selectAll("rect")
    //     .data(global.lazy.districts)
    //     .enter()
    //     .append("rect")
    //     .attr("class", "geo-bounds")
    //     .attr("x", d => {
    //         const northeast = d.geocode_result[0].geometry.viewport.northeast;
    //         const southwest =  d.geocode_result[0].geometry.viewport.southwest;
    //         console.log(northeast,southwest);
    //         d.northeast_x_y = projection([northeast.lng, northeast.lat])
    //         d.southwest_x_y = projection([southwest.lng, southwest.lat])
    //         console.log(d.northeast_x_y, d.southwest_x_y);
    //         d.x = d.southwest_x_y[0];
    //         d.y = d.northeast_x_y[1];
    //         d.width = d.northeast_x_y[0] - d.southwest_x_y[0];
    //         d.height =  d.southwest_x_y[1] - d.northeast_x_y[1];

    //         console.log(d.x, d.y, d.width, d.height)
    //         return d.x;
    //     })
    //     .attr("y", d => d.y)
    //     .attr("width", d => d.width)
    //     .attr("height", d => d.height)
    //     .on("mouseover", function (event, d) {
    //         console.log("mouseover", event,d)
    //         d3.select(this).classed("hover", true)
    //     })
    //     .on("mouseout", function(event, d) {
    //         console.log("mouseout", event,d)
    //         d3.select(this).classed("hover", false)
    //     })
    //     .style("fill", "blue")
    //     .style("opacity", 0.2)


    const tooltip = svg.append("foreignObject")
        .attr("class", "tooltip")
        .attr("width", 400)
        .attr("height", 800)
        .attr("x", 0)
        .attr("y", 0)
        .style("text-align", "left")
        .style("color", "white")
      .append("xhtml:div")
        .style("opacity", 0)
        .attr("class", "tooltip-content")

    svg.append("g")
    .attr("class", "y-axis")
    .call(yAxis);
    svg.selectAll(".y-axis path")
        .style("stroke", "white");
    svg.selectAll(".y-axis text")
        .style("fill", "white")
    svg.selectAll(".y-axis line")
        .style("stroke", "white")

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

    const dateRange = d3.extent(global.lazy.fatalities, d => d.parsed_date );
    const time_zero = dateRange[0].getTime();
    const totalMilliseconds = dateRange[1].getTime() - time_zero;
    const daysPerSecond = 365/2;
    const days_data_per_ms_real = daysPerSecond / 1000;
    const ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
    const framesPerSecond = 12;
    const frames_per_ms = 1000/framesPerSecond;
    const x = d3.scaleTime()
        .domain(dateRange)
        .range([0, histogram_width]);
    
    global.scrubber.width = real_ms_to_width(global.scrubber.width_real_ms);

    const scrubber = svg.append('rect')
        .attr('x', 0)
        .attr('y', histogram_center)
        .attr('width', global.scrubber.width)
        .attr('height', global.scrubber.height)
        .attr('opacity',0.3)
        .attr('stroke', 'white')
        .call(d3.drag() // Apply drag behavior
            .on('start', dragStarted)
            .on('drag', dragging)
            .on('end', dragEnded)
      );
    
    // Functions to handle drag events
    function dragStarted(event, d) {
      global.scrubber.click_diff = event.x - Number(scrubber.attr('x'))
      // Handle the start of the drag event
      global.scrubber.dragging = true;
    }

    const padding_time_data_ms = real_ms_to_data_ms(global.scrubber.width_real_ms);
    const scrub_x = d3.scaleTime()
        .domain([time_zero - padding_time_data_ms, dateRange[1].getTime()])
        .range([-global.scrubber.width, histogram_width])
        .clamp(false);

    const max_real_ms =  data_ms_to_real_ms(dateRange[1]?.getTime() - dateRange[0]?.getTime());
    const scrub_x_real_ms = d3.scaleLinear()
        .domain([0, histogram_width])
        .range([0, max_real_ms])
        .clamp(false);
    d3.interval(function(){
        console.log(svg.selectAll(".fatality").size());

    },1000)
    function histogram_tick(elapsed: number) {
        elapsed_real_ms_diff = elapsed - elapsed_real_ms_last;
        if(!global.scrubber.paused && !global.scrubber.dragging) {
            elapsed_real_ms_virtual += elapsed_real_ms_diff;
        }
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
        const items_to_add = find_in_interval(interval_to_add);
        items_to_add.forEach(addToScatterPlot);
        const x_val = scrub_x(current_time_left_ms);
        const real_x = d3.max([0,x_val]) || 0;
        const subtraction_left = d3.min([x_val,0]) || 0;
        const width = d3.min([global.scrubber.width,histogram_width-real_x]) + subtraction_left;
        scrubber
            .attr('x', real_x)
            .attr('width', Math.abs(width))
        update_scatter();
        
        elapsed_real_ms_last = elapsed;
    }

    function scrub_x_to_elapsed_real_ms(scrubber_x: number) {
        let elapsed_real_ms = scrub_x_real_ms(scrubber_x);
        if(elapsed_real_ms < 0) {
          elapsed_real_ms = max_real_ms + global.scrubber.width_real_ms + elapsed_real_ms;
        }
        return elapsed_real_ms;
    }
    
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

    const totalWidthMilliseconds = totalMilliseconds + padding_time_data_ms;

    function width_to_ms_data(widthInPixels: number) {
        const oneDayPixelValue = scrub_x(new Date(time_zero + days_to_ms(1)));
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

    function data_ms_to_real_ms(ms_data: number) {
        return ms_data / ms_data_per_ms_real;
    }

    if(global.test) {
        const real_ms = 1000;
        const data_ms = real_ms_to_data_ms(real_ms);
        const out = data_ms_to_real_ms(data_ms);
        if(real_ms !== out) {
            throw new Error("inverse ms broken ${in} ${out}")
        }
    }

    const opacity_scale = d3.scaleLinear()
        .domain([real_ms_to_data_ms(global.scrubber.width_real_ms),0])
        .range([0,1])

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
        .attr("fill", "white")

    const dateFormat = d3.timeFormat("%Y %b %d");

    function fatality_to_opacity(d: Fatality) {
        const diff = current_time_right_ms - d.parsed_date_ms_with_noise;
        if(diff < 0) return 0;
        return opacity_scale(diff)
    }

    function update_scatter() {
        svg.selectAll(".fatality")
          .each(function(d) {
            if(interval_to_remove.has(d.parsed_date_ms_with_noise)) {
                this.remove();
            }
          })
          .style("opacity", fatality_to_opacity);

        const text = dateFormat(new Date(current_time_right_ms));
        const x = Number(scrubber.attr("x")) + Number(scrubber.attr("width"));
        const y = Number(scrubber.attr("y")) + 30;
        dateText.text(text)
            .attr("x", x)
            .attr("y", y);
    }

    function positiveModulo(dividend: number, divisor: number) {
        return ((dividend % divisor) + divisor) % divisor;
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
        .domain([d3.max(histogram(global.lazy.fatalities), d => d.length), 0]);

    function bin_width(d) {
        return Math.max(0, x(d.x1) - x(d.x0));
    }

    svg.selectAll("rect")
        .data(israeli_bins)
        .enter()
        .append("rect")
        .attr("x", d => x(d.x0))
        .attr("y", d => histogram_center + global.scrubber.height)
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
    .then(on_fatalities)

fetch('/static/json/districts_geocode.json')
    .then(on_response)
    .then(on_districts)