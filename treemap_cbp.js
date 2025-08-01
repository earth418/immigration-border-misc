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

function font_sizepx2(d) {return (d.value / 3000000000) * 5 + 6}

function font_size2(d) {return font_sizepx2(d) + "px"}

function indent2(d) {
    const maxCharsPerLine = Math.floor((d.x1 - d.x0) / (font_sizepx2(d) * 0.7));
    return Math.floor(d.data.name.length / maxCharsPerLine) + 0.7;
}

// leaf.filter(d => d.value > 293000000).append("text")
//     .attr("x", (d) => (d.x0 + d.x1) / 2.0 )
//     .attr("y", (d) => (d.y1 + d.y0) / 2.0)
//     .attr("dy", "0.5em")
//     .attr("text-anchor", "middle")
//     .attr("font-size", font_size2)
//     .attr("fill", "black")
//     .attr("font-family", "proxima-nova")
//     // .text(d => d.data.name)
//     .each(function(d) { 
//         const width = Math.max(0, Math.floor(d.x1 - d.x0) - 4);
//         wrapText(d.data.name, d3.select(this), width);
//     })
//     .filter(d => d.value > 400000000).append("tspan")
//         .text(d => `$${format(Math.floor(d.value / 1000000))} million`)
//         .attr("x", (d) => (d.x0 + d.x1) / 2.0)
//         .attr("y", (d) => (d.y1 + d.y0) / 2.0)
//         .attr("dy", (d) => indent2(d) + "em")
//         // .attr("dy", (d) => (d.value < 400000000) ? "3.0em" : "1.0em")
//         .attr("font-size", font_size2)
//         .attr("fill", "black")

document.getElementById("treecbp-container").append(svg.node());


// function get_fips(w) {
//     const county = w.county;
//     const query = county + w.state;
//     let fips_county = fips_data.get(query);
//     if (query == "SKAGWAYAK")
//         fips_county = "02230"
//         // return countymap.get("02230");
//     else if (fips_county) {
//         fips_county = fips_county[6];
//     }
//     else {
//         if (query == "DISTRICT OF COLUMBIADC")
//             fips_county = "11001";
//             // return countymap.get("11001");
//         else if (query == "GREATER BRIDGEPORTCT" || query == "WESTERN CONNECTICUTCT" 
//             || query == "NAUGATUCK VALLEYCT" || (w.city == "STAMFORD" && w.state == "CT"))
//             fips_county = "09001";
//             // return countymap.get("09001");
//         else if (query == "SOUTHEASTERN CONNECTICUTCT") 
//             fips_county = "09011";
//             // return countymap.get("09011");
//         else if (query == "SOUTH CENTRAL CONNECTICUTCT") 
//             fips_county = "09009";
//             // return countymap.get("09009");
//         else if (query == "CAPITOLCT")
//             fips_county = "09003";
//             // return countymap.get("09003");
//         else if ((w.city == "LAS CRUCES" || w.city == "SANTA TERESA") && w.state == "NM")
//             fips_county = "35013";
//             // return countymap.get("35013");
//         else if (w.city == "NASHUA" && w.state == "NH")
//             // return countymap.get("33011");
//             fips_county = "33011";
//         else if (county.endsWith("(CITY)"))
//             fips_county = fips_data.get(county.slice(0, -7) + w.state)[6];
//     }
//     // console.log("query:", query, "county:", fips_county);
//     return fips_county;
// }

// function datatomap(w) {
//     const fips_county = get_fips(w);
//     if (fips_county) {
//         const frq = frequency.get(fips_county);
//         frequency.set((frq == undefined) ? 1 : frq + 1);
//         return countymap.get(fips_county);
//     } else {
//         console.log(fips_county);
//     }
// }

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

// function get_radius_

const projection1 = d3.geoMercator()
    .center([-97.42011851400741, 38.56265081052521])
    .translate([total_width / 2, total_height / 2])
    .scale(1900)


// function location_of(zipcode) {
//     const county = zipcode.substring(0,5);
//     let loc = zll.default[county];
//     if (loc == undefined) {
//         loc = zll.default["0" + county.substring(0,4)];
//         if (loc == undefined)
//             console.log(county);
//     }
//     const proj = projection1([loc[1], loc[0]]);
//     // console.log(proj);
//     return proj;
// }



function transition() {

    const duration = 20000;

    d3.select("#treecbp-container").transition()
        .duration(duration)
        .style("background-color",null);
        
    leaf.selectAll("rect").transition()
        .duration(duration)
        .attr("height", "5px")
        .attr("width", "5px")
        .attr("x", 0)
        .attr("y", 0)
        // .end().then((w) => )

    
    leaf.selectAll("text").remove();
    
    leaf.transition().duration(duration)
        .attr("transform", d => `translate(${projection1([d.data.lon, d.data.lat])})`)
        // .attr("transform", d => `translate(${location_of(d.data.zip)})`)
   
}

document.addEventListener("keydown", (e) => {
    if (e.key == "d") {
        transition();
    }
});