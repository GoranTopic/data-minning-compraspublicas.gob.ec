import fs from 'fs';

const download_pdf = async (url, page, path) => {
    let pdfString = await page.evaluate( async url =>
        new Promise( async (resolve, reject) => {
            let timeout = setTimeout(() => // 10 minutes
                reject("pdf fetch timeout"), 10 * 1000 * 60);
            const reader = new FileReader();
            //console.log('created reader')
            const response = await window.fetch(url);
            //console.log('response')
            const data = await response.blob();
            //console.log('made data')
            reader.onload = () => { 
                //console.log('promised resolved');
                resolve(reader.result)
            };
            reader.onerror = () => { 
                //console.log('promised rejected'); 
                reject('Error occurred while reading binary string')
            };
            reader.readAsBinaryString(data);
        }), url
    );

    let filename = path + ".pdf"
    try{
        // save pdf binary string 
        const pdfData = Buffer.from(pdfString, 'binary');
        fs.writeFileSync(filename , pdfData);
        // console.log(`downloaded pdf: ${filename}`);
        return true;
    }catch(e){
        // did it downloaded
        console.error(`could not downloaded pdf: ${filename}`, e);
        return false;
    }
}

export default download_pdf
