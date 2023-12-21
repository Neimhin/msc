export class Slider {
    private svg: d3.Selection<SVGGElement, unknown, HTMLElement, undefined>;
    private sliderRect: d3.Selection<SVGRectElement, unknown, HTMLElement, undefined>;
    private handle: d3.Selection<SVGCircleElement, unknown, HTMLElement, undefined>;
    private sliderText: d3.Selection<SVGTextElement, unknown, HTMLElement, undefined>;
    private width: number;
    private height: number;
    private center: number;
    private currentValue: number;
    private _scale: (number: number) => number;
    private onDrag: (newValue: number) => void;
    private _textFormatter: (width: number) => string;
    private _text_formatter: (width: number) => void = ()=>'';
    constructor(svg, width, height, center, initialValue, onDrag) {
        this.svg = svg;
        this.width = width;
        this.height = height;
        this.center = center;
        this.currentValue = initialValue;
        this.onDrag = onDrag;

        this.initSlider();
    }

    text_formatter(f: (width:number)=>void) {
        if(f) {
            this._text_formatter = f;
            this.sliderText.text(this._text_formatter(this.currentValue))
            return this;
        }
        return this._text_formatter;
    }

    initSlider() {
        this.on_drag = (event) => {
            const newX = Math.max(0, Math.min(this.width, event.x));
            this.handle.attr("cx", newX);
            this.sliderRect.attr("width", newX);
            this.currentValue = newX;
            this.sliderText
                .attr("x", newX + 10)
                .text(this._text_formatter(newX));

            if (this.onDrag) {
                this.onDrag(newX);
            }
        };
        const sliderDrag = d3.drag()
            .on("drag", this.on_drag );

        this.sliderRect = this.svg.append("rect")
            .attr("width", this.currentValue)
            .attr("height", this.height)
            .attr("y", this.center)
            .attr("fill", "#ddd");

        this.handle = this.svg.append("circle")
            .attr("cx", this.currentValue)
            .attr("cy", this.center + this.height / 2)
            .attr("r", 8)
            .attr("fill", "steelblue")
            .style("opacity", 0.3)
            .call(sliderDrag);

        this.sliderText = this.svg.append("text")
            .attr("x", this.currentValue + 10)
            .attr("y", this.center + this.height / 2 + 5)
            .attr("text-anchor", "left")
            .attr("fill", "white");
    }

    setValue(newValue) {
        const newX = Math.max(0, Math.min(this.width, newValue));
        this.handle.attr("cx", newX);
        this.sliderRect.attr("width", newX);
        this.currentValue = newX;
        this.sliderText
            .attr("x", newX + 10)
            .text(`memory: ${ms_to_days(global.current).toFixed(1)} days`);
    }

    getValue() {
        return this.currentValue;
    }
}