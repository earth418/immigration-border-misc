// import * as zll from './zipc_latlon.json' with {type: "json"};
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


const array_data = parseCSV(geocoded_cbp);
array_data[0] = ["origin","","","","","","","",""] // this is the name layer anyway

let data = array_data.map((w) => {
    return {name : w[0], value: w[1], country : w[2], address: w[3], county: w[5], city: w[4], state: w[6], zip: w[7], lat: w[8], lon: w[9], parent: "origin"};
});

// thank you to 
// https://d3-graph-gallery.com/graph/treemap_basic.html
// for helping me realize I needed this parent stuff
// data[0].name = "origin";
data[0].parent = "";

const total_width = 1920, total_height = 1080;


// treemap1 starts at (106, 230)
// treemap1 ends (953, 935)
// treemap2 starts (960, 230)
// treemap2 ends (1808, 935)

const width = 975, height = 610;
const treemap_ht = 935 - 230;
const treemap_wd = 1808 - 960;

const root_data = d3.stratify()
    .id((d) => d.name)
    .parentId((d) => d.parent)
    (data);

root_data.sum((d) => +d.value);

const root = d3.treemap()
.tile(d3.treemapSquarify)
.size([treemap_wd+960, treemap_ht+230])
.padding(0)
.paddingTop(230)
.paddingLeft(960)
(root_data);


// Create the SVG container.
const svg = d3.create("svg")
    .attr("viewBox", [0, 0, total_width, total_height])
    .attr("width", total_width)
    .attr("height", total_height)
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");

const leaf = svg.selectAll("g")
    .data(root.leaves())
    .attr("id", (d) => d.data.county)
    .join("a")
        .attr("x", (d) => d.x0+10)
        .attr("y", (d) => d.y0+20)
        .attr("href", (d) => `#`)

const format = d3.format(",d");
leaf.append("title")
    .text(d => `${d.data.name.slice(1).replace(/\//g, ".")}\n${format(d.value)}`)

leaf.append("rect")
    .attr("x", (d) => d.x0)
    .attr("y", (d) => d.y0)
    .attr("width", (d) => d.x1 - d.x0)
    .attr("height", (d) => d.y1 - d.y0)
    .style("stroke","black")
    .style("stroke-width",0.5)
    .style("fill", (d) => ["#fee5a0", "#ffcf52", "#ffb803"][Math.floor(Math.random() * 3)])
    .style("fill-opacity", 0.9)


function wrapText(txt, text, width) {
     text.each(function() {
        const text = d3.select(this);
        const words = txt.split(/\s+/);
        const fontSize = parseFloat(text.attr("font-size")) || 10;
        const charWidth = fontSize * 0.6; // Approximate character width
        const maxCharsPerLine = Math.floor(width / charWidth);
        // let tspan = text.text(null).append("tspan").attr("x", text.attr("x")).attr("y", y).attr("dy", dy + "em");
        
        if (maxCharsPerLine <= 0) return;

        let currentLine = [];
        let lineNumber = 0;
        const lineHeight = 1.1;
        const y = text.attr("y");
        const dy = parseFloat(text.attr("dy")) || 0;
        
        for (let i = 0; i < words.length; i++) {
            const word = words[i];
            const testLine = currentLine.length > 0 ? currentLine.join(" ") + " " + word : word;
            
            if (testLine.length <= maxCharsPerLine) {
                currentLine.push(word);
            } else {
                if (currentLine.length > 0) {
                    // Add current line
                    text.append("tspan")
                        .attr("x", text.attr("x"))
                        .attr("y", y)
                        .attr("dy", lineNumber * lineHeight - dy + "em")
                        .text(currentLine.join(" "));
                    
                    lineNumber++;
                    currentLine = [word];
                } else {
                    // Word is too long for one line, add it anyway
                    text.append("tspan")
                        .attr("x", text.attr("x"))
                        .attr("y", y)
                        .attr("dy", lineNumber * lineHeight - dy + "em")
                        .text(word);
                    
                    lineNumber++;
                }
            }
        }
        
        // Add remaining words
        if (currentLine.length > 0) {
            text.append("tspan")
                .attr("x", text.attr("x"))
                .attr("y", y)
                .attr("dy", lineNumber * lineHeight - dy + "em")
                .text(currentLine.join(" "));
        }
    });
}

function font_sizepx2(d) {return (d.value / 3000000000) * 4 + 8}

function font_size2(d) {return font_sizepx2(d) + "px"}

function indent2(d) {
    const maxCharsPerLine = Math.floor((d.x1 - d.x0) / (font_sizepx2(d) * 0.7));
    return Math.floor(d.data.name.length / maxCharsPerLine) + 0.7;
}

function d_to_radius(d) {
    const val = Math.max(5,Math.sqrt(d.value) / 500);
    return val;
}

    // .each(function(d) { 
    //     const width = Math.max(0, Math.floor(d.x1 - d.x0) - 4);
    //     wrapText(d.data.name, d3.select(this), width);
    // })
//     .filter(d => d.value > 400000000).append("tspan")
//         .text(d => `$${format(Math.floor(d.value / 1000000))} million`)
//         .attr("x", (d) => (d.x0 + d.x1) / 2.0)
//         .attr("y", (d) => (d.y1 + d.y0) / 2.0)
//         .attr("dy", (d) => indent2(d) + "em")
//         // .attr("dy", (d) => (d.value < 400000000) ? "3.0em" : "1.0em")
//         .attr("font-size", font_size2)
//         .attr("fill", "black")

document.getElementById("treecbp-container").append(svg.node());

function centroid(feature) {
    const path = d3.geoPath();
    return path.centroid(feature);
}

function adjust(position) {
    return [position[0] * total_width / width, position[1] * total_height / height];
}

function wiggle(position) {
    const factor = 5;
    return position.map((w) => w + Math.random() * factor * 2 - factor);
}



const projection1 = d3.geoMercator()
    .center([-97.42011851400741, 38.56265081052521])
    .translate([total_width / 2, total_height / 2])
    .scale(1900)

function transition() {

    // const duration = 40000;
    const duration = 1000;

    d3.select("#treecbp-container").transition()
        .duration(duration)
        .style("background-color",null);
        
    leaf.selectAll("rect").transition()
        .duration(duration)
        .attr("height", d_to_radius)
        .attr("width", d_to_radius)
        .attr("x", d => -d_to_radius(d)/2.0)
        .attr("y", d => -d_to_radius(d)/2.0)
        .attr("rx", d_to_radius)
        .attr("ry", d_to_radius)
    
    // leaf.filter(d => d.value > 293000000).append("text")
    //     .attr("x", (d) => (d.x0 + d.x1 + d_to_radius(d)) / 2.0)
    //     .attr("y", (d) => (d.y0 + d.y1 + d_to_radius(d)) / 2.0)
    //     .attr("dy", "0.1em")
    //     .attr("text-anchor", "middle")
    //     .attr("font-size", font_size2)
    //     .attr("fill", "black")
    //     .attr("font-family", "proxima-nova")
    //     .text(d => d.data.name.split(" ").slice(0, 2).join(" "))
    
    // leaf.selectAll("text").remove();
    
    leaf.transition().duration(duration)
        .attr("transform", d => `translate(${projection1([d.data.lon, d.data.lat])})`)
        // .attr("transform", d => `translate(${location_of(d.data.zip)})`)
   
}

let f_index = 0;
const findex_map = [-1, -1, 0];
// const names = ["THE GEO GROUP, INC.", "DEPLOYED RESOURCES LLC"];
const names = ["DEPLOYED RESOURCES LLC"];
const locations = [{
    x0: 1194,
    x1: 1694,
    y0: 230,
    y1: 935
}]

function untransition() {

    const duration = 1000;

    const f_ind = findex_map[f_index];
    if (f_ind == -1) {
        return;
    }
    const l = locations[f_ind];
    
    // d3.select("#treecbp-container").transition().duration(duration).style("background-color","lightgrey");


    leaf.filter(d => d.data.name == names[f_ind])
        .attr("position", "absolute")
        .attr("z-index", 99999)
        // .raise().raise().raise()
        // .raise().raise().raise()
        // .raise().raise().raise()
        // .raise().raise().raise()
        // .raise().raise().raise()
    console.log(leaf.filter(d => d.data.name == names[f_ind]));

    leaf.filter(d => d.data.name == names[f_ind]).selectAll("rect").transition()
        .duration(duration)
        // .attr("x", (d) => d.x0)
        // .attr("y", (d) => d.y0)
        // .attr("width", (d) => d.x1 - d.x0)
        // .attr("height", (d) => d.y1 - d.y0)
        .attr("x", (d) => l.x0 - 100)
        .attr("y", (d) => l.y0)
        .attr("width", (d) => l.x1 - l.x0)
        .attr("height", (d) => l.y1 - l.y0)
        .attr("rx", 0)
        .attr("ry", 0)
        .style("fill-opacity", 1.0)



    // d3.select("#treeice-container").append(leaf.filter(d => d.data.name == names[f_ind]).node());
        
    leaf.filter(d => d.data.name == names[f_ind])
        .append("text")
        .attr("x", (d) => (l.x0 + l.x1) / 2.0)
        .attr("y", (d) => (l.y0 + l.y1) / 2.0)
        .attr("dy", "0.5em")
        .attr("text-anchor", "middle")
        .attr("font-size", 15)
        .attr("fill", "black")
        .attr("font-family", "proxima-nova")
        .text(d => d.data.name)
        // .text(d => d.data.name.split(" ").slice(0, 2).join(" "))

        leaf.filter(d => d.data.name == names[f_ind]).transition().duration(duration)
            .attr("transform", `translate(0.0,0.0)`)
            // .attr("x", -5800)
            // .attr("y", 500)

}

// [].slice

document.addEventListener("keydown", (e) => {
    if (e.key == "d") {
        transition();
    }
    if (e.key == "f") {
        untransition();
        f_index++;
        if (f_index == findex_map.length) {
            f_index = 0;
        }
    }
});