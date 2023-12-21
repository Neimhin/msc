import { drag } from 'd3';
class Slider {
    constructor(svg, x, y, width, height, onDrag) {
        this.svg = svg;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.onDrag = onDrag;
        this.createSlider();
    }
    createSlider() {
        this.rect = this.svg.append("rect")
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("x", this.x)
            .attr("y", this.y)
            .attr("fill", "#ddd");
        this.handle = this.svg.append("circle")
            .attr("cx", this.width)
            .attr("cy", this.y + this.height / 2)
            .attr("r", 8)
            .attr("fill", "steelblue")
            .style("opacity", 0.3);
        const sliderDrag = drag()
            .on("drag", (event) => {
            const newX = Math.max(0, Math.min(this.width, event.x));
            this.handle.attr("cx", newX);
            this.rect.attr("width", newX);
            this.onDrag(newX);
        });
        this.handle.call(sliderDrag);
    }
    updateWidth(newWidth) {
        this.width = newWidth;
        this.rect.attr("width", this.width);
        this.handle.attr("cx", this.width);
    }
}
export default Slider;
//# sourceMappingURL=slider.js.map