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
        // await page.goto("http://127.0.0.1:5500/index.html");
        
        // const no_frames = 50;
        // const duration_per_frame = 20000 / (no_frames - 1);
        
        const duration = 40000;
        let start_time = Date.now();

        // for (let i = 0; i < no_frames; i++) {

        // let it = Date.now();
            // const t = Math.max(0, i * duration_per_frame - (Date.now() - start_time));
            // await new Promise(r => setTimeout(r, t));
            // console.log("Stalling for ", t, "ms");
        let i = 0;
        while (Date.now() - start_time < duration) {
            console.log("Frame", i, Date.now() - start_time, "ms elapsed");
            await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../img/image" + i +".png"});        
            if (i == 0)
                await page.keyboard.press("d");
            i++;
        }
        // await page.close();
        await browser.close();
    })();
}

// ffmpeg -r 4 -i img*.png -c:v libx264 -vf out.mp4

function d_based() {
    // const slow3G = puppeteer.networkConditions['Slow 3G'];

    (async () => {
        const browser = await puppeteer.launch({executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1920,
            height: 1080
        })
        await page.goto("http://127.0.0.1:3000/index_pie.html");

        const no_frames = 2 /* frames per data */ * 22 /* number of data*/;
    
        for (let i = 0; i < no_frames; i++) {
            await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "../img2/image" + ((i < 10) ? "0" + i : i) +".png"});        
            await page.keyboard.press("d");
            // await page.reload();
            // for (let kk = 0; kk < i; ++kk) {
            //     await new Promise(r => setTimeout(r, 20));
            // }
            // await new Promise(r => setTimeout(r, 40));
        }

        await browser.close();
    })();
}

// time_based();
d_based();