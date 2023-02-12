/* the following is the function the website ses to make call the server. 
 * I collected the source code of the function, along with the paramters and the output of the function
 * for three difrent cases */

function ajax_call(data, clazz, action, callbackFunct) {
    var url = HOST + 'interfazWeb.php';
    var obj = {
        method :'post',
        asynchronous: false,
        parameters :"__class=" + clazz + "&__action=" + action + "&" + data,
        onSuccess : function(resp, result) {callbackFunct.apply(this, [ result, resp.responseText ]);},
        onFailure : function(resp, result) {alert("Error de conexión: " + resp.responseText);}
    }
    var myAjax = new Ajax.Request(url, obj);
}

// parameters
let param1 = {
    data: "captccc2=0&idus=&UsuarioID=&txtPalabrasClaves=&Entidadbuscar=&txtEntidadContratante=&cmbEntidad=&txtTiposContratacion=219&txtCodigoTipoCompra=&txtCodigoProceso=&f_inicio=2023-01-6&f_fin=2023-02-5&count=&paginaActual=0&estado=&trx=50008",
    clazz: "SolicitudCompra",
    action: "buscarProcesoxEntidadCount",
    callbackFunct: function contarProcesos(result,resp) {
        if(result != ""){
            totProcesos = result['count'];
            $('count').value = result['count'];
        }
        presentarProcesosInicial(0);		
    }
}
// response 1
let resp1 = {
"request": {
    "options": {
        "method": "post",
        "asynchronous": false,
        "contentType": "application/x-www-form-urlencoded",
        "encoding": "UTF-8",
        "parameters": {
            "__class": "SolicitudCompra",
            "__action": "buscarProcesoxEntidadCount",
            "captccc2": "1",
            "idus": "",
            "UsuarioID": "",
            "txtPalabrasClaves": "",
            "Entidadbuscar": "",
            "txtEntidadContratante": "",
            "cmbEntidad": "",
            "txtTiposContratacion": "219",
            "txtCodigoTipoCompra": "",
            "txtCodigoProceso": "",
            "f_inicio": "2023-01-6",
            "f_fin": "2023-02-5",
            "count": "163",
            "paginaActual": "0",
            "estado": "",
            "trx": "50008"
        },
        "evalJSON": true,
        "evalJS": true
    },
    "transport": {},
    "url": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/servicio/interfazWeb.php",
    "method": "post",
    "parameters": {
        "__class": "SolicitudCompra",
        "__action": "buscarProcesoxEntidadCount",
        "captccc2": "1",
        "idus": "",
        "UsuarioID": "",
        "txtPalabrasClaves": "",
        "Entidadbuscar": "",
        "txtEntidadContratante": "",
        "cmbEntidad": "",
        "txtTiposContratacion": "219",
        "txtCodigoTipoCompra": "",
        "txtCodigoProceso": "",
        "f_inicio": "2023-01-6",
        "f_fin": "2023-02-5",
        "count": "163",
        "paginaActual": "0",
        "estado": "",
        "trx": "50008"
    },
    "body": "__class=SolicitudCompra&__action=buscarProcesoxEntidadCount&captccc2=1&idus=&UsuarioID=&txtPalabrasClaves=&Entidadbuscar=&txtEntidadContratante=&cmbEntidad=&txtTiposContratacion=219&txtCodigoTipoCompra=&txtCodigoProceso=&f_inicio=2023-01-6&f_fin=2023-02-5&count=163&paginaActual=0&estado=&trx=50008",
    "_complete": true
},
    "transport": {},
    "readyState": 4,
    "status": 200,
    "statusText": "OK",
    "responseText": "\r\n\r\n\n\r\n",
    "headerJSON": {
        "count": "163"
    },
    "responseXML": null,
    "responseJSON": null
}
// result1
let result1 = {
    "count": "163"
}

// parameters 2
let param2 = {
    data: "captccc2=1&idus=&UsuarioID=&txtPalabrasClaves=&Entidadbuscar=&txtEntidadContratante=&cmbEntidad=&txtTiposContratacion=219&txtCodigoTipoCompra=&txtCodigoProceso=&f_inicio=2023-01-6&f_fin=2023-02-5&count=163&paginaActual=0&estado=&trx=50008",
    clazz: "SolicitudCompra",
    action: "buscarProcesoxEntidad",
    callbackFunct: function listarProcesos(result, resp) {
        $('cargando').innerHTML = '';		
        if(result=="fallo"){
            $('divProcesos').innerHTML = '<B> <font SIZE=2 color="red">Captcha Incorrecto</font></B> ';
        }else if(result==""){
            $('divProcesos').innerHTML = '<B> <font SIZE=2 color="red">No existen procesos para la consulta ingresada</font></B>';
        }else{
            consultaParametro();
            res = abrirTabla();
            res+=nuevaCabecera();
            result.each(function(regProcesos){
                //console.log(regProcesos);
                res+=nuevaFila();
                res+=nuevaCeldaLink(regProcesos.c, regProcesos.i,regProcesos.v);
                res+=nuevaCelda(regProcesos.r);
                res+=nuevaCelda(regProcesos.d);
                res+=nuevaCelda(regProcesos.g);                                              
                if (muestraTipoCompra == 'SI'){
                    if (regProcesos.j){
                        res+=nuevaCelda(regProcesos.j); //Tipo de compra
                    }else{
                        res+=nuevaCelda('');
                    }
                }
                res+=nuevaCelda(regProcesos.s);
                if(regProcesos.t==4505)
                    res+=nuevaCelda('No aplica');
                else if(regProcesos.t==4504){
                    res+=nuevaCelda(formatoMoneda4Dec(regProcesos.p));
                }
                else{//Mantis 2741: Controles para la visualizacion del precio referencial - Isabel Montero 24/01/2017
                    if(regProcesos.t==386){              
                        var estados =["Adjudicada","Finalizada","Adjudicado - Registro de Contratos","Ejecución de Contrato","En Recepción"]; 
                        if (regProcesos.g=='Borrador' && regProcesos.z!=''){
                            var fechaPub=regProcesos.z;
                        }else{
                            var fechaPub=regProcesos.f;
                        } 
                        if(!inArray(regProcesos.g,estados) && regProcesos.u!='' && fechaPub>fechaOcultaSIE){
                            res+=nuevaCelda('NO DISPONIBLE');
                        }
                        else{
                            res+=nuevaCelda(formatoMoneda(regProcesos.p));
                        }
                    }
                    else{//Fin cambios 2741
                        res+=nuevaCelda(formatoMoneda(regProcesos.p));
                    }
                }
                res+=nuevaCelda(regProcesos.f);
                //res+=nuevaCeldaOpcion(regProcesos.e, regProcesos.i);
                //res+=nuevaCelda(regProcesos.f);
                if (regProcesos.g=='Borrador'){
                    fechaProceso = formatoFecha(regProcesos.f + ' 00:00:00');
                    if(fechaProceso >= fechaBanderaLink){
                        res+=nuevaCeldaOpcionEliminar(regProcesos.g,regProcesos.i,fechaProceso);
                    }
                }else{
                    res+=nuevaCeldaOpcion(regProcesos.e, regProcesos.i);
                }                        
                res+=cerrarFila();
            });
            res+=cerrarTabla();
            res+=dibujarPaginadores();          
            $('divProcesos').innerHTML = res;
        }
        $("linkReload").click();
    }
}
// result2
let result2 = [ // count 20
    {
        "c": "ABI-EPMMOP-001-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 5,40 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 75, segunda planta del edificio principal junto a los accesos peatonales con la Empresa Pública Metropolitana de",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "18670.080000",
        "f": "2023-02-03 12:00:00",
        "i": "7LUrE0QhhVeg2FKBIQJiHmqdgX7pztVVzEg55RvC_rI,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-002-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 16,35 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 35A, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "40038.720000",
        "f": "2023-02-03 12:00:00",
        "i": "RdksJiCW3-Img2dIgQLRrIAyWuYSBP_puzRLkHJpSI4,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-003-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 22,91 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 17, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "56103.360000",
        "f": "2023-02-03 12:00:00",
        "i": "rceCANrM1MaHskAvEWbbjxyQmif0tBnE___ECIo_iyM,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-004-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 43,46 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 22 y 23, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "106428.480000",
        "f": "2023-02-03 12:00:00",
        "i": "GAARiLo2W5MWw7MynS_KVau1Ye3tziixpY984l42808,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-005-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 7,02 m2, ubicado en el Terminal Terrestre Interprovincial Carcelén, oficina número 07, sector boleterias junto a la estación urbano con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "17798.400000",
        "f": "2023-02-03 12:00:00",
        "i": "S2ET9bJKcrFvpdynHSpn7HHtgJzyL9YMakvg4OIWgT4,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-006-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 7,02 m2, ubicado en el Terminal Terrestre Interprovincial Carcelén, oficina número 05, sector boleterias junto a la estación urbano con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "17798.400000",
        "f": "2023-02-03 12:00:00",
        "i": "W6qVbZKVXArZJq1GEOmR3VeGtpTGpq2rBSY4LqRXHYQ,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-007-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 21.73 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 19, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "53214.240000",
        "f": "2023-02-03 12:00:00",
        "i": "UdV6c4kYYJJkFh-ypnnU_aasqSuC6c1R93Jt4X9bWfw,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-008-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 10,80 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 66 y 67, planta alta del edificio operacional junto a los accesos peatonales con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "37340.160000",
        "f": "2023-02-03 12:00:00",
        "i": "V7C1WVQLwuV4LYhuUmK_DBuXd2nXLfwj-SnLPbB77o4,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-009-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 32.79 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 32 y 33, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "105446.400000",
        "f": "2023-02-03 12:00:00",
        "i": "Qzo9N-hnvHTcoxRKPv0qi4tpDQMoXYfNWhdqvWLXJyw,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-010-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 22.91 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 21, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "56103.360000",
        "f": "2023-02-03 12:00:00",
        "i": "MjkTpuFh74cN5MQmbJad_EMWkNSJ1p2yv0bFtV8oyRo,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-011-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 16,20 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 70, 71 y 72, planta alta del edificio operacional junto a los accesos peatonales con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "56008.800000",
        "f": "2023-02-03 12:00:00",
        "i": "CU7kCwqqzdHAZRVMh3E3PTNlOWKaOYssDYBHlJZdBR8,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-012-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 32,79 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 43, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "80297.760000",
        "f": "2023-02-03 12:00:00",
        "i": "ayZOLfIUGksyt1qpqXXkg5Ksj1n0Ef-_aeTmsONMgK8,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-013-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 10,80 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 41 y 42, planta alta del edificio operacional junto a los accesos peatonales con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "37339.200000",
        "f": "2023-02-03 12:00:00",
        "i": "qD3YJTOKPyiAk1qt0vOXhcwCbTTkeuf0NK8qNfXmN6U,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-014-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 33,57 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 42, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "82207.200000",
        "f": "2023-02-03 12:00:00",
        "i": "hb5z_lNNsCVamwsOaVOyvsHqbABlRBoiS9PiGxGJKYE,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-015-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 21,73 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 18, planta baja del edificio de encomiendas y administración",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "53214.240000",
        "f": "2023-02-03 12:00:00",
        "i": "XfmnnlFpxCw1OuwNuViyC_wDulYrNqp9CHLT5ULck8E,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ABI-EPMMOP-016-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "Empresa Publica Metropolitana de Movilidad y Obras Publicas",
        "d": "arrendamiento de un espacio físico de una superficie de 10,8 m2, ubicado en el Terminal Terrestre Interprovincial Quitumbe, local número 6 y 57, planta alta del edificio operacional junto a los accesos peatonales con la Empresa Pública Metropolitana de Pasajeros y Metro de Quito",
        "s": "PICHINCHA / QUITO",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "37340.160000",
        "f": "2023-02-03 12:00:00",
        "i": "kZqShRTSEhR_w2NZacZNWl0meKTdbNAgPHbIwYz45E4,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "ARBI-GADM-002-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "GOBIERNO AUTONOMO DESCENTRALIZADO DEL CANTON MIRA",
        "d": "ARRENDAMIENTO PARA EL USO DE LA INFRAESTRUCTURA FÍSICA DEL LOCAL SEIS, UBICADO EN CENTRO DE COMERCIALIZACIÓN ARTESANAL Y AGROINDUSTRIAL DEL GADC – MIRA, PROVINCIA DEL CARCHI?",
        "s": "CARCHI / MIRA",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "35.710000",
        "f": "2023-02-03 13:00:00",
        "i": "9klam-pf80wNiobgVEvyRgO1m0Us8PKcUjKtQXmwawg,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "PEA-EMOVEP-0010-202",
        "j": "Servicio",
        "r": "EMPRESA PUBLICA DE MOVILIDAD TRANSITO Y TRANSPORTE DE CUENCA",
        "d": "SERVICIO DE ARRENDAMIENTO DEL KIOSCO No. 74 UBICADO EN EL INTERIOR DE LA TERMINAL TERRESTRE DEL CANTON CUENCA",
        "s": "AZUAY / CUENCA",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "46.970000",
        "f": "2023-02-03 13:00:00",
        "i": "L1A46L2dVTiJgiV0AmEQqJbd_NcNzEFU0pRdGXw8MAU,",
        "t": "7117",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "PEA-EMOVEP-009-2023",
        "j": "No aplica para Procedimientos Especiales",
        "r": "EMPRESA PUBLICA DE MOVILIDAD TRANSITO Y TRANSPORTE DE CUENCA",
        "d": "ARRENDAMIENTO DE LA BODEGA No. 3 UBICADO EN EL INTERIOR DE LA TERMINAL TERRESTRE DEL CANTON CUENCA.",
        "s": "AZUAY / CUENCA",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "225.400000",
        "f": "2023-02-03 13:00:00",
        "i": "fZel1J9cegNwGg8kDYScLNrdkXMLbTdICdUYkWTw2n0,",
        "t": "7118",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    },
    {
        "c": "PE-MMI-001-2023",
        "j": "Bien",
        "r": "COMPAÑIA DE ECONOMIA MIXTA MERCADO MAYORISTA DE IBARRA COMERCIBARRA",
        "d": "ADQUISICIÓN DE UN TERRENO PARA LA IMPLEMENTACIÓN DE LA FERIA DE VEHÍCULOS, CANTÓN IBARRA, PROVINCIA DE IMBABURA",
        "s": "IMBABURA / IBARRA",
        "g": "Audiencia de Preguntas y Aclaraciones",
        "p": "298046.690000",
        "f": "2023-02-03 13:00:00",
        "i": "uHJnjEIWU1lXtAMfK4D4tj97BQT6LQ2NmkKLfErMwpM,",
        "t": "7115",
        "u": "",
        "z": "",
        "v": "2",
        "e": "modNo"
    }
]


// parameters 3
let param3 = {
    data: 'cod=FECHA_OCULTA_VALORES_SIE',
    clazz: "Parametro",
    action: "buscarValorParametroSIE",
    callbackFunct: function fechaOcultar(result,resp){
        fechaOcultaSIE=result['valor'];
    }
}
// result3
let result3 = {
  "valor": "2017-02-04"
}

