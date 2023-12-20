export class DynamicPieChart {
    constructor(svg_root, width, x, y) {
        this._dynamic_radius = false;
        this.diameter = width;
        this.width = width;
        this.height = width;
        this.radius = Math.min(this.width, this.height) / 2;
        this.x = x;
        this.y = y;
        this.svg_group = svg_root
            .append("g")
            .attr("transform", `translate(${x}, ${y})`);
        // sort(null) stops d3 from sorting by highest value, keep same order on updates
        this.pie = d3.pie().value((d) => d.value).sort(null);
        this.arc = d3.arc().innerRadius(0).outerRadius(this.radius);
        this._color = d3.scaleOrdinal(d3.schemeCategory10);
        return this;
    }
    dynamic_radius(v) {
        this._dynamic_radius = v;
    }
    calculateDynamicRadius(totalSum) {
        const minRadius = 3;
        const maxRadius = Math.min(this.width, this.height) / 2;
        const scaleFactor = Math.sqrt(totalSum) / 10;
        let newRadius = minRadius + scaleFactor;
        newRadius = Math.max(minRadius, Math.min(newRadius, maxRadius));
        return newRadius;
    }
    title(title) {
        this.svg_group.append("text")
            .attr("class", "pie-chart-title")
            .attr("x", -this.radius)
            .attr("y", -this.radius - 10)
            .attr("text-anchor", "left")
            .style("font-size", "12px")
            .style("fill", "white")
            .text(title);
        return this;
    }
    color(c) {
        this._color = c;
        return this;
    }
    updateData(bins) {
        if (this._dynamic_radius) {
            const total_sum = d3.sum(bins, d => d.value);
            this.radius = this.calculateDynamicRadius(total_sum);
            this.arc = d3.arc().innerRadius(0).outerRadius(this.radius);
        }
        this.drawLegend(bins);
        const pieData = this.pie(bins);
        const arcs = this.svg_group.selectAll(".pie-slice")
            .data(pieData);
        arcs.enter().append("path")
            .attr("class", "pie-slice")
            .attr("d", this.arc)
            .attr("fill", (d, i) => this._color(i.toString()))
            .transition()
            .duration(100);
        // Update existing arcs
        arcs.attr("d", this.arc)
            .attr("fill", (d, i) => this._color(i.toString()));
        // Remove old arcs
        arcs.exit().remove();
    }
    drawLegend(data) {
        const n = data.length;
        const including_spacing = this.height / data.length;
        const proportion = 0.8;
        const x = this.height / (proportion * n + (1 - proportion) * (n - 1));
        const legendRectSize = proportion * x;
        const legendSpacing = (1 - proportion) * x;
        const legend = this.svg_group.selectAll('.legend')
            .data(data)
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', (d, i) => {
            const height = legendRectSize + legendSpacing;
            const offset = height * data.length / 2;
            const horz = -2 * legendRectSize + this.width;
            const vert = i * height - offset;
            return `translate(${this.radius + 3}, ${vert})`;
        });
        legend.append('rect')
            .attr('width', 4)
            .attr('height', legendRectSize)
            .style('fill', (d, i) => this._color(i.toString()))
            .style('stroke', (d, i) => this._color(i.toString()));
        legend.append('text')
            .attr('x', 6)
            .attr('y', legendRectSize / 2)
            .attr('height', legendRectSize)
            .attr("dominant-baseline", "middle")
            .style("fill", 'white')
            .style("font-size", "10px")
            .text(d => title_case(d.category));
        return this;
    }
}
function title_case(str) {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}
//# sourceMappingURL=DynamicPieChart.js.map