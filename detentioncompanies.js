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

const array_data = parseCSV(geocoded_ice);
array_data[0] = ["origin","","","","","","","",""] // this is the name layer anyway

let data = array_data.map((w) => {
    return {name : w[0], value: w[1], country : w[2], address: w[3], county: w[5], city: w[4], state: w[6], zip: w[7], lat: w[8], lon: w[9], parent: "origin"};
});

data[0].parent = "";

const total_width = 1920, total_height = 1080;

// treemap1 starts at (106, 230)
// treemap1 ends (953, 935)
// treemap2 starts (960, 230)
// treemap2 ends (960, 1808)

const width = 975, height = 610;

const treemap_ht = 935 - 230;
const treemap_wd = 953 - 106;


const root_data = d3.stratify()
    .id((d) => d.name)
    .parentId((d) => d.parent)
    (data);

root_data.sum((d) => +d.value);

const root = d3.treemap()
.tile(d3.treemapSquarify)
.size([treemap_wd+106, treemap_ht+230])
.padding(0)
.paddingTop(230)
.paddingLeft(106)
(root_data);

const projection1 = d3.geoMercator()
    .center([-97.42011851400741, 38.56265081052521])
    .translate([total_width / 2, total_height / 2])
    .scale(1900)


function d_to_radius(d) {
    const val = Math.max(5,d.value / 10000000);
    return val;
}

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


leaf.selectAll("rect")
    .attr("height", d_to_radius)
    .attr("width", d_to_radius)
    .attr("x", d => -d_to_radius(d)/2.0)
    .attr("y", d => -d_to_radius(d)/2.0)
    .attr("rx", d_to_radius)
    .attr("ry", d_to_radius)

leaf.attr("transform", d => `translate(${projection1([d.data.lon, d.data.lat])})`)
