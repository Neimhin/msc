const GOLDEN_RATIO = 1.618

let sketch1 = function(p) {
    let data;
    p.preload = function preload() {
        console.log("running preload");
        data = p.loadJSON("/static/json/ransomware-attacks.json");
        console.log(data);
    }

    p.setup = function setup() {
        console.log("running setup");
        p.createCanvas(400 * GOLDEN_RATIO, 400);
    }

    p.draw = function draw() {
        p.background(255);
        p.stroke(220);
        console.log(p.width)
        for (var j=0; j<=p.width; j=j+50) {
            p.line(0, j, p.width, j);
        }
    }
}
new p5(sketch1, "p5-1")