function calculate() {
    
    // extract information from form
    var english = document.getElementById('units-english').checked;
    var si = document.getElementById('units-si').checked;
    var shape = document.getElementById('shape').value;
    var radius = parseFloat(document.getElementById('radius').value);
    var height = parseFloat(document.getElementById('height').value);

    // get the proper units
    if (english) {
        var units = 'ft';
        var units_label = document.getElementById('units-english').value;
    } else {
        var units = 'm';
        var units_label = document.getElementById('units-si').value;
    }

    // calculate volume
    if (shape == 'Sphere') {
        var radius_units = units;
        var height_units = '-';
        var height = ''; // don't need height for sphere
        var formula = '3/4 * &#928; * r(' + units + ')^3';
        var vol = (3.0 / 4.0) * Math.PI * Math.pow(radius, 3);
    } else if (shape == 'Cone') {
        var radius_units = units;
        var height_units = units;
        var formula = '&#928; * r(' + units + ')^2 * h(' + units + ')/3';
        var vol = Math.PI * Math.pow(radius, 2) * (height / 3.0);
    } else if ( shape == 'Cylinder') {
        var radius_units = units;
        var height_units = units;
        var formula = '&#928; * r(' + units + ')^2 * h(' + units + ')'
        var vol = Math.PI * Math.pow(radius, 2) * height;
    } else {
        alert('wrong shape selected');
        return false;
    }

    var to_display = `
    <p>You selected to use ${units_label} units</p>
    <p>You selected to find the volume for a ${shape} shape</p>
    <table>
        <tr>
            <th>Shape</th>
            <th>Radius</th>
            <th>Height</th>
            <th>Volume</th>
        </tr>
        <tr>
            <td></td>
            <td><strong>(${radius_units})</strong></td>
            <td><strong>(${height_units})</strong></td>
            <td><strong>(${formula})</strong></td>
        </tr>
        <tr>
            <td>${shape}</td>
            <td>${radius}</strong></td>
            <td>${height}</td>
            <td>${vol.toFixed(5)}</td>
        </tr>
    </table>
    `; 
    document.getElementById('results').innerHTML = to_display;
}

function clearForm() {
    document.getElementById("form").reset();
    document.getElementById('results').innerHTML = "";
}