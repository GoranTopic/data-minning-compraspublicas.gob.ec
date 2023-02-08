import parseDescritionTable from './description.js'
import parseFechasTable from './fechas.js'
import parseProductosTable from './productos.js'
import parseParametrosTable from './parámetrosDeCalificación.js'
import parseArchivosTable from './archivos.js'

let tab_order = [ '', 'Descripción', 'Fechas', 'Productos', 'Parámetros de Calificación', '', 'Archivos' ] 

const parseTable = (type, html) =>{
    switch(type) {
        case 'Descripción':
            return parseDescritionTable(html);
        case 'Fechas':
            return parseFechasTable(html);
        case 'Productos':
            return parseProductosTable(html);
        case 'Parámetros de Calificación':
            return parseParametrosTable(html);
        case 'Archivos':
            return parseArchivosTable(html);
        default:
            // code block
            break;
    } 

}

export default parseTable
