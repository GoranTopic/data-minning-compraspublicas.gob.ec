const query_tab = async url =>
    await new Promise( (resolve, reject) => {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = res => { resolve(res) };
        xhttp.open("GET", url, false);
        xhttp.send()
    })

export { query_tab }
