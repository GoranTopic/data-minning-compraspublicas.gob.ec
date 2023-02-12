import { createWorker } from 'tesseract.js';
 
const worker = createWorker({
  logger: m => console.log(m)
});
 
(async () => {
  await worker.load();
  await worker.loadLanguage('eng');
  await worker.initialize('eng');
  const { data: { text } } = await worker.recognize('https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/exe/generadorCaptcha.php');
  console.log(text);
  await worker.terminate();
})();
