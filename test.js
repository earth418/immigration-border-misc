const puppeteer = require('puppeteer');
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
    
    const no_frames = 10;
    const duration_per_frame = 5000 / (no_frames - 1);
    let start_time = Date.now();

    for (let i = 0; i < no_frames; i++) {
        // let it = Date.now();
        await page.screenshot({omitBackground : true, fullPage: true, captureBeyondViewport: true, fromSurface: true, type : "png", path : "./images/image" + i +".png"});        
        const t = Math.max(0, i * duration_per_frame - (Date.now() - start_time));
        console.log("Stalling for ", t, "ms");
        await new Promise(r => setTimeout(r, t));
        console.log(Date.now() - start_time, " elapsed");
        if (i == 0)
            page.keyboard.press("d");
    }
    await page.close();
})();
// require(["puppeteer"], (puppeteer) => {

//     (async () => {
//         const browser = await puppeteer.launch();
//         const page = await browser.newPage();
//         await page.goto("http://127.0.0.1:3000/index.html");
//         page.screenshot({omitBackground : true, type : "png", path : "./image1.png"});
//     })();
// });