import us from './counties-albers-10m.json' with {type: "json"};
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


const array_data = parseCSV(treemap_text);
array_data[0] = ["origin","","","","","",""] // this is the name layer anyway

let data = array_data.map((w) => {
    return {name : w[0], value: w[1], country : w[2], address: w[3], county: w[5], city: w[4], state: w[6], zip: w[7], parent: "origin"};
});

// thank you to 
// https://d3-graph-gallery.com/graph/treemap_basic.html
// for helping me realize I needed this parent stuff
// data[0].name = "origin";
data[0].parent = "";

const total_width = 1920, total_height = 1080;

const width = 975, height = 610;
const treemap_ht = 1000;

const root_data = d3.stratify()
    .id((d) => d.name)
    .parentId((d) => d.parent)
    (data);

root_data.sum((d) => +d.value);

const root = d3.treemap()
.tile(d3.treemapSquarify)
.size([total_width / 2, treemap_ht])
.padding(0)
.paddingTop((total_height - treemap_ht))
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
        .attr("href", (d) => `https://google.com`)

const format = d3.format(",d");
leaf.append("title")
    .text(d => `${d.data.name.slice(1).replace(/\//g, ".")}\n${format(d.value)}`)

leaf.append("rect")
    .attr("x", (d) => d.x0)
    .attr("y", (d) => d.y0)
    .attr("width", (d) => d.x1 - d.x0)
    .attr("height", (d) => d.y1 - d.y0)
    .style("stroke","black")
    .style("fill", (d) => ["#ffe3c8", "#ffecd7"][Math.floor(Math.random() * 2)])
    .style("fill-opacity", 1.0)

// from claude
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

function font_sizepx(d) {return ((d.value / 1000000000) * 5 + 5);}

function font_size(d) {return font_sizepx(d) + "px"}

function indent(d) {
    const maxCharsPerLine = Math.floor((d.x1 - d.x0) / (font_sizepx(d) * 0.6));
    return Math.floor(d.data.name.length / maxCharsPerLine) + 0.7;
}

// leaf.filter(d => d.value > 73000000).append("text")
//     .attr("x", (d) => (d.x0 + d.x1) / 2.0 )
//     .attr("y", (d) => (d.y1 + d.y0) / 2.0)
//     .attr("dy", "0.5em")
//     .attr("text-anchor", "middle")
//     .attr("font-size", font_size)
//     .attr("fill", "black")
//     .attr("font-family", "proxima-nova")
//     // .text(d => d.data.name)
//     .each(function(d) { 
//         const width = Math.max(0, Math.floor(d.x1 - d.x0) - 4);
//         wrapText(d.data.name, d3.select(this), width);
//     })
//     .filter(d => d.value > 191000000).append("tspan")
//         .text(d => `$${format(Math.floor(d.value / 1000000))} million`)
//         .attr("x", (d) => (d.x0 + d.x1) / 2.0)
//         .attr("y", (d) => (d.y1 + d.y0) / 2.0)
//         .attr("dy", (d) => indent(d) + "em")
//         .attr("font-size", font_size)
//         .attr("fill", "black")

document.getElementById("treeice-container").append(svg.node());

// const statemap = new Map(topojson.feature(us, us.objects.states)).features.map(d => [d.id, d]);


const countymap = new Map(topojson.feature(us, us.objects.counties).features.map(d => [d.id, d]));

const fips_data = new Map();
// fips_text:
//  `State Name,County Name,City Name,State Code,State FIPS Code,County Code,StCnty FIPS Code,City Code,StCntyCity FIPS Code
parseCSV(fips_text).splice(1).forEach((w) => {
    fips_data.set(w[1] + w[3], w);
});

function datatomap(w) {
    const county = w.county;
    const query = county + w.state;
    let fips_county = fips_data.get(query);
    if (!fips_county) {
        if (query == "DISTRICT OF COLUMBIADC")
            return countymap.get("11001");
        else if (query == "GREATER BRIDGEPORTCT" || query == "WESTERN CONNECTICUTCT")
            return countymap.get("09001");
        else if (query == "SOUTHEASTERN CONNECTICUTCT") 
            return countymap.get("09011");
        else if (query == "CAPITOLCT")
            return countymap.get("09003");
        else if (county.endsWith("(CITY)"))
            fips_county = fips_data.get(county.slice(0, -7) + w.state);
    }
    if (fips_county)
        return countymap.get(fips_county[6]);
    else {
        console.log(county);
    }
}


// const path = d3.geoPath();

// const map_svg = d3.create("svg")
//       .attr("width", width)
//       .attr("height", height)
//       .attr("viewBox", [0, 0, width, height])
//       .attr("style", "width: 100%; height: auto; height: intrinsic;");

// map_svg.append("path")
//       .datum(topojson.feature(us, us.objects.nation))
//       .attr("fill", "#ddd")
//       .attr("d", path);

// map_svg.append("path")
//     .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
//     .attr("fill", "none")
//     .attr("stroke", "white")
//     .attr("stroke-linejoin", "round")
//     .attr("d", path);

// document.getElementById("map-container").append(map_svg.node())

function centroid(feature) {
    const path = d3.geoPath();
    return path.centroid(feature);
}

function adjust(position) {
    return [position[0] * total_width / width, position[1] * total_height / height];
}

function transition() {

    const duration = 5000;

    d3.select("#treeice-container").transition().duration(duration).style("background-color",null);
        
    leaf.selectAll("rect").transition().duration(duration)
            .attr("height", "2px")
            .attr("width", "2px")
            .attr("x", 0)
            .attr("y", 0)
        
    leaf.selectAll("text").remove();
    
    leaf.transition().duration(duration)
        .attr("transform", d => `translate(${adjust(centroid(datatomap(d.data)))})`)
   
}

document.addEventListener("keydown", (e) => {
    if (e.key == "d") {
        transition();
    }
});