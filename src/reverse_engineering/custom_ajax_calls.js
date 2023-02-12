
const queryProcessesCount = async ({ 
    startDate, 
    endDate, 
    palabrasClaves,
    entidadContratante,
    tipoDeContratacion,
    tipoDeCompra,
    codigoDelProceso,
    txtTiposContratacion,
}) => await new Promise( (resolve, reject) => {
    // get count of compras
    var url = HOST + 'interfazWeb.php';
    var obj = {
        method :'post',
        asynchronous: false,
        parameters :"__class=" 
        + "SolicitudCompra"
        + "&" + "__action=buscarProcesoxEntidadCount" 
        + "&" + `captccc2=0` 
        + "&" +`idus=`
        + "&" +`UsuarioID=`
        + "&" +`txtPalabrasClaves=${palabrasClaves}`
        + "&" +`Entidadbuscar=`
        + "&" +`txtEntidadContratante=${entidadContratante}`
        + "&" +`cmbEntidad=`
        + "&" +`txtTiposContratacion=${txtTiposContratacion}`
        + "&" +`txtCodigoTipoCompra=${tipoDeCompra}`
        + "&" +`txtCodigoProceso=${codigoDelProceso}`
        + "&" +`f_inicio=${startDate}`
        + "&" +`f_fin=${endDate}`
        + "&" +`count=`
        + "&" +`paginaActual=0`
        + "&" +`estado=`
        + "&" +`trx=50008`,
        onSuccess : function(resp, result) { resolve(result) },
        onFailure : function(resp, result) { reject("Error de conexión: " + resp.responseText); }
    }
    var myAjax = new Ajax.Request(url, obj);
})

const queryComprasPage = ({ 
    count,
    pagination,
    startDate, 
    endDate, 
    palabrasClaves,
    entidadContratante,
    tipoDeContratacion,
    tipoDeCompra,
    codigoDelProceso,
    txtTiposContratacion,
}) => new Promise( (resolve, reject) => {
    // get count of compras
    var url = HOST + 'interfazWeb.php';
    var obj = {
        method :'post',
        asynchronous: false,
        parameters :"__class=" 
        + "SolicitudCompra"
        + "&" + "__action=buscarProcesoxEntidad" 
        + "&" + `captccc2=1` 
        + "&" +`idus=`
        + "&" +`UsuarioID=`
        + "&" +`txtPalabrasClaves=${palabrasClaves}`
        + "&" +`Entidadbuscar=`
        + "&" +`txtEntidadContratante=${entidadContratante}`
        + "&" +`cmbEntidad=`
        + "&" +`txtTiposContratacion=${txtTiposContratacion}`
        + "&" +`txtCodigoTipoCompra=${tipoDeCompra}`
        + "&" +`txtCodigoProceso=${codigoDelProceso}`
        + "&" +`f_inicio=${startDate}`
        + "&" +`f_fin=${endDate}`
        + "&" +`count=${count}`
        + "&" +`paginaActual=${pagination}`
        + "&" +`estado=`
        + "&" +`trx=50008`,
        onSuccess : function(resp, result) { resolve(result) },
        onFailure : function(resp, result) { reject("Error de conexión: " + resp.responseText); }
    }
    var myAjax = new Ajax.Request(url, obj);
})

const decode = compra => {
    let decoded_compras = {};
    let code = { 
        c: 'Código',
        j: 'Tipo Compra',
        r: 'Entidad',
        d: 'Objeto de Proceso',  
        s: 'Provincia/Cantón',                            
        g: 'Estado del Proceso',                                  
        p: 'Presupuesto Referencial Total(sin iva)',                              
        f: 'Fecha de Publicación',                       
        i: 'idSoliCompra', // this is th hash the server uses to expose the compras page
        t: 't', //'7117' // unknown                                     
        u: 'u', // unknown
        z: 'z', // unknown                               
        v: 'api_version', // api version                                     
        e: 'e' //'modNo'   // unknown                 
    }
    for(let key of Object.keys(code))
       decoded_compras[code[key]] = compra[key];
    return decoded_compras;
}


export { queryComprasPage, queryProcessesCount, decode }
