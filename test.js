const puppeteer = require('puppeteer');
// const slow3G = puppeteer.networkConditions['Slow 3G'];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto("http://127.0.0.1:3000/index.html");
    
    page.keyboard.press("d");
    const no_frames = 4;
    const duration_per_frame = 2000 / no_frames;
    let start_time = Date.now();

    for (let i = 0; i < no_frames; i++) {
        let it = Date.now();
        await page.screenshot({omitBackground : true, type : "png", path : "./images/image" + i +".png"});        
        const t = Math.max(0, duration_per_frame - (Date.now() - it));
        await new Promise(r => setTimeout(r, t));
        console.log(Date.now() - start_time, " elapsed");
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