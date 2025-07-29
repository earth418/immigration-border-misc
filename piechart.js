import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const width = 900, height = 900, 
      margin = 40;


const radius = 900 / 2 - margin;

// .attr("viewBox", [0, 0, width, height])
// .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
const svg = d3.select("#export")
    .append("svg")
        .attr("width", width)
        .attr("height", height)   
    .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

var data = [
    {"ICE": 4, "CBP": 5, "D":3},
    {"ICE": 5, "CBP": 7, "D":40}
];

var arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

function arcTween(d) {

    var i = d3.interpolate(this._current, d);

    this._current = i(0);

    return function(t) {
        return arc(i(t));
    }
}


const IIC_arr = ["ICE","CBP"];

function create_pie(data) {
    const total = data.reduce((a, b) => a + b[1], 0);
    const total_IIC = data.reduce((a, b) => a + (IIC_arr.includes(b[0])) * b[1], 0);
    console.log(total_IIC);
    let last_end = 0;
    const arr_angles = data.map((a, i) => {
        const ang = 2 * Math.PI * a[1] / total;
        var last_start = (i == 0) ? -Math.PI * total_IIC / total : last_end;
        last_end = last_start + ang;
        
        return {
            name: a[0], 
            value: a[1], 
            angle: ang,
            startAngle: last_start,
            endAngle: last_end
        };
    });
    return arr_angles;
}

function create(data) {
    
    const pie_data = create_pie(data);
    const u = svg.selectAll("path").data(pie_data);

    u
        .enter()
        .append('path')
        .merge(u)
        .transition(1000)
        .attrTween("d", arcTween)
        .attr("d", d3.arc()
            .innerRadius(0)
            .outerRadius(radius)
            // .startAngle(d => -get_half_angle(d))
            // .endAngle(d => get_half_angle(d))
        )
        .attr("id", d => d.name)
        .attr("fill", d => (IIC_arr.includes(d.name)) ? "#dad" : "#ded")
        .attr("stroke", "black")
        .style("stroke-width", "2px")
        .style("opacity",1)

    u
        .exit()
        .remove()
}

let i = 0;
let u = create(Object.entries(data[0]));

document.addEventListener("keydown", (e) => {
    if (e.key == "d") {
        i++;
        let data_i = Object.entries(data[0]).map((d) => [d[0], d[1] + (i / 40.0) * (data[1][d[0]] - d[1])]);
        create(data_i);
    }
});



// create(Object.entries(data[0]));
// await new Promise(r => setTimeout(r, 1000));
// create(Object.entries(data[1]));
// update(Object.entries(data[0]));
// for (let i = 0; i < 40; ++i) {
//     let data_i = Object.entries(data[0]).map((d) => [d[0], d[1] + (i / 40.0) * (data[1][d[0]] - d[1])]);
//     console.log(data_i);
//     await new Promise(r => setTimeout(r, 100));
//     update(data_i);
// }