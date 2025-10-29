const puppeteer = require('puppeteer');

function time_based() {
    // const slow3G = puppeteer.networkConditions['Slow 3G'];

    (async () => {
        const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080
        })
        await page.goto("http://127.0.0.1:3000/index.html");
        const duration = 40000;
        let start_time = Date.now();

        let i = 0;
        await page.keyboard.press("d");
        while (Date.now() - start_time <= duration) {
            console.log("Frame", i, Date.now() - start_time, "ms elapsed");
            await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../images/distribute_points/image" + i +".png"});        
            i++;
        }
        // await page.close();
        await browser.close();
    })();
}

function time_based_f() {
    (async () => {
        const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080
        })
        await page.goto("http://127.0.0.1:3000/index.html");
        await page.keyboard.press("d");
        await new Promise(r => setTimeout(r, 4000));
        const duration = 10000;
        let i = 0;

        for (let kk = 0; kk < 3; ++kk, await page.keyboard.press("f")) {
            let start_time = Date.now();

            while (Date.now() - start_time <= duration) {
                console.log("Frame", i, Date.now() - start_time, "ms elapsed");
                await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../images/barchart/image" + i +".png"});        
                if (i == 0)
                    await page.keyboard.press("f");
                i++;
            }
        }
            // await page.close();
        await browser.close();
    })();
}



function time_based_g() {
    (async () => {
        const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080
        })
        await page.goto("http://127.0.0.1:3000/index.html");
        await page.keyboard.press("d");
        await new Promise(r => setTimeout(r, 101));
        await page.keyboard.press("f");
        await new Promise(r => setTimeout(r, 101));
        await page.keyboard.press("f");
        await new Promise(r => setTimeout(r, 101));
        await page.keyboard.press("f");
        await new Promise(r => setTimeout(r, 101));
        
        const duration = 10000;
        let i = 0;

        for (let kk = 0; kk < 2; ++kk) {
            // if (kk == 0) continue;
            let first_frame = true;
            let start_time = Date.now();

            while (Date.now() - start_time <= duration) {
                if (first_frame) {
                    first_frame = false;
                    await page.keyboard.press("g");
                }
                console.log("Frame", i, Date.now() - start_time, "ms elapsed");
                await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../images/barchart_expand/image" + i +".png"});        
                i++;
            }
        }
        await browser.close();
    })();
}

// time_based()
// time_based_f()

// ffmpeg -r 4 -i img*.png -c:v libx264 -vf out.mp4

// function d_based() {
//     // const slow3G = puppeteer.networkConditions['Slow 3G'];

//     (async () => {
//         const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
//         const page = await browser.newPage();
//         await page.setViewport({
//             width: 1920,
//             height: 1080
//         })
//         await page.goto("http://127.0.0.1:3000/index_pie.html");

//         const no_frames = 2 /* frames per data */ * 22 /* number of data*/;
    
//         for (let i = 0; i < no_frames; i++) {
//             await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../img2/image" + ((i < 10) ? "0" + i : i) +".png"});        
//             await page.keyboard.press("d");
//             // await page.reload();
//             // for (let kk = 0; kk < i; ++kk) {
//             //     await new Promise(r => setTimeout(r, 20));
//             // }
//             // await new Promise(r => setTimeout(r, 40));
//         }

//         await browser.close();
//     })();
// }

// time_based();
// d_based();


if (true) {
    // const slow3G = puppeteer.networkConditions['Slow 3G'];

    (async () => {
        const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080
        })
        await page.goto("http://127.0.0.1:3000/index.html");
        // const duration = 40000;
        // let start_time = Date.now();

        // let i = 0;
        await page.keyboard.press("d");
        await new Promise(r => setTimeout(r, 1000));
        await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../images/background.png"});        
        // while (Date.now() - start_time <= duration) {
            // console.log("Frame", i, Date.now() - start_time, "ms elapsed");
            // i++;
        // }
        // await page.close();
        await browser.close();
    })();
}