/**
 * Generates table html based on passed config and rows.
 * @param {Array[object]} rows 
 * @param {object} col_definition 
 *  {
 *      name: 'Name'
 *      selector: x => x.name
 *  }
 */
function get_table_html(rows, col_definition) {
    let html = '<table class="table table-striped table-bordered">';
        html += '<thead class="thead-dark">';
            html += '<tr>';
            html += '<th scope="col">#</th>';
            col_definition.forEach(col => {
                html += '<th scope="col">';
                html += col.name;
                html += '</th>';
            }, this);
            html += '</tr>';
        html += '</thead>';
        html += '<tbody>'
            html += get_table_body_content(rows, col_definition)
        html += '</tbody>'
    html += '</table>';
    return html;
}


function get_table_body_content(rows, col_definition) {
    let count = 1;
    let html = '';
    rows.forEach(row => {
        html += '<tr>';
            html += '<th scope="row">' + count++ + '</th>';
        col_definition.forEach(col => {
            html += '<td>';
            html += col.selector(row)
            html += '</td>'
        });
        html += '</tr>';
    }, this);
    return html;
}