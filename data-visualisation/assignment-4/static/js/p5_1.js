let sketch1 = function(p) {
    let data;
    p.preload = function preload() {
        console.log("running preload");
        data = p.loadJSON("/static/json/ransomware-attacks.json");
        console.log(data);
    }
}
new p5(sketch1, "p5-1")