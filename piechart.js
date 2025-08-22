import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

function parseCSV(str) {
    // Function written by Trevor Dixon, https://stackoverflow.com/a/14991797

    const arr = [];
    let quote = false;  // 'true' means we're inside a quoted field

    // Iterate over each character, keep track of current row and column (of the returned array)
    for (let row = 0, col = 0, c = 0; c < str.length; c++) {
        let cc = str[c], nc = str[c+1];        // Current character, next character
        arr[row] = arr[row] || [];             // Create a new row if necessary
        arr[row][col] = arr[row][col] || '';   // Create a new column (start with empty string) if necessary

        // If the current character is a quotation mark, and we're inside a
        // quoted field, and the next character is also a quotation mark,
        // add a quotation mark to the current column and skip the next character
        if (cc == '"' && quote && nc == '"') { arr[row][col] += cc; ++c; continue; }

        // If it's just one quotation mark, begin/end quoted field
        if (cc == '"') { quote = !quote; continue; }

        // If it's a comma and we're not in a quoted field, move on to the next column
        if (cc == ',' && !quote) { ++col; continue; }

        // If it's a newline (CRLF) and we're not in a quoted field, skip the next character
        // and move on to the next row and move to column 0 of that new row
        if (cc == '\r' && nc == '\n' && !quote) { ++row; col = 0; ++c; continue; }

        // If it's a newline (LF or CR) and we're not in a quoted field,
        // move on to the next row and move to column 0 of that new row
        if (cc == '\n' && !quote) { ++row; col = 0; continue; }
        if (cc == '\r' && !quote) { ++row; col = 0; continue; }

        // Otherwise, append the current character to the current column
        arr[row][col] += cc;
    }
    return arr;
}

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


const raw_data = parseCSV(pie_data); //.shift();


// console.log(raw_data);

const data = raw_data.map((rd) => {
    // year: w[0]
    // immigration stuff = w[1] + w[2] + w[3] + w[4] + 0.25 * w[5]
    // w[6] => secret service
    // w[7] => marshals service
    // w[8] => fbi
    // w[9] => dea
    // w[10] => atf
    // w[11] => traffic safety
    // w[12] => irs enforcement
    // w[13] => ucsp capitol police
    // return {immigration: w[1]+w[2]+w[3]+w[4]+0.25*w[5], 
    let w = rd.map(parseFloat);
    return {cbp: w[1],
            ice: w[2],
            // uccis: w[3],
            // dhs: w[4],
            uscg: 0.25*w[5], 
            usss : w[6], 
            usms : w[7], 
            fbi : w[8], 
            dea : w[9], 
            atf : w[10], 
            // traffic : w[11], 
            // irs : w[12], 
            // ucsp : w[13], 
    };
});

console.log(data);

// var data = [
//     {"ICE": 4.1, "CBP": 5.4, "D":4},
//     {"ICE": 5.2, "CBP": 7.2, "D":3},
//     {"ICE": 7.2, "CBP": 8.1, "D":3},
//     {"ICE": 7.5, "CBP": 8.8, "D":4},
//     {"ICE": 8.1, "CBP": 10.5, "D":3.5},
// ];

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


const IIC_arr = ["ice","cbp","uccis","dhs","uscg"];
// const IIC_color = w => ["#fee5a0", "#ffcf52", "#ffb803"][Math.floor(w.name.charCodeAt(1)) % 3];
const colors = {
    "fbi":"#004d65",
    "dea":"#66a4b7",
    "usms":"#abe9fd",
    "atf":"#c38b57ff",
    "usss":"#9f7146ff",
    "uscg":"#dac3ad",
    "ice":"#ffb803",
    "cbp":"#fee5a0"
};

const order = ["fbi","dea","usms",
    "atf","usss","uscg","cbp","ice"];

function create_pie(data) {
    const total = data.reduce((a, b) => a + b[1], 0);
    const total_IIC = data.reduce((a, b) => a + (IIC_arr.includes(b[0])) * b[1], 0);
    console.log(data);
    let last_end = 0;

    const sorted = data.sort((a, b) => 
        order.findIndex((w) => w == a[0]) - order.findIndex((w) => w == b[0]));
        // .sort((a, b) => b[1] - a[1])
        // .filter(a => IIC_arr.includes(a[0]))
        // // .sort((a, b) => a[0].localeCompare(b[0]))
        // .concat(
        //     data.filter(a => !IIC_arr.includes(a[0]))
        //     .sort((a,b) => a[1] - b[1])
        //     // .sort((a,b) => a[0].localeCompare(b[0]))
        // );
    const arr_angles = sorted.map((a, i) => {
        const ang = 2 * Math.PI * a[1] / total;
        var last_start = (i == 0) ? -Math.PI * total_IIC / total : last_end;
        last_end = last_start + ang;
        
        return {
            name: a[0], 
            value: a[1], 
            color: colors[a[0]],
            angle: ang,
            startAngle: last_start,
            endAngle: last_end
        };
    });
    return arr_angles;
}

const arcGen = 
            d3.arc()
            .innerRadius(0)
            .outerRadius(radius);

function create(data) {
    
    const pie_data = create_pie(data);
    const u = svg.selectAll("path").data(pie_data);

    u.selectAll("text")
        .attr("transform", d => `translate(${arcGen.centroid(d)})`)
        

    u
        .enter()
        .append('path')
        .merge(u)
        .attr("d",
            arcGen
        )
        // .transition(1000)
        // .attrTween("d", arcTween)
        .attr("id", d => d.name)
        .attr("fill", d => d.color)
        .style("stroke-width", "0px")
        .style("opacity",1)
        // .attr("fill", d => (IIC_arr.includes(d.name)) ? IIC_color(d) : "#ded")
        // .attr("stroke", "black")
        // .append('p')
        //     .text(d => d.name)
        //     .attr("transform", d => {
        //         let ar = arc.centroid(d)
        //         // console.log(ar);
        //         return `translate${ar[0]},${ar[1]}`;
        //     });

    // u
    //     .enter()
    //     .append("text")
    //     .text(d => d.name)
    //     .attr("transform", d => `translate(${arcGen.centroid(d)})`)
    //     .style("text-transform","uppercase")
    //     .style("font-family","sans-serif")
    //     .style("text-anchor","middle")
    //     .style('font-size', d => 4 + 20 * (d.value / 5000))
        // .exit()
        // .remove()
    
    u
        .exit()
        .remove()
    // return u;
}


let yr = document.getElementById("year-label");
yr.innerText = "2004";
const fp_data = 2;
let i = fp_data;
create(Object.entries(data[1]));

document.addEventListener("keydown", (e) => {
    if (e.key == "d") {
        i++;
        let data_index = Math.floor(i / fp_data);
        if (data_index >= data.length)
            return;

        // create(data_i);
        yr.innerText = 2004 + data_index;

        // Object.entries(data[data_index]).map((d, ind) => console.log(data[data_index+1][d[0]] - d[1]));
        let data_i;
        if (fp_data > 1)
            data_i = Object.entries(data[data_index]).map((d, ind) => [d[0], d[1] + ((i % fp_data) / fp_data) * (data[data_index+1][d[0]] - d[1])]);
        else
            data_i = Object.entries(data[i]);
    
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